# Аудит документации на предмет смены стратегии хранения

**Дата:** Fri Oct  9 17:08:03 RTZ 2026
---

## 🚫 Секция 1: Устаревшая логика (Требует удаления/правки)
Поиск терминов: галерея, витрина, selenium, загрузк.*блогер, upload.*blogger
```text
./AGENTS.md:597:- Все изображения загружены на gallery.obrazslov.ru (Blogger, безлимитное хранение)
./docs/domains-list.md:29:## Витрина НКО (Контур V)
./docs/domains-list.md:33:| 15 | gallery.obrazslov.ru | nko-vitrina | Blogger | Blogger | 🟢 |
./docs/migration/STRATEGY.md:28:| 13 | gallery.obrazslov.ru | Фотоархив | Blogger | Хранение изображений в Blogger CDN (см. САМ п.2.4) |
./docs/migration/STRATEGY.md:56:### Этап 4: Astro-миграция (gallery)
./docs/migration/STRATEGY.md:58:Фото-галерея на Astro-компонентах из shared-assets.
./docs/migration/SUMKA-MAPPING.md:18:| 5.4.8 Стандарты для gallery.obrazslov.ru | ImageGallery, FAQPage, блок «Раскрытие интересов» | astro/src/components/ | Этап 4 | ⬜ |
./docs/migration/SUMKA-MAPPING.md:76:| 7.4 Сайт-витрина НКО | Hugo-тема с секциями «О нас», «Документы», «Контакты» | hugo/layouts/ | Этап 2 (пилот) | ⬜ |
./docs/STATUS.md:53:| 14 | gallery.obrazslov.ru | nko-vitrina | V | Blogger | Blogger | 🟢 |
./docs_audit_summary.md:7:Поиск терминов: галерея, витрина, selenium, загрузк.*блогер, upload.*blogger
./domains-graph.yaml:22:    note: сайт-витрина НКО
./domains-graph.yaml:98:  # d. Сайт-витрина НКО
./domains-graph.yaml:99:  - fqdn: gallery.obrazslov.ru
./README.md:39:- **14 доменов** в трёх контурах: A (основная сеть: 13 сайтов на Hugo + база знаний), B (изолированный контур ПДн, 152-ФЗ), V (витрина НКО);
./TASKS.md:19:| gallery | 🟡 Создан, виден в сети, без контента и оформления |
./TASKS.md:102:| **INFRA-108** | Настройка Blogger Gallery (`gallery.obrazslov.ru`) | Создание блога, привязка CNAME, получение API Key | 🔴 BLOCKER | 👤 | ⬜ | Источник правды для изображений |
./TASKS.md:103:| **INFRA-109** | Скрипт `upload_to_blogger.py` + интеграция с API | Автоматизация загрузки sanitized-файлов | 🔴 BLOCKER | 🤖→ | ⬜ | Зависит от INFRA-107, 108 |
./TASKS.md:129:| **MIG-013** | Миграция gallery.obrazslov.ru | Blogger, фотоархив (платформа не меняется); репозиторий gallery-npo под пайплайны | 🟡 | → | ⬜ | Этап 4 |
./TASKS.md:141:| **MIG-018** | Оформление gallery | Контент, `ImageGallery`, `FAQPage`, блок «Раскрытие интересов» | 🟡 | 🤖→👤 | ⬜ | Сейчас пуст |
./TASKS.md:144:| **MIG-022** | САН: витрина → Next.js | Статическая заглушка (без ПДн) → `can-secure-dev`/Vercel | 🟢 | 🤖→👤 | ❌ | Отменено: план САН изменён на Hugo (см. STRATEGY.md) |
./ГРЕК-ПАНТЕОН.md:380:#### 6.4.5. Стандарт для сайта-витрины `gallery.obrazslov.ru`
./ГРЕК-ПАНТЕОН.md:382:Для сайта-витрины НКО `gallery.obrazslov.ru` применяются следующие дополнительные требования:
./ГРЕК-ПАНТЕОН.md:384:1. **Главная страница:** разметка `ImageGallery` с полными метаданными (`publisher`, `author`, `license`, `hasPart`).
./ГРЕК-ПАНТЕОН.md:452:- Изображения Пантеона дублируются на сайте-витрине НКО `gallery.obrazslov.ru` с использованием:
./ГРЕК-ПАНТЕОН.md:457:- Сайт-витрина НКО `gallery.obrazslov.ru` позиционируется как **ФОТОАРХИВ НКО** — централизованное хранилище изображений всех проектов экосистемы.
./ГРЕК-ПАНТЕОН.md:598:### Изображение с атрибуцией (для `gallery.obrazslov.ru`)
./ГРЕК-ПАНТЕОН.md:614:### ImageGallery (для главной страницы `gallery.obrazslov.ru`)
./ГРЕК-ПАНТЕОН.md:619: "@type": "ImageGallery",
./ГРЕК-ПАНТЕОН.md:635: "contentUrl": "https://gallery.obrazslov.ru/images/zeus.webp",
./ГРЕК-ПАНТЕОН.md:644:### FAQPage (для `gallery.obrazslov.ru/p/faq.html`)
./ГРЕК-ПАНТЕОН.md:672: "text": "Изображения добавляются автоматически через IGalleryExporter при создании или обновлении объектов в САН и Пантеоне. Ручное добавление доступно редакторам через административную панель."
./ЛИЦ.md:115:- Blogger-витрина: ссылки в разделе "О блоге"
./МИГРАЦИЯ.md:28:- **Этап 1 (Быстрый переезд):** Все 14 сайтов переносятся на новую инфраструктуру в их текущем виде — 13 сайтов на Hugo как статические, `grekpanteon.obrazslov.ru` как статический дамп, `can.blagorussia.ru` — временный деперсонализированный статический архив (витрина) на Hugo (в репозитории организации `blago-nko`), не обрабатывающая ПДн. После готовности MVP происходит перенос кодовой базы в изолированный репозиторий `can-secure-dev` с развёртыванием на Vercel (Next.js + Supabase), `gallery.obrazslov.ru` — на Blogger с кастомным доменом.
./МИГРАЦИЯ.md:42:Архитектура и детали переноса для `grekpanteon.obrazslov.ru` описаны в отдельном Манифесте Грек-Пантеон, а для САН — в Манифесте САН. Настоящий манифест фокусируется на RSS-сайтах, общей инфраструктуре (DNS, хостинг, мониторинг, WAF, Image Sanitization, Blogger-витрина), SEO-преемственности и координации запуска с платформой САН и Пантеоном.
./МИГРАЦИЯ.md:50:- Сайт-витрина НКО `gallery.obrazslov.ru` — развёртывается на Blogger с кастомным доменом.
./МИГРАЦИЯ.md:75:| 14| `galleryobrazslovru.blogspot.com` | `gallery.obrazslov.ru` | **Новый** (Blogger с кастомным доменом, без переноса legacy-контента) |
./МИГРАЦИЯ.md:83:Настоящий документ описывает полный цикл переноса 14 сайтов экосистемы (11 RSS + САН + Пантеон + gallery), но с разделением ответственности: RSS-сайты и общие сервисы – в данном манифесте, САН и Пантеон – в их собственных манифестах.
./МИГРАЦИЯ.md:138:- **Единый дизайн с темизацией** – ВСЕ 14 сайтов (11 RSS + САН + Пантеон + gallery) используют единые shared-assets (CSS, JS, шаблоны) с вариациями `data-theme` для разных типов контента.
./МИГРАЦИЯ.md:212:### Контур В: Сайт-витрина НКО
./МИГРАЦИЯ.md:214:- **Домен:** `gallery.obrazslov.ru`.
./МИГРАЦИЯ.md:216:- **Репозиторий:** `gallery-npo`.
./МИГРАЦИЯ.md:424:#### 5.1.5. Сайт-витрина НКО gallery.obrazslov.ru
./МИГРАЦИЯ.md:426:**Назначение:** SEO-витрина + вечный архив изображений всех сайтов экосистемы + упрощённое управление для редакторов.
./МИГРАЦИЯ.md:428:Сайт-витрина НКО `gallery.obrazslov.ru` позиционируется как **ФОТОАРХИВ НКО** — централизованное хранилище изображений всех проектов экосистемы.
./МИГРАЦИЯ.md:457:#### 5.1.6. Технические требования к шаблону Blogger для gallery.obrazslov.ru
./МИГРАЦИЯ.md:469:- На главной странице: `ImageGallery` с полной атрибуцией издателя (`publisher`), автора (`author`) и лицензии (`license`).
./МИГРАЦИЯ.md:571:| gallery.obrazslov.ru | CNAME | ghs.google.com (Blogger) |
./МИГРАЦИЯ.md:579:| Функция/Компонент | 13 сайтов на Hugo | САН | gallery.obrazslov.ru |
./МИГРАЦИЯ.md:703:**Для gallery.obrazslov.ru:**
./САМ.md:34:d. **`gallery.obrazslov.ru`** (Blogger) — витрина НКО, тематический каталог изображений.
```

