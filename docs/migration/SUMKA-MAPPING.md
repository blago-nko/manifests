# Реестр соответствия артефактов СУМКа → shared-assets (INFRA-050)

> Документ описывает, как требования манифеста СУМКа реализуются в общей библиотеке shared-assets.

## Принцип

СУМКа остаётся **источником требований** (что должно быть на странице), shared-assets становится **местом реализации** (как это сверстано и собрано). Каждый артефакт СУМКа получает строку в этом реестре со статусом и путём реализации.

## Раздел 5. Mobile-First и Geo-оптимизация

| Артефакт СУМКа | Реализация в shared-assets | Где живёт | Когда | Статус |
| :--- | :--- | :--- | :--- | :--- |
| 5.1 Mobile-First для всех 14 сайтов | baseof.html (Hugo) / layout-компонент (Astro) + CSS breakpoints 360/768/1024, flex/grid, touch-цели ≥44px | hugo/layouts/_default/, web/css/main.css | Этап 2 (пилот) | ⬜ |
| 5.2 Google Discover | meta-теги в head-partial: max-image-preview:large, max-snippet:-1 | hugo/layouts/partials/head.html | Этап 2 | ⬜ |
| 5.3 Open Graph и Twitter Cards | partial og-meta.html с динамическими тегами из front matter | hugo/layouts/partials/ | Этап 2 | ⬜ |
| 5.4 JSON-LD разметка | шорткод jsonld.html для Article, FAQPage, BreadcrumbList | hugo/layouts/shortcodes/ | Этап 2 | ⬜ |
| 5.4.7 Расширенная семантическая разметка для ИИ-поисковиков | additional JSON-LD для AI-агентов | hugo/layouts/shortcodes/ | Этап 3 | ⬜ |
| 5.4.8 Стандарты для gallery.obrazslov.ru | ImageGallery, FAQPage, блок «Раскрытие интересов» | astro/src/components/ | Этап 4 | ⬜ |
| 5.5 Чек-лист для Google Discover | автоматическая проверка в CI (PageSpeed Insights API) | scripts/ | Фаза 4 | ⬜ |
| 5.6 Image Sanitization Pipeline | script для ресайза ≤1600px, конвертации в WebP, удаления EXIF | scripts/image_sanitizer.py | Этап 1 (пилот) | ⬜ |
| 5.7 Регламент атрибуции изображений для grekpanteon | partial image-attribution.html с метаданными автора | hugo/layouts/partials/ | Этап 3 (MIG-012) | ⬜ |

## Раздел 1. Архитектура контентного конвейера

| Артефакт СУМКа | Реализация в shared-assets | Где живёт | Когда | Статус |
| :--- | :--- | :--- | :--- | :--- |
| 1.1 Источники контента | скрипты импорта из Blogger (blogger_export.py, media_downloader.py) | scripts/ | Этап 1 | ⬜ |
| 1.2 Контекстный билдер (ИИ-паспорт статьи) | front matter generator (AI-summary, tags, categories) | scripts/ | Этап 1 | ⬜ |
| 1.3 Лингвистический шлюз качества | spellcheck + grammar check в CI (LanguageTool API) | .github/workflows/ | Фаза 4 | ⬜ |
| 1.4 Мульти-ролевая атрибуция | partial author-card.html с ролями (автор, редактор, фотограф) | hugo/layouts/partials/ | Этап 3 | ⬜ |
| 1.5 URL-структура по типам сайтов | permalinks в config.toml каждого сайта; маппинг старых URL → новых | config.toml, scripts/url_mapping.py | Этап 2 | ⬜ |

## Раздел 2. Дистрибуция в социальные сети

| Артефакт СУМКа | Реализация в shared-assets | Где живёт | Когда | Статус |
| :--- | :--- | :--- | :--- | :--- |
| 2.1 ISocialDistributionService | скрипт публикации в ВК, Telegram, Дзен (Python) | scripts/social_publisher.py | Фаза 4 | ⬜ |
| 2.2 Лимиты для чужих групп | throttling logic в social_publisher.py | scripts/ | Фаза 4 | ⬜ |
| 2.3 Лимиты для собственных групп | queue + retry logic | scripts/ | Фаза 4 | ⬜ |
| 2.4 Штрафная пауза | cooldown mechanism | scripts/ | Фаза 4 | ⬜ |
| 2.5 Видео-Матрица РФ (Content-Based Routing) | выбор видеохостинга (Rutube/VK Video/YouTube) по geo | scripts/ | Фаза 4 | ⬜ |

## Раздел 3. Дистрибуция в фиды и каталоги

