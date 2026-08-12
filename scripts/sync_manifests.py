#!/usr/bin/env python3
"""sync_manifests.py — автоматическая синхронизация реквизитов манифестов.

Единый источник правды: docs/manifests.yaml.

Логика:
1. Читает реестр docs/manifests.yaml.
2. Для каждого манифеста вырезает сгенерированные блоки, считает hash
   «чистого» текста и сравнивает с content_hash из реестра:
   - hash пустой (первый запуск) -> инициализация hash без повышения версии;
   - hash изменился              -> minor-версия +1 (1.1-н -> 1.2-н),
                                    last_revision = дата последнего коммита файла;
   - hash не изменился           -> ничего не меняется.
3. Генерирует таблицу в README.md (маркеры MANIFESTS:TABLE).
4. Генерирует в каждом манифесте таблицу реквизитов (MANIFEST:METADATA)
   и блок «Связанные документы» (MANIFEST:RELATED) — все активные
   манифесты, кроме текущего.
5. Проверяет существование файлов и ссылок.

Зависимости: pyyaml
"""

import hashlib
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "docs" / "manifests.yaml"
README = ROOT / "README.md"

META_BEGIN = "<!-- MANIFEST:METADATA:BEGIN -->"
META_END = "<!-- MANIFEST:METADATA:END -->"
REL_BEGIN = "<!-- MANIFEST:RELATED:BEGIN -->"
REL_END = "<!-- MANIFEST:RELATED:END -->"
TABLE_BEGIN = "<!-- MANIFESTS:TABLE:BEGIN -->"
TABLE_END = "<!-- MANIFESTS:TABLE:END -->"

STATUS_LABELS = {
    "active": "🟢 Активен",
    "draft": "🟡 Черновик",
    "archived": "⚪ Архив",
}


def fail(msg: str) -> None:
    print(f"❌ ОШИБКА: {msg}")
    sys.exit(1)


def normalize(text: str) -> str:
    """Нормализация текста для стабильного hash."""
    text = text.replace("\r\n", "\n")
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip("\n") + "\n"


def strip_block(text: str, begin: str, end: str) -> str:
    """Удаляет сгенерированный блок вместе с маркерами."""
    pattern = re.compile(
        r"[ \t]*" + re.escape(begin) + r".*?" + re.escape(end) + r"[ \t]*\n?",
        re.S,
    )
    return pattern.sub("", text)


def clean_content(raw: str) -> str:
    text = strip_block(raw, META_BEGIN, META_END)
    text = strip_block(text, REL_BEGIN, REL_END)
    return normalize(text)