## ✅ Секция 2: Новая архитектура (Проверка наличия)
Поиск терминов: r2, cloudflare, cdn.obrazslov, object storage
```text
./.github/workflows/backup-ecosystem.yml:4:# Внешние цели (Cloudflare R2, Codeberg-зеркало) — этап 2 INFRA-032.
./AGENTS.md:599:- PDF и медиа-паспорта загружены в R2 бакет blago-nko-backups
./docs/backup/backup-plan.yaml:11:  - id: r2
./docs/backup/backup-plan.yaml:14:    secrets_needed: [R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET]
./docs/backup/RESTORE.md:16:## Источник 2: Cloudflare R2 (этап 2)
./docs/backup/RESTORE.md:18:    aws s3 cp s3://<R2_BUCKET>/manifests-<DATE>.tar.gz . \
./docs/backup/RESTORE.md:19:      --endpoint-url=https://<account>.r2.cloudflarestorage.com
./docs/backup/RESTORE.md:21:Требуется: secrets `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET`.
./docs/migration/PILOT-checklist.md:35:- [ ] 301-редиректы настроены (Cloudflare Page Rules)
./docs/migration/STRATEGY.md:8:2. Единый деплой через GitHub Pages + Cloudflare DNS.
./docs/migration/STRATEGY.md:62:- Cloudflare DNS → GitHub Pages по каждому сайту.
./docs/migration/STRATEGY.md:79:- Формы без ПДн → Formspree или Cloudflare Workers.
./docs/migration/STRATEGY.md:112:- Невоспроизводимые пути → 301 правилами Cloudflare (список ведёт url_mapping.py).
./docs/migration/SUMKA-MAPPING.md:75:| 7.3 Эволюционная модель хранения медиа | R2/YOS для медиа >5MB (hot/cold storage) | scripts/media_storage.py | Фаза 4 | ⬜ |
./docs/migration/SUMKA-MAPPING.md:113:- **R2 Usage:** Только для PDF-документов и медиа-паспортов (`media_passport.json.gz`).
./docs_audit_summary.md:62:Поиск терминов: r2, cloudflare, cdn.obrazslov, object storage
./domains-graph.yaml:107:  - fqdn: r2.blagorussia.ru
./ROADMAP.md:23:- Медиа-пайплайн: загрузка → sanitize → R2 → CDN URL
./TASKS.md:74:| **INFRA-020** | Наполнение таксономии domains-graph, уточнение ролей хаба и r2 | общие категории и подтаксономии по 016.2 | 🟠 | 🤖→ | ⬜ | После INFRA-001 |
./TASKS.md:83:| **INFRA-032** | Бэкапы ключевых файлов + runbook восстановления | weekly-backup в ветку backups; R2 и зеркало — этап 2 | 🟡 | → | 🔄 | Этап 1: workflow + runbook |
./TASKS.md:104:| **INFRA-110** | Конфиг `image_storage_routing.json` в shared-assets | Маршрутизация типов файлов (Blogger/R2/Git) | 🟡 HIGH | → | ⬜ | Единый источник правил хранения |
./TASKS.md:138:| **MIG-015** | Спасение контента 11 RSS | Перепарсинг живых Blogger-сайтов, бэкап в R2/YOS (0 ₽) | 🟠 | 🤖→👤 | ⬜ | Пока контент жив |
./TASKS.md:215:| `migrate_blogger_to_r2.py` | САМ/СУМКа | ❌ Отсутствует | MIG-010 | ✅ Да |
./ГРЕК-ПАНТЕОН.md:44:- **Этап 2 (MVP и замещение на целевой движок):** После успешного переезда всей экосистемы, статическая версия постепенно замещается полноценной версией на **Astro + Yandex Object Storage** (Parquet + DuckDB) с использованием архитектуры островов (Islands Architecture). ИИ-конвейер генерирует 16 505+ страниц.
./ГРЕК-ПАНТЕОН.md:45:- **Этап 3 (Масштабирование):** Оптимизация производительности, переход на PostgreSQL при превышении лимитов Yandex Object Storage, расширение геоинформационного слоя.
./ГРЕК-ПАНТЕОН.md:61:- **Структура данных:** Parquet-файлы в Yandex Object Storage (S3-совместимое хранилище) + обработка через DuckDB (in-memory OLAP).
./ГРЕК-ПАНТЕОН.md:63:- **Партиционирование данных:** Parquet-файлы в Yandex Object Storage обязаны быть партиционированы (например, по алфавитным группам или категориям персонажей). Это архитектурное требование для обеспечения работы *predicate pushdown* в DuckDB и предотвращения полного сканирования датасета при росте базы до 16 505+ страниц.
./ГРЕК-ПАНТЕОН.md:179:1. **ETL-конвейер:** Скрипт `grekpanteon_pipeline.py` выгружает данные из Google Sheets в Parquet-файлы (Yandex Object Storage).
./ГРЕК-ПАНТЕОН.md:451:- Cloudflare R2 используется только для PDF-документов (если есть) и медиа-паспортов.
./ГРЕК-ПАНТЕОН.md:458:- Защита от vendor lock-in обеспечивается скриптом `migrate_blogger_to_r2.py` и еженедельным бэкапом метаданных в `shared-assets/blogger_image_metadata.json` (Git).
./ГРЕК-ПАНТЕОН.md:504:- `scripts/migrate_blogger_to_r2.py` – скрипт аварийной миграции
./ГРЕК-ПАНТЕОН.md:521:| САМ | Принцип «Эволюционная модель хранения» | Blogger (основное безлимитное хранилище) + Cloudflare R2 (исключительно как резервный архив для PDF и бэкапов) |
./ЛИЦ.md:51:- `migrate_backups_to_r2.py` — перенос backup/feed.xml в Cloudflare R2
./ЛИЦ.md:65:- `backup-r2.yml` — автоматический бэкап в R2
./МИГРАЦИЯ.md:29:- **Этап 2 (MVP и замещение на целевые движки):** После успешного переезда всей экосистемы, `grekpanteon.obrazslov.ru` постепенно замещается на полноценную версию на Astro + Yandex Object Storage (16 505+ страниц, ИИ-конвейер), а `can.blagorussia.ru` — на платформу САН на Next.js с Supabase и всеми сервисами.
./МИГРАЦИЯ.md:90:- **Видео-инфраструктура** – отказ от R2, мульти-загрузка на внешние платформы, Видео-Матрица РФ, двойное зеркалирование, Единый Видео-Реестр.
./МИГРАЦИЯ.md:235:4. Загрузка обработанных изображений в Blogger (основное хранилище) с заменой URL; PDF и `media_passport.json.gz` загружаются в Cloudflare R2 (согласно САМ п. 2.4).
./МИГРАЦИЯ.md:350:Общесистемные артефакты (`video_alternatives_db.json`, `identity_graph.json`, `image_sanitizer.py`, `generate_sitemaps.py`, `ping_search_engines.py`, `verification.json`, `migrate_blogger_to_r2.py`, `blogger_image_metadata.json`, `backup_blogger_metadata.yml`, `image_storage_routing.json`, `STATUS.md`, `update-status.yml`, `shared-assets` полностью, Политика конфиденциальности) перечислены в САМ.
./МИГРАЦИЯ.md:392:**Целевой стек хранения данных для Этапа 2:** Parquet-файлы в Yandex Object Storage + обработка через DuckDB.
./МИГРАЦИЯ.md:451:- Скрипт `migrate_blogger_to_r2.py` — аварийная миграция
./МИГРАЦИЯ.md:453:- Альтернативный план: при закрытии Blogger → автоматический запуск скрипта → переключение DNS на R2-зеркало
./МИГРАЦИЯ.md:516:- **`grekpanteon.obrazslov.ru`** постепенно замещается на полноценную версию на **Astro + Yandex Object Storage** (Parquet + DuckDB) с ИИ-конвейером генерации 16 505+ страниц.
./МИГРАЦИЯ.md:525:| 2. Подготовка и Прототипирование | СУМКа работает в штатном режиме, распределяя контент по площадкам. | Решение Арх. Комитета: Утверждение перехода на Astro. <br> Разработка: Настройка Astro, Parquet + Yandex Object Storage + DuckDB, Leaflet (карты) и ИИ-конвейера (Gemini). | Этап -1 (Прототип): Проектирование реляционного ядра, парсинг данных, работа через Google Sheets / Supabase Free. Ручные тестовые объекты вносятся и мигрируют в боевую БД на этом этапе. |
./МИГРАЦИЯ.md:543:- **ГРЕК-ПАНТЕОН:** Оптимизация производительности, переход на PostgreSQL при превышении лимитов Yandex Object Storage, расширение геоинформационного слоя.
./МИГРАЦИЯ.md:641:- Cloudflare R2: 10 ГБ (только для PDF и медиа-паспортов)
./МИГРАЦИЯ.md:685:- `scripts/migrate_blogger_to_r2.py` – аварийная миграция
./МИГРАЦИЯ.md:765:- Настройка R2/S3 для хранения медиа
./МИГРАЦИЯ.md:769:- Настройка Cloudflare для DNS и CDN
./МИГРАЦИЯ.md:803:  - **Митигация**: Cloudflare CDN + кэширование
./МИГРАЦИЯ.md:825:- Интеграция с R2 для хранения медиа
```

