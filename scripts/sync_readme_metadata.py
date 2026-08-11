#!/usr/bin/env python3
"""
SAM-INFRA-008: Автосинхронизация версий и дат манифестов в README.md.
Читает YAML-frontmatter манифестов и обновляет таблицу между маркерами
<!-- AUTO-VERSION-TABLE START/END --> в README.md.
"""

import re
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    raise SystemExit("Требуется PyYAML: pip install pyyaml")

MANIFESTS = [
    {"file": "САМ.md",           "name": "САМ",           "group": "arch"},
    {"file": "САН.md",           "name": "САН",           "group": "arch"},
    {"file": "СУМКа.md",         "name": "СУМКа",         "group": "arch"},
    {"file": "ГРЕК-ПАНТЕОН.md",  "name": "ГРЕК-ПАНТЕОН",  "group": "arch"},
    {"file": "МИГРАЦИЯ.md",      "name": "МИГРАЦИЯ",      "group": "arch"},
    {"file": "ЛИЦ.md",           "name": "ЛИЦ",           "group": "legal"},
    {"file": "AGENTS.md",        "name": "AGENTS",        "group": "tech"},
]

START_MARK = "<!-- AUTO-VERSION-TABLE START -->"
END_MARK = "<!-- AUTO-VERSION-TABLE END -->"


def parse_frontmatter(path: Path) -> dict:
    """Извлекает YAML из frontmatter Markdown-файла."""
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


def fmt_date(value) -> str:
    """Форматирует дату из ISO в DD.MM.YYYY."""
    if not value:
        return "—"
    if isinstance(value, datetime):
        return value.strftime("%d.%m.%Y")
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").strftime("%d.%m.%Y")
    except ValueError:
        return str(value)


def build_row(m: dict) -> str:
    """Строит одну строку таблицы для манифеста."""
    meta = parse_frontmatter(Path(m["file"]))
    version = meta.get("version", "—")
    status = meta.get("status", "—")
    date = fmt_date(meta.get("date") or meta.get("approved_date"))
    last_rev = fmt_date(meta.get("last_revision") or meta.get("date") or meta.get("approved_date"))
    return f"| [{m['name']}]({m['file']}) | {version} | {status} | {date} | {last_rev} |"


HEADER = "| Манифест | Версия | Статус | Дата утверждения | Последняя редакция |\n|----------|--------|--------|------------------|--------------------|"


def build_table() -> str:
    """Генерирует полный блок таблицы с маркерами."""
    arch = [build_row(m) for m in MANIFESTS if m["group"] == "arch"]
    legal = [build_row(m) for m in MANIFESTS if m["group"] == "legal"]
    tech = [build_row(m) for m in MANIFESTS if m["group"] == "tech"]
    parts = [
        START_MARK,
        "",
        "## Архитектурные манифесты",
        "",
        HEADER,
        *arch,
        "",
        "## Юридический пакет",
        "",
        HEADER,
        *legal,
        "",
        "## Технические регламенты",
        "",
        HEADER,
        *tech,
        "",
        f"*Таблица обновлена автоматически: {datetime.utcnow():%d.%m.%Y %H:%M} UTC (SAM-INFRA-008)*",
        "",
        END_MARK,
    ]
    return "\n".join(parts)


def update_readme():
    """Обновляет или вставляет таблицу в README.md."""
    readme = Path("README.md")
    text = readme.read_text(encoding="utf-8")
    table = build_table()

    pattern = re.compile(
        re.escape(START_MARK) + r".*?" + re.escape(END_MARK),
        re.DOTALL,
    )
    if pattern.search(text):
        new_text = pattern.sub(table.replace("\\", "\\\\"), text)
    else:
        anchor = "## Экосистема управляется"
        if anchor in text:
            new_text = text.replace(anchor, table + "\n\n" + anchor, 1)
        else:
            new_text = table + "\n\n" + text

    readme.write_text(new_text, encoding="utf-8")
    print("✓ README.md синхронизирован")


if __name__ == "__main__":
    update_readme()