def git_file_date(rel_path: str) -> str:
    """Дата последнего коммита, затрагивавшего файл (YYYY-MM-DD)."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel_path],
            capture_output=True, text=True, cwd=ROOT, check=True,
        ).stdout.strip()
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", out):
            return out
    except Exception:
        pass
    return date.today().isoformat()


def bump_version(version: str) -> str:
    """1.1-н -> 1.2-н (major и суффикс не меняются)."""
    m = re.fullmatch(r"(\d+)\.(\d+)(-\S+)?", (version or "").strip())
    if not m:
        fail(f"не распознана версия: {version!r}")
    return f"{m.group(1)}.{int(m.group(2)) + 1}{m.group(3) or ''}"


def cell(value) -> str:
    return str(value).replace("|", "\\|")


def meta_block(m: dict) -> str:
    rows = [
        "| Реквизит | Значение |",
        "|---|---|",
        f"| Манифест | {cell(m['short_title'])} |",
        f"| Название | {cell(m['title'])} |",
        f"| Описание | {cell(m['description'])} |",
        f"| Версия | {cell(m['version'])} |",
        f"| Статус | {cell(STATUS_LABELS[m['status']])} |",
        f"| Дата утверждения | {cell(m['approved_date'])} |",
        f"| Дата последней редакции | {cell(m['last_revision'] or '—')} |",
        f"| Протоколы | {cell(m['protocols'])} |",
    ]
    return f"{META_BEGIN}\n\n" + "\n".join(rows) + f"\n\n{META_END}"


def related_block(m: dict, active: list) -> str:
    lines = ["## Связанные документы", ""]
    for other in active:
        if other["file"] == m["file"]:
            continue
        lines.append(f"- [{other['short_title']} — {other['title']}]({other['file']})")
    return f"{REL_BEGIN}\n\n" + "\n".join(lines) + f"\n\n{REL_END}"


def rebuild(clean: str, meta: str, related: str) -> str:
    """Собирает файл: заголовок, таблица реквизитов, текст, связи."""
    lines = clean.split("\n")
    head_idx = next((i for i, ln in enumerate(lines) if ln.startswith("#")), None)
    if head_idx is not None:
        head = "\n".join(lines[: head_idx + 1])
        body = "\n".join(lines[head_idx + 1:]).lstrip("\n")
        result = f"{head}\n\n{meta}\n\n{body}\n"
    else:
        result = f"{meta}\n\n{clean}"
    result = result.rstrip("\n") + "\n\n" + related + "\n"
    return re.sub(r"\n{3,}", "\n\n", result)


def main() -> None:
    if not REGISTRY.exists():
        fail("не найден docs/manifests.yaml")
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}
    manifests = data.get("manifests") or []
    if not manifests:
        fail("в docs/manifests.yaml нет списка manifests")

    for m in manifests:
        for key in ("file", "short_title", "title", "description",
                    "version", "status", "approved_date", "protocols"):
            if key not in m or m[key] in (None, ""):
                fail(f"реестр: у манифеста {m.get('id', '?')} нет поля {key}")
        if m["status"] not in STATUS_LABELS:
            fail(f"реестр: неизвестный статус {m['status']!r} у {m['file']}")
        if not (ROOT / m["file"]).exists():
            fail(f"реестр: файл не найден: {m['file']}")

    report = []
    cleans = {}
    for m in manifests:
        rel = m["file"]
        raw = (ROOT / rel).read_text(encoding="utf-8")
        clean = clean_content(raw)
        cleans[rel] = clean
        new_hash = hashlib.sha256(clean.encode("utf-8")).hexdigest()
        old_hash = (m.get("content_hash") or "").strip()

        if not old_hash:
            m["content_hash"] = new_hash
            if not (m.get("last_revision") or "").strip():
                m["last_revision"] = git_file_date(rel)
            report.append(f"🆕 {rel}: инициализация hash (версия {m['version']} не менялась)")
        elif old_hash != new_hash:
            old_v = m["version"]
            m["version"] = bump_version(old_v)
            m["last_revision"] = git_file_date(rel)
            m["content_hash"] = new_hash
            report.append(f"🔄 {rel}: текст изменён: {old_v} -> {m['version']}, редакция {m['last_revision']}")
        else:
            report.append(f"✅ {rel}: без изменений (версия {m['version']})")

    REGISTRY.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    # --- таблица в README ---
    readme = README.read_text(encoding="utf-8")
    if TABLE_BEGIN not in readme or TABLE_END not in readme:
        fail("в README.md нет маркеров MANIFESTS:TABLE:BEGIN/END")
    rows = [
        "| Манифест | Описание | Файл | Версия | Статус | Дата последней редакции | Протоколы |",
        "|---|---|---|---|---|---|---:|",
    ]
    for m in manifests:
        rows.append(
            "| [{st}]({file}) | {desc} | {file} | {ver} | {status} | {rev} | {prot} |".format(
                st=cell(m["short_title"]), file=cell(m["file"]),
                desc=cell(m["description"]), ver=cell(m["version"]),
                status=cell(STATUS_LABELS[m["status"]]),
                rev=cell(m["last_revision"] or "—"), prot=cell(m["protocols"]),
            )
        )
    table = f"{TABLE_BEGIN}\n\n" + "\n".join(rows) + f"\n\n{TABLE_END}"
    readme = re.sub(
        re.escape(TABLE_BEGIN) + r".*?" + re.escape(TABLE_END),
        lambda _: table, readme, flags=re.S,
    )
    README.write_text(readme, encoding="utf-8")

    # --- файлы манифестов ---
    active = [m for m in manifests if m["status"] == "active"]
    for m in manifests:
        rel = m["file"]
        new = rebuild(cleans[rel], meta_block(m), related_block(m, active))
        old = (ROOT / rel).read_text(encoding="utf-8")
        if new != old:
            (ROOT / rel).write_text(new, encoding="utf-8")
            report.append(f"📝 {rel}: обновлены сгенерированные блоки")

    print("\n".join(report))
    print("✅ Синхронизация завершена.")


if __name__ == "__main__":
    main()
