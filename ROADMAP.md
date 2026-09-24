# 🗺️ Долгосрочный план развития экосистемы

> Текущее состояние экосистемы: [docs/STATUS.md](docs/STATUS.md).
>
> Этот документ описывает направления развития, которые не имеют чёткого done-критерия и идут как процессы. Конкретные задачи — в [TASKS.md](TASKS.md).

## P2 — Направления (ongoing)

### Миграция 14 доменов на новую инфраструктуру (MIG-002…014)

- Hugo + GitHub Pages для 13 сайтов на Hugo
- Astro для grekpanteon и interesnye-mesta
- Единые shared-assets из `blago-nko/shared-assets`
- RSS-hub архитектура (hub-and-spokes)
- Зависит от: INFRA-033 (shared-assets)
- После завершения миграции: активировать INFRA-031 (uptime-мониторинг доменов на новых площадках; Blogger-сайты не мониторим — аптайм вне нашего контура)

### Контент-инфраструктура

- Issue forms для предложений контента
- RSS-генераторы с единой таксономией
- Sitemap-генераторы (единые для всех 14)
- Медиа-пайплайн: загрузка → sanitize → R2 → CDN URL
- Аналитика: Plausible / Umami (self-hosted)

### Release management

- Semantic versioning экосистемы (v2026.09.0 и т.п.)
- Release notes на GitHub Releases
- Теги на критичных коммитах
- Canary-деплой для Hugo-темы

### Governance

- Архитектурный комитет — процесс утверждения изменений САМ
- RFC-процесс для крупных изменений
- Ежеквартальные ретроспективы
- Публичный roadmap

---

*Последнее обновление: 2026-09-16*

## CI-техдолг (до старта волны 1)

- **Node20 removal:** дедлайн 23.09.2026 прошёл. Actions (`checkout@v4`, `markdownlint-cli2-action@v18`, `configure-pages@v5`, `upload-artifact@v4`, `deploy-pages@v4`) target Node20, forced на Node24. Обновить до Node24-native версий до старта INFRA-083.
- **ubuntu-latest → Ubuntu 26.04:** rollout 19.10–19.11.2026. Пин `ubuntu-24.04` или явный тест `ubuntu-26.04` до волны 1.