| Артефакт СУМКа | Реализация в shared-assets | Где живёт | Когда | Статус |
| :--- | :--- | :--- | :--- | :--- |
| 3.1 Google Merchant Center (XML) | генератор product feed из front matter | scripts/merchant_feed.py | Фаза 4 | ⬜ |
| 3.2 Meta Business Suite (JSON Graph API) | скрипт публикации через Graph API | scripts/meta_publisher.py | Фаза 4 | ⬜ |
| 3.3 Яндекс.Бизнес, Дзен, ВК, Telegram | универсальный publisher с адаптерами | scripts/ | Фаза 4 | ⬜ |
| 3.4 Throttling и квоты | rate limiting per platform | scripts/ | Фаза 4 | ⬜ |

## Раздел 4. ИИ-агенты дистрибуции

| Артефакт СУМКа | Реализация в shared-assets | Где живёт | Когда | Статус |
| :--- | :--- | :--- | :--- | :--- |
| 4.1 Реестр ИИ-агентов | конфиг agents.yaml с ролями и permissions | config/ | Фаза 4 | ⬜ |
| 4.2 Режимы работы seo_outreach | скрипт генерации outreach-писем (AI-powered) | scripts/seo_outreach.py | Фаза 4 | ⬜ |

## Раздел 6. Единый центр управления (Дашборд)

| Артефакт СУМКа | Реализация в shared-assets | Где живёт | Когда | Статус |
| :--- | :--- | :--- | :--- | :--- |
| 6.1 Админка для всех 14 сайтов | Hugo Admin UI (децентрализованная, через GitHub PR) | отдельно | Фаза 4 | ⬜ |
| 6.2 Модерация контента | workflow approval (PR review + CI checks) | .github/workflows/ | Фаза 4 | ⬜ |
| 6.3 Аналитика трафика | self-hosted Matomo/Plausible (Фаза 4) | отдельно | Фаза 4 | ⬜ |
| 6.4 Identity Graph | partial author-links.html (связи между авторами) | hugo/layouts/partials/ | Фаза 4 | ⬜ |
| 6.5 Управление социальными ссылками | конфиг social_links.yaml | config/ | Этап 2 | ⬜ |

## Раздел 7. Инструменты разработки и CI/CD

| Артефакт СУМКа | Реализация в shared-assets | Где живёт | Когда | Статус |
| :--- | :--- | :--- | :--- | :--- |
| 7.1 Инструменты разработки | Makefile с командами dev, build, deploy | Makefile | Этап 2 | ⬜ |
| 7.2 CI/CD процессы | reusable workflows (lint, test, deploy) | .github/workflows/ | Этап 2 | ⬜ |
| 7.3 Эволюционная модель хранения медиа | R2/YOS для медиа >5MB (hot/cold storage) | scripts/media_storage.py | Фаза 4 | ⬜ |
| 7.4 Сайт-витрина НКО | Hugo-тема с секциями «О нас», «Документы», «Контакты» | hugo/layouts/ | Этап 2 (пилот) | ⬜ |

## Раздел 8. Регистрация в поисковых системах

| Артефакт СУМКа | Реализация в shared-assets | Где живёт | Когда | Статус |
| :--- | :--- | :--- | :--- | :--- |
| 8.1 Матрица обязательности регистрации | checklist в docs/seo-registration.md | docs/ | Этап 5 | ⬜ |
| 8.2 Архитектура аккаунтов | документация в docs/seo-accounts.md | docs/ | Этап 5 | ⬜ |
| 8.3 Процесс регистрации | runbook в docs/seo-registration-runbook.md | docs/ | Этап 5 | ⬜ |
| 8.4 Файлы для верификации | static/verification/ (Google Search Console, Yandex.Webmaster) | hugo/static/verification/ | Этап 5 | ⬜ |

## Минимальный набор артефактов (все 14 сайтов)

Эти артефакты реализуются на пилоте (Этап 2) и rollout'ятся на все сайты в Этапе 3:

1. Mobile-first layout (baseof.html + CSS breakpoints)
2. Шапка и подвал (partials header.html, footer.html)
3. CookieConsent.js + стили баннера
4. Футер-лицензия CC BY-NC 4.0
5. Блок «Об экосистеме» (ссылки на 14 доменов)
6. Favicon и OG-изображения
7. RSS index.xml, sitemap.xml, robots.txt
8. Meta-тег верификации Search Console

Контроль: на пилоте чек-лист «артефакты СУМКа» проходится построчно; в Этапе 3 тот же чек-лист применяется к каждому сайту.

---

*Последнее обновление: 2026-09-18*
