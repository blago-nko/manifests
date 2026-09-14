# Манифесты архитектуры

![Sync](https://github.com/blago-nko/manifests/actions/workflows/sync-manifests.yml/badge.svg)
![Lint](https://github.com/blago-nko/manifests/actions/workflows/markdown-lint.yml/badge.svg)

Канонический репозиторий архитектурных манифестов экосистемы blago-nko: принципы системы, доменные платформы, план миграции, лицензирование и единые стандарты для ИИ-агентов.

> **ИИ-агентам:** перед любыми операциями в этом репозитории прочитайте [AGENTS.md](AGENTS.md) — обязательный протокол поведения (Codespaces-Only, PR-only, правила веток и префиксов).

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

## Структура репозитория

<!-- README:TREE:BEGIN -->

- 📁 **.github/**
  - 📁 **workflows/**
    - [apply-architecture-patches.yml](.github/workflows/apply-architecture-patches.yml)
    - [architecture-check.yml](.github/workflows/architecture-check.yml)
    - [auto-update-status.yml](.github/workflows/auto-update-status.yml)
    - [license-check.yml](.github/workflows/license-check.yml)
    - [manifest-consistency-check.yml](.github/workflows/manifest-consistency-check.yml)
    - [manifest-lint.yml](.github/workflows/manifest-lint.yml)
    - [markdown-lint.yml](.github/workflows/markdown-lint.yml)
    - [pr-prefix-check.yml](.github/workflows/pr-prefix-check.yml)
    - [readme-license-check.yml](.github/workflows/readme-license-check.yml)
    - [sync-manifests.yml](.github/workflows/sync-manifests.yml)
    - [sync-readme-sections.yml](.github/workflows/sync-readme-sections.yml)
    - [update-manifest-dates.yml](.github/workflows/update-manifest-dates.yml)
    - [update-status.yml](.github/workflows/update-status.yml)
  - [PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)
- 📁 **docs/**
  - [manifests.yaml](docs/manifests.yaml)
  - [STATUS.md](docs/STATUS.md)
- 📁 **scripts/**
  - [apply_arch_patches.py](scripts/apply_arch_patches.py)
  - [blogger_page_parser.py](scripts/blogger_page_parser.py)
  - [blogger_postid_rescue.py](scripts/blogger_postid_rescue.py)
  - [branch-protection.json](scripts/branch-protection.json)
  - [image_storage_adapter.py](scripts/image_storage_adapter.py)
  - [pdn_scanner.py](scripts/pdn_scanner.py)
  - [ruleset-repo.json](scripts/ruleset-repo.json)
  - [ruleset.json](scripts/ruleset.json)
  - [sanitize_images.py](scripts/sanitize_images.py)
  - [sync_manifests.py](scripts/sync_manifests.py)
  - [sync_readme_licenses.py](scripts/sync_readme_licenses.py)
  - [sync_readme_sections.py](scripts/sync_readme_sections.py)
  - [update_status.py](scripts/update_status.py)
- [.cursorrules](.cursorrules)
- [.markdownlint-cli2.jsonc](.markdownlint-cli2.jsonc)
- [.markdownlint.yaml](.markdownlint.yaml)
- [.markdownlintignore](.markdownlintignore)
- [AGENTS.md](AGENTS.md)
- [LICENSE](LICENSE)
- [LICENSE-CONTENT](LICENSE-CONTENT)
- [README.md](README.md)
- [STATUS.md](STATUS.md)
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
| [САМ](САМ.md) | Системный Архитектурный Манифест (78 принципов, 14 доменов) | САМ.md | 2.11-н | 🟢 Активен | 2026-08-27 | 3 |
| [СУМКа](СУМКа.md) | дистрибуция, соцсети, фиды | СУМКа.md | 1.9-н | 🟢 Активен | 2026-08-23 | 1 |
| [САН](САН.md) | Платформа САН (Сообщество Агентов Недвижимости, Next.js, RESO) | САН.md | 1.5-н | 🟢 Активен | 2026-08-22 | 1 |
| [ГРЕК-ПАНТЕОН](ГРЕК-ПАНТЕОН.md) | База знаний по античной мифологии (16 505+ страниц, Hugo) | ГРЕК-ПАНТЕОН.md | 1.8-н | 🟢 Активен | 2026-09-13 | 1 |
| [МИГРАЦИЯ](МИГРАЦИЯ.md) | План миграции 14 доменов на новую инфраструктуру | МИГРАЦИЯ.md | 1.11-н | 🟢 Активен | 2026-09-12 | 1 |
| [ЛИЦ](ЛИЦ.md) | Лицензирование и интеллектуальная собственность (CC BY 4.0 + MIT) | ЛИЦ.md | 1.7-н | 🟢 Активен | 2026-08-23 | 1 |
| [AGENTS](AGENTS.md) | Единые стандарты поведения ИИ-агентов экосистемы blago-nko | AGENTS.md | 1.4-н | 🟢 Активен | 2026-09-14 | 1 |

<!-- MANIFESTS:TABLE:END -->

## Репозитории экосистемы

<!-- README:REPOS:BEGIN -->

- [manifests](https://github.com/blago-nko/manifests) — Р•РґРёРЅС‹Р№ РёСЃС‚РѕС‡РЅРёРє РїСЂР°РІРґС‹: Р°СЂС…РёС‚РµРєС‚СѓСЂРЅС‹Рµ РјР°РЅРёС„РµСЃС‚С‹ Рё СЃС‚Р°РЅРґР°СЂС‚С‹ СЌРєРѕСЃРёСЃС‚РµРјС‹ blago-nko

<!-- README:REPOS:END -->

## Статус экосистемы

<!-- README:STATUS:BEGIN -->

**Текущий статус экосистемы:** [docs/STATUS.md](docs/STATUS.md)

Файл обновляется автоматически workflow `update-status.yml`.

<!-- README:STATUS:END -->

## Как работает автосинхронизация

- `sync-manifests.yml` — при пуше в `main`, по расписанию и вручную запускает `scripts/sync_manifests.py`: обновляет метаданные манифестов, таблицу выше и `docs/manifests.yaml`;
- `sync-readme-sections.yml` — обновляет в этом файле дерево файлов, список репозиториев и ссылку статуса;
- `update-manifest-dates.yml` — обновляет даты редакций в файлах с маркером `MANIFEST:METADATA:BEGIN`;
- `update-status.yml` — перегенерирует `docs/STATUS.md`.

## Вклад в проект

- Изменения — только через GitHub Codespaces или веб-интерфейс (Codespaces-Only Policy);
- Формат веток: `<тип>/<ПРЕФИКС>-<описание>`, например `feat/INFRA-014-readme-full`;
- Префиксы заголовков PR: `SAM-`, `CAN-`, `MIG-`, `LIC-`, `INFRA-`, `feat`, `fix`, `docs`, `chore`;
- Обязательные проверки: `Check PR Title Prefix`, `lint`, `architecture-check`.

Подробности — в [AGENTS.md, раздел 5](AGENTS.md).

## Лицензия

Контент — CC BY 4.0, код — MIT. Подробности: [ЛИЦ](ЛИЦ.md), [LICENSE](LICENSE), [LICENSE-CONTENT](LICENSE-CONTENT).

## Контакты

Владелец репозитория: [@bobralv-cyber](https://github.com/bobralv-cyber). Вопросы и предложения — через Issues.
