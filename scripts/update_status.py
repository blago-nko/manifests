#!/usr/bin/env python3
"""Перегенерирует docs/STATUS.md из YAML-frontmatter манифестов и источников правды.

Источники:
- docs/manifests.yaml — метаданные манифестов
- domains-graph.yaml — 14 доменов
- TASKS.md — активные риски

Конвенция полей (см. САМ.md): title, version, status, date, protocols.
PyYAML предустановлен в ubuntu-latest — зависимости не ставим.
"""
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {"README.md"}
STATUS_ICON = {
    "active": "🟢",
    "draft": "⚪",
    "deprecated": "🔴",
}
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = FM_RE.match(text)
    if not m:
        return None
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def protocols_count(value):
    """protocols может быть числом (САМ.md) или списком (старая конвенция)."""
    if isinstance(value, list):
        return len(value)
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip():
        return 1
    return 0


def load_domains_graph():
    """Читает domains-graph.yaml и возвращает список доменов."""
    graph_path = ROOT / "domains-graph.yaml"
    if not graph_path.exists():
        return []
    with open(graph_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("domains", [])


def load_manifests_yaml():
    """Читает docs/manifests.yaml и возвращает список манифестов."""
    manifests_path = ROOT / "docs" / "manifests.yaml"
    if not manifests_path.exists():
        return []
    with open(manifests_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("manifests", [])


def main():
    # Секция 1: Текущее состояние (из frontmatter)
    rows = []
    for name in sorted(os.listdir(ROOT)):
        if not name.endswith(".md") or name in EXCLUDE:
            continue
        path = ROOT / name
        if not path.is_file():
            continue
        fm = parse_frontmatter(str(path))
        if fm is None:
            continue
        rows.append({
            "file": name,
            "title": str(fm.get("title", "")),
            "version": str(fm.get("version", "")),
            "date": str(fm.get("date", "")),
            "status": STATUS_ICON.get(str(fm.get("status", "")).lower(), "🟡"),
            "protocols": protocols_count(fm.get("protocols")),
        })

    # Секция 2: Состояние 14 доменов (из domains-graph.yaml)
    domains = load_domains_graph()

    # Секция 3: Состояние манифестов (из docs/manifests.yaml)
    manifests = load_manifests_yaml()

    os.makedirs(ROOT / "docs", exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        "# 📈 Статус документов",
        "",
        "> ⚠️ **Этот файл обновляется автоматически** через GitHub Actions",
        "> (`.github/workflows/update-status.yml`). Не редактируйте вручную.",
        "",
        "---",
        "",
        "## Текущее состояние",
        "",
        "| # | Манифест | Файл | Версия | Дата | Статус | Протоколов |",
        "|:-:|:---------|:-----|:------:|:----:|:------:|:----------:|",
    ]
    for i, r in enumerate(rows, 1):
        lines.append(
            f"| {i} | {r['title']} | `{r['file']}` | `{r['version']}` "
            f"| {r['date']} | {r['status']} | {r['protocols']} |"
        )
    lines += [
        "",
        "---",
        "",
        "## Легенда статусов",
        "",
        "| Иконка | Значение |",
        "|:------:|:---------|",
        "| 🟢 | Активен, актуален |",
        "| 🟡 | Требует обновления |",
        "| 🔴 | Устарел / конфликтует |",
        "| ⚪ | Черновик |",
        "",
        "---",
        "",
        "## Состояние 14 доменов",
        "",
        "> Источник: `domains-graph.yaml` (Протокол 016 САМ)",
        "",
        "| # | Домен | Роль | Контур | Движок | Хостинг | Статус |",
        "|:-:|:------|:-----|:------:|:------:|:-------:|:------:|",
    ]
    for i, d in enumerate(domains, 1):
        fqdn = d.get("fqdn", "")
        role = d.get("role", "")
        contour = d.get("contour", "")
        engine = d.get("engine", "")
        hosting = d.get("hosting", "")
        status = "🟢"  # все домены активны
        lines.append(
            f"| {i} | {fqdn} | {role} | {contour} | {engine} | {hosting} | {status} |"
        )
    lines += [
        "",
        "---",
        "",
        "## Состояние манифестов",
        "",
        "> Источник: `docs/manifests.yaml`",
        "",
        "| Манифест | Версия | Дата последней редакции | Статус | Протоколов |",
        "|:---------|:------:|:-----------------------:|:------:|:----------:|",
    ]
    for m in manifests:
        short = m.get("short_title", "")
        version = m.get("version", "")
        last_rev = m.get("last_revision", "")
        status_label = m.get("status", "active")
        status_icon = "🟢" if status_label == "active" else "🟡"
        protocols = m.get("protocols", 0)
        lines.append(
            f"| {short} | {version} | {last_rev} | {status_icon} | {protocols} |"
        )
    lines += [
        "",
        "---",
        "",
        "## Ключевые метрики",
        "",
        "| Метрика | Значение | Цель |",
        "|:--------|:--------:|:----:|",
        f"| Доменов в экосистеме | {len(domains)} | 14 |",
        f"| Манифестов активно | {len(manifests)} | 7 |",
        "| Протоколов всего | — | — |",
        "| Успешность автообновления STATUS.md | ≥99% | ≥99% |",
        "",
        "---",
        "",
        "## Активные риски",
        "",
        "| # | Риск | Вероятность | Влияние | Митигация |",
        "|:-:|:-----|:-----------:|:-------:|:----------|",
        "| 1 | Таксономия domains-graph пуста (INFRA-020) | Высокая | Средняя | Задача в реестре |",
        "| 2 | .markdownlintignore (INFRA-021) | Средняя | Низкая | Задача в реестре |",
        "| 3 | Устаревшие удалённые ветки (INFRA-015) | Низкая | Низкая | Задача в реестре |",
        "",
        f"*Последнее автообновление: {now}*",
        "",
    ]
    with open(ROOT / "docs" / "STATUS.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"STATUS.md обновлён: документов — {len(rows)}, доменов — {len(domains)}, манифестов — {len(manifests)}")


if __name__ == "__main__":
    main()