## 📄 Секция 3: Полный список целевых файлов (.md/.yaml)
Ниже перечислены все файлы документации и манифестов. Их нужно просмотреть на предмет противоречий.
```text
./.github/ISSUE_TEMPLATE/bug_report.md
./.github/ISSUE_TEMPLATE/config.yml
./.github/ISSUE_TEMPLATE/feature_request.md
./.github/PULL_REQUEST_TEMPLATE.md
./.github/workflows/apply-architecture-patches.yml
./.github/workflows/architecture-check.yml
./.github/workflows/backup-ecosystem.yml
./.github/workflows/license-check.yml
./.github/workflows/manifest-consistency-check.yml
./.github/workflows/manifest-lint.yml
./.github/workflows/markdown-lint.yml
./.github/workflows/pr-prefix-check.yml
./.github/workflows/readme-license-check.yml
./.github/workflows/sync-manifests.yml
./.github/workflows/sync-readme-sections.yml
./.github/workflows/tests.yml
./.github/workflows/update-status.yml
./.markdownlint.yaml
./.pytest_cache/README.md
./AGENTS.md
./CHANGELOG.md
./CODE_OF_CONDUCT.md
./CONTRIBUTING.md
./README.md
./ROADMAP.md
./SECURITY.md
./TASKS.md
./docs/STATUS.md
./docs/backup/RESTORE.md
./docs/backup/backup-plan.yaml
./docs/domains-list.md
./docs/manifests.yaml
./docs/migration/DATA_VALIDATION_RULES.md
./docs/migration/PILOT-checklist.md
./docs/migration/STRATEGY.md
./docs/migration/SUMKA-MAPPING.md
./docs/migration/THEME-BOUNDARY.md
./docs_audit_summary.md
./domains-graph.yaml
./ГРЕК-ПАНТЕОН.md
./ЛИЦ.md
./МИГРАЦИЯ.md
./САМ.md
./САН.md
./СУМКа.md
```
