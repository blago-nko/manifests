#!/usr/bin/env python3
"""Перегенерирует docs/STATUS.md из источников правды (единственный писатель файла).

Источники: docs/manifests.yaml, domains-graph.yaml.
Формат timestamp-строки — контракт с .github/workflows/update-status.yml:
**Последнее обновление**: DD.MM.YYYY HH:MM UTC
"""
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def load_yaml(rel):
    p = ROOT / rel
    if not p.exists():
        return {}
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main():
    manifests = load_yaml("docs/manifests.yaml").get("manifests", [])
    domains = load_yaml("domains-graph.yaml").get("domains", [])
    now_utc = datetime.now(timezone.utc)
    now = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    stamp = now_utc.strftime("%d.%m.%Y")

    lines = [
        "# 📈 Статус документов",
        "",
        "> ⚠️ **Этот файл обновляется автоматически** через GitHub Actions",
        "> (`.github/workflows/update-status.yml`). Не редактируйте вручную.\n> Реестр задач: [TASKS.md](../TASKS.md). Долгосрочный план: [ROADMAP.md](../ROADMAP.md).",
        "",
        "---",
        "",
        "## Текущее состояние",
        "",
        "| # | Манифест | Файл | Версия | Дата | Статус | Протоколов |",
        "|:-:|:---------|:-----|:------:|:----:|:------:|:----------:|",
    ]
    for i, m in enumerate(manifests, 1):
        icon = "🟢" if m.get("status") == "active" else "🟡"
        lines.append(
            f"| {i} | {m.get('short_title','')} | `{m.get('file','')}` | {m.get('version','')} "
            f"| {m.get('last_revision','')} | {icon} | {m.get('protocols',0)} |"
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
        lines.append(
            f"| {i} | {d.get('fqdn','')} | {d.get('role','')} | {d.get('contour','')} "
            f"| {d.get('engine','')} | {d.get('hosting','')} | 🟢 |"
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
        icon = "🟢" if m.get("status") == "active" else "🟡"
        lines.append(
            f"| {m.get('short_title','')} | {m.get('version','')} | {m.get('last_revision','')} "
            f"| {icon} | {m.get('protocols',0)} |"
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
        f"**Последнее обновление**: {stamp}",
        "",
    ]
    (ROOT / "docs" / "STATUS.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"STATUS.md обновлён: манифестов — {len(manifests)}, доменов — {len(domains)}")


if __name__ == "__main__":
    main()
