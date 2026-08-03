#!/usr/bin/env python3
"""Перегенерирует docs/STATUS.md из YAML-frontmatter манифестов в корне.

Конвенция полей (см. САМ.md): title, version, status, date, protocols.
PyYAML предуставновлен в ubuntu-latest — зависимости не ставим.
"""
import os
import re
from datetime import datetime, timezone

import yaml

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


def main():
    rows = []
    for name in sorted(os.listdir(".")):
        if not name.endswith(".md") or name in EXCLUDE:
            continue
        fm = parse_frontmatter(name)
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

    os.makedirs("docs", exist_ok=True)
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
        f"*Последнее автообновление: {now}*",
        "",
    ]
    with open("docs/STATUS.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"STATUS.md обновлён: документов — {len(rows)}")


if __name__ == "__main__":
    main()
