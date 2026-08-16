# SAM-EXC-001 — Аварийная раскатка SAM-LIC-010 (2026-08-16)

- **Тип:** санкционированное исключение из Strict Branch Protocol (прямые пуши в main).
- **Обоснование:** срочная юридическая правка лицензий (AGPLv3 + CC BY-NC 4.0) во всех 15 репозиториях.
- **Решение:** SAM-LIC-010 (файлы LICENSE/LICENSE-CONTENT, коммиты fix(LIC) от 2026-08-16).
- **Компенсация:** рецидив исключён ruleset SAM-BRANCH-001 и workflow readme-license-check; синхронизация README людей выполняется только через PR скриптом scripts/sync_readme_licenses.py.
