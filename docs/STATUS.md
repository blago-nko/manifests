# 📈 Статус документов

> ⚠️ **Этот файл обновляется автоматически** через GitHub Actions
> (`.github/workflows/update-status.yml`). Не редактируйте вручную.
> Реестр задач: [TASKS.md](../TASKS.md). Долгосрочный план: [ROADMAP.md](../ROADMAP.md).

---

## Текущее состояние

| # | Манифест | Файл | Версия | Дата | Статус | Протоколов |
|:-:|:---------|:-----|:------:|:----:|:------:|:----------:|
| 1 | САМ | `САМ.md` | 2.12-н | 2026-09-15 | 🟢 | 3 |
| 2 | СУМКа | `СУМКа.md` | 1.10-н | 2026-09-15 | 🟢 | 1 |
| 3 | САН | `САН.md` | 1.5-н | 2026-08-22 | 🟢 | 1 |
| 4 | ГРЕК-ПАНТЕОН | `ГРЕК-ПАНТЕОН.md` | 1.10-н | 2026-09-16 | 🟢 | 1 |
| 5 | МИГРАЦИЯ | `МИГРАЦИЯ.md` | 1.12-н | 2026-09-15 | 🟢 | 1 |
| 6 | ЛИЦ | `ЛИЦ.md` | 1.7-н | 2026-08-23 | 🟢 | 1 |
| 7 | AGENTS | `AGENTS.md` | 1.8-н | 2026-09-17 | 🟢 | 1 |

---

## Легенда статусов

| Иконка | Значение |
|:------:|:---------|
| 🟢 | Активен, актуален |
| 🟡 | Требует обновления |
| 🔴 | Устарел / конфликтует |
| ⚪ | Черновик |

---

## Состояние 14 доменов

> Источник: `domains-graph.yaml` (Протокол 016 САМ)

| # | Домен | Роль | Контур | Движок | Хостинг | Статус |
|:-:|:------|:-----|:------:|:------:|:-------:|:------:|
| 1 | blagorussia.ru | rss-hub | A | Hugo | GitHub Pages | 🟢 |
| 2 | obrazslov.ru | rss-site | A | Hugo | GitHub Pages | 🟢 |
| 3 | partnerstvo.blagorussia.ru | rss-site | A | Hugo | GitHub Pages | 🟢 |
| 4 | novosti.blagorussia.ru | rss-site | A | Hugo | GitHub Pages | 🟢 |
| 5 | ot-gorozan.blagorussia.ru | rss-site | A | Hugo | GitHub Pages | 🟢 |
| 6 | obavlenia.blagorussia.ru | rss-site | A | Hugo | GitHub Pages | 🟢 |
| 7 | interesnye-mesta.obrazslov.ru | rss-site | A | Hugo | GitHub Pages | 🟢 |
| 8 | moisites.blagorussia.ru | rss-site | A | Hugo | GitHub Pages | 🟢 |
| 9 | joga.blagorussia.ru | rss-site | A | Hugo | GitHub Pages | 🟢 |
| 10 | ideologia.obrazslov.ru | rss-site | A | Hugo | GitHub Pages | 🟢 |
| 11 | nasa-istoria.blagorussia.ru | rss-site | A | Hugo | GitHub Pages | 🟢 |
| 12 | grekpanteon.obrazslov.ru | knowledge-base | A | Astro | GitHub Pages | 🟢 |
| 13 | can.blagorussia.ru | pdn-platform | B | Next.js | Vercel | 🟢 |
| 14 | gallery.obrazslov.ru | nko-vitrina | V | Blogger | Blogger | 🟢 |

---

## Состояние манифестов

> Источник: `docs/manifests.yaml`

| Манифест | Версия | Дата последней редакции | Статус | Протоколов |
|:---------|:------:|:-----------------------:|:------:|:----------:|
| САМ | 2.12-н | 2026-09-15 | 🟢 | 3 |
| СУМКа | 1.10-н | 2026-09-15 | 🟢 | 1 |
| САН | 1.5-н | 2026-08-22 | 🟢 | 1 |
| ГРЕК-ПАНТЕОН | 1.10-н | 2026-09-16 | 🟢 | 1 |
| МИГРАЦИЯ | 1.12-н | 2026-09-15 | 🟢 | 1 |
| ЛИЦ | 1.7-н | 2026-08-23 | 🟢 | 1 |
| AGENTS | 1.8-н | 2026-09-17 | 🟢 | 1 |

---

## Ключевые метрики

| Метрика | Значение | Цель |
|:--------|:--------:|:----:|
| Доменов в экосистеме | 14 | 14 |
| Манифестов активно | 7 | 7 |
| Успешность автообновления STATUS.md | ≥99% | ≥99% |

---

## Активные риски

| # | Риск | Вероятность | Влияние | Митигация |
|:-:|:-----|:-----------:|:-------:|:----------|
| 1 | Таксономия domains-graph пуста (INFRA-020) | Высокая | Средняя | Задача в реестре |
| 2 | .markdownlintignore (INFRA-021) | Средняя | Низкая | Задача в реестре |
| 3 | Устаревшие удалённые ветки (INFRA-015) | Низкая | Низкая | Задача в реестре |

**Последнее обновление**: 17.09.2026
