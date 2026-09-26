# Манифесты архитектуры

![Sync](https://github.com/blago-nko/manifests/actions/workflows/sync-manifests.yml/badge.svg)
![Lint](https://github.com/blago-nko/manifests/actions/workflows/markdown-lint.yml/badge.svg)

Канонический репозиторий архитектурных манифестов экосистемы blago-nko: принципы системы, доменные платформы, план миграции, лицензирование и единые стандарты для ИИ-агентов.

> **ИИ-агентам:** перед любыми операциями в этом репозитории прочитайте [AGENTS.md](AGENTS.md) — обязательный протокол поведения (Codespaces-Only, PR-only, правила веток и префиксов).

## 🧭 Навигация (старт здесь)

| Документ | Зачем |
| :--- | :--- |
| [AGENTS.md](AGENTS.md) | Протокол поведения ИИ-агентов (обязателен перед любыми операциями) |
| [TASKS.md](TASKS.md) | Реестр задач и протоколов (что делаем сейчас) |
| [ROADMAP.md](ROADMAP.md) | Долгосрочные направления развития (P2) |
| [docs/STATUS.md](docs/STATUS.md) | Статус документов, доменов и метрик |
| [domains-graph.yaml](domains-graph.yaml) | Машиночитаемый граф экосистемы (Протокол 016) |

## О проекте

**Архитектурный манифест** — markdown-документ, фиксирующий принципы, границы и правила разработки одного из доменов экосистемы.

Принципы репозитория:

- **Единственный источник правды** — манифесты хранятся только здесь;
- **Тело правит человек, метаданные — машина** — текст через PR человека, версии/даты/hash через скрипты;
- **Полная аудируемость** — каждое изменение через Pull Request с проверками.

Иерархия документов:

1. [САМ](САМ.md) — системные принципы (верхний уровень);
2. доменные манифесты: [СУМКа](СУМКа.md), [САН](САН.md), [ГРЕК-ПАНТЕОН](ГРЕК-ПАНТЕОН.md), [МИГРАЦИЯ](МИГРАЦИЯ.md);
3. [ЛИЦ](ЛИЦ.md) — лицензирование;
4. [AGENTS.md](AGENTS.md) — протоколы ИИ-агентов.

## 🌐 Экосистема в цифрах

- **14 доменов** в трёх контурах: A (основная сеть: 13 сайтов на Hugo + база знаний), B (изолированный контур ПДн, 152-ФЗ), V (витрина НКО);
- **7 манифестов** — принципы и правила доменов (иерархия: САМ → доменные → ЛИЦ → AGENTS);
- **13 рубрик таксономии** — единая классификация контента (Протокол 016.2);
- живой статус — в [docs/STATUS.md](docs/STATUS.md).

## Структура репозитория

<!-- README:TREE:BEGIN -->

- 📁 **.github/**
  - 📁 **ISSUE_TEMPLATE/**
    - [bug_report.md](.github/ISSUE_TEMPLATE/bug_report.md)
    - [config.yml](.github/ISSUE_TEMPLATE/config.yml)
    - [feature_request.md](.github/ISSUE_TEMPLATE/feature_request.md)
  - 📁 **workflows/**
    - [apply-architecture-patches.yml](.github/workflows/apply-architecture-patches.yml)
    - [architecture-check.yml](.github/workflows/architecture-check.yml)
    - [backup-ecosystem.yml](.github/workflows/backup-ecosystem.yml)
    - [license-check.yml](.github/workflows/license-check.yml)
    - [manifest-consistency-check.yml](.github/workflows/manifest-consistency-check.yml)
    - [manifest-lint.yml](.github/workflows/manifest-lint.yml)
    - [markdown-lint.yml](.github/workflows/markdown-lint.yml)
    - [pr-prefix-check.yml](.github/workflows/pr-prefix-check.yml)
    - [readme-license-check.yml](.github/workflows/readme-license-check.yml)
    - [sync-manifests.yml](.github/workflows/sync-manifests.yml)
    - [sync-readme-sections.yml](.github/workflows/sync-readme-sections.yml)
    - [tests.yml](.github/workflows/tests.yml)
    - [update-status.yml](.github/workflows/update-status.yml)
  - [CODEOWNERS](.github/CODEOWNERS)
  - [PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)
- 📁 **docs/**
  - 📁 **backup/**
    - [backup-plan.yaml](docs/backup/backup-plan.yaml)
    - [RESTORE.md](docs/backup/RESTORE.md)
  - 📁 **migration/**
    - [PILOT-checklist.md](docs/migration/PILOT-checklist.md)
    - [STRATEGY.md](docs/migration/STRATEGY.md)
    - [SUMKA-MAPPING.md](docs/migration/SUMKA-MAPPING.md)
  - [manifests.yaml](docs/manifests.yaml)
  - [STATUS.md](docs/STATUS.md)
- 📁 **scripts/**
  - [apply_arch_patches.py](scripts/apply_arch_patches.py)
  - [blogger_export.py](scripts/blogger_export.py)
  - [blogger_page_parser.py](scripts/blogger_page_parser.py)
  - [blogger_postid_rescue.py](scripts/blogger_postid_rescue.py)
  - [branch-protection.json](scripts/branch-protection.json)
  - [check_docs_links.py](scripts/check_docs_links.py)
  - [check_tasks_registry.py](scripts/check_tasks_registry.py)
  - [image_storage_adapter.py](scripts/image_storage_adapter.py)
  - [media_downloader.py](scripts/media_downloader.py)
  - [pdn_scanner.py](scripts/pdn_scanner.py)
  - [ruleset-repo.json](scripts/ruleset-repo.json)
  - [ruleset.json](scripts/ruleset.json)
  - [sanitize_images.py](scripts/sanitize_images.py)
  - [sync_manifests.py](scripts/sync_manifests.py)
  - [sync_readme_licenses.py](scripts/sync_readme_licenses.py)
  - [sync_readme_sections.py](scripts/sync_readme_sections.py)
  - [update_status.py](scripts/update_status.py)
  - [url_mapping.py](scripts/url_mapping.py)
- 📁 **tests/**
  - 📁 **e2e/**
    - [test_domains.py](tests/e2e/test_domains.py)
  - 📁 **snapshots/**
    - [test_status_structure.py](tests/snapshots/test_status_structure.py)
  - [test_check_docs_links.py](tests/test_check_docs_links.py)
  - [test_check_tasks_registry.py](tests/test_check_tasks_registry.py)
  - [test_update_status.py](tests/test_update_status.py)
- [.cursorrules](.cursorrules)
- [.gitignore](.gitignore)
- [.markdownlint-cli2.jsonc](.markdownlint-cli2.jsonc)
- [.markdownlint.yaml](.markdownlint.yaml)
- [AGENTS.md](AGENTS.md)
- [CHANGELOG.md](CHANGELOG.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [domains-graph.yaml](domains-graph.yaml)
- [LICENSE](LICENSE)
- [LICENSE-CONTENT](LICENSE-CONTENT)
- [README.md](README.md)
- [requirements.txt](requirements.txt)
- [ROADMAP.md](ROADMAP.md)
- [SECURITY.md](SECURITY.md)
- [TASKS.md](TASKS.md)
- [ГРЕК-ПАНТЕОН.md](ГРЕК-ПАНТЕОН.md)
- [ЛИЦ.md](ЛИЦ.md)
- [МИГРАЦИЯ.md](МИГРАЦИЯ.md)
- [САМ.md](САМ.md)
- [САН.md](САН.md)
- [СУМКа.md](СУМКа.md)

<!-- README:TREE:END -->

## Список манифестов

<!-- MANIFESTS:TABLE:BEGIN -->

| Манифест | Описание | Файл | Версия | Статус | Дата последней редакции | Протоколы |
|---|---|---|---|---|---|---:|
| [САМ](САМ.md) | Системный Архитектурный Манифест (78 принципов, 14 доменов) | САМ.md | 2.13-н | 🟢 Активен | 2026-09-24 | 3 |
| [СУМКа](СУМКа.md) | дистрибуция, соцсети, фиды | СУМКа.md | 1.11-н | 🟢 Активен | 2026-09-24 | 1 |
| [САН](САН.md) | Платформа САН (Сообщество Агентов Недвижимости, Next.js, RESO) | САН.md | 1.6-н | 🟢 Активен | 2026-09-24 | 1 |
| [ГРЕК-ПАНТЕОН](ГРЕК-ПАНТЕОН.md) | База знаний по античной мифологии (~350 страниц сейчас; цель 16 505+, Hugo→Astro) | ГРЕК-ПАНТЕОН.md | 1.10-н | 🟢 Активен | 2026-09-16 | 1 |
| [МИГРАЦИЯ](МИГРАЦИЯ.md) | План миграции 14 доменов на новую инфраструктуру | МИГРАЦИЯ.md | 1.13-н | 🟢 Активен | 2026-09-24 | 1 |
| [ЛИЦ](ЛИЦ.md) | Лицензирование и интеллектуальная собственность (AGPLv3 + CC BY-NC 4.0) | ЛИЦ.md | 1.7-н | 🟢 Активен | 2026-08-23 | 1 |
| [AGENTS](AGENTS.md) | Единые стандарты поведения ИИ-агентов экосистемы blago-nko | AGENTS.md | 1.8-н | 🟢 Активен | 2026-09-17 | 1 |

<!-- MANIFESTS:TABLE:END -->

## Репозитории экосистемы

<!-- README:REPOS:BEGIN -->

- [manifests](https://github.com/blago-nko/manifests) — Единый источник правды: архитектурные манифесты и стандарты экосистемы blago-nko
- [obrazslov](https://github.com/blago-nko/obrazslov) — Образ слов — база знаний экосистемы blago-nko (пилот миграции с Blogger на Hugo)
- [shared-assets](https://github.com/blago-nko/shared-assets) — Общие ассеты экосистемы: Hugo-тема, Astro-компоненты, CookieConsent, CSS/JS, RSS

<!-- README:REPOS:END -->

## Статус экосистемы

<!-- README:STATUS:BEGIN -->

**Текущий статус экосистемы:** [docs/STATUS.md](docs/STATUS.md)

Файл обновляется автоматически workflow `update-status.yml`.

<!-- README:STATUS:END -->

## 🤖 Как работает автосинхронизация

- **Три писателя — три цели:** `sync-manifests.yml` (метаданные манифестов + таблица README), `sync-readme-sections.yml` (дерево/репозитории/статус README), `update-status.yml` (docs/STATUS.md);
- **Семь валидаторов** на каждом PR: markdown-lint, architecture-check, manifest-consistency, license-check и другие;
- **Контракт единственного писателя:** docs/STATUS.md пишет только `scripts/update_status.py`;
- **Без шума:** авто-PR создаётся только при реальном диффе (не более одного в день).

## Вклад в проект

- Изменения — только через GitHub Codespaces или веб-интерфейс (Codespaces-Only Policy);
- Формат веток: `<тип>/<ПРЕФИКС>-<описание>`, например `feat/INFRA-014-readme-full`;
- Префиксы заголовков PR: `SAM-`, `CAN-`, `MIG-`, `LIC-`, `INFRA-`, `feat`, `fix`, `docs`, `chore`;
- Обязательные проверки: `Check PR Title Prefix`, `lint`, `architecture-check`.

Подробности — в [AGENTS.md, раздел 5](AGENTS.md).

## Лицензия

Контент — CC BY-NC 4.0, код — AGPLv3. Подробности: [ЛИЦ](ЛИЦ.md), [LICENSE](LICENSE), [LICENSE-CONTENT](LICENSE-CONTENT).

## Контакты

Владелец репозитория: [@bobralv-cyber](https://github.com/bobralv-cyber). Вопросы и предложения — через Issues.
