# Стратегия миграции сайтов с Blogger на Hugo/Astro (INFRA-047)

> Документ описывает план миграции 14 сайтов с Blogger на Hugo и Astro.

## Цели

1. Уйти от vendor lock-in Blogger (контроль контента, деплоя, URL).
2. Единый деплой через GitHub Pages + Cloudflare DNS.
3. Общие ассеты (тема, компоненты, CSS/JS) через shared-assets как submodule.
4. Активировать INFRA-031 (uptime-мониторинг) после миграции — аптайм станет в нашем контуре.

## Матрица миграции (14 сайтов)

| # | Домен | Роль | Целевой движок | Комментарий |
| :-: | :------ | :----- | :--------------: | :------------ |
| 1 | <www.blagorussia.ru> | хаб сообществ | Hugo | Сложная навигация, 13 рубрик; apex → www редирект |
| 2 | obrazslov.ru | Образ слов (база знаний) | Hugo | Кандидат на пилот |
| 3 | partnerstvo.blagorussia.ru | Юридический хаб НП | Hugo | Секция «Документы»; ПДн-формы → Yandex Forms |
| 4 | novosti.blagorussia.ru | Новости | Hugo | Новостной поток |
| 5 | ot-gorozan.blagorussia.ru | Конкурс | Hugo | Медиа-контент; формы без ПДн |
| 6 | obavlenia.blagorussia.ru | Объявления | Hugo | Короткие посты |
| 7 | interesnye-mesta.obrazslov.ru | Наследие | Hugo | Архив |
| 8 | moisites.blagorussia.ru | Интернет-школа | Hugo | Обучающий контент |
| 9 | joga.blagorussia.ru | Йога | Hugo | Статьи + события |
| 10 | ideologia.obrazslov.ru | Идеология | Hugo | Тексты |
| 11 | nasa-istoria.blagorussia.ru | Наша история (архив памяти) | Hugo | ПДн-формы → Yandex Forms |
| 12 | grekpanteon.obrazslov.ru | Пантеон | Hugo | Биографии |
| 13 | gallery.obrazslov.ru | Фотоархив | Blogger | Хранение изображений в Blogger CDN (см. САМ п.2.4) |
| 14 | can.blagorussia.ru | САН | Hugo | Мигрирует вместе со всеми; изоляция контура B — после финальной проверки 14 сайтов (Этап 7) |

## Этапы

### Этап 1: Инструменты экспорта

- scripts/blogger_export.py — экспорт постов из Blogger API → YAML front matter + markdown.
- scripts/media_downloader.py — скачивание медиа из Blogger в локальный /static/images/.
- scripts/url_mapping.py — маппинг старых URL → новых (для 301-редиректов).

### Этап 2: Пилотная миграция (1 сайт)

Кандидаты: A — obrazslov.ru; B — nasa-istoria.blagorussia.ru; C — <www.blagorussia.ru>.

На пилоте:

1. Создание репозитория blago-nko/<сайт>.
2. Подключение shared-assets как submodule.
3. Перенос 10-20 постов с Blogger.
4. Реализация общих артефактов СУМКа (mobile-first layout, шапка, подвал, cookie, лицензия) как Hugo-partials в shared-assets.
5. Деплой в staging-ветку на GitHub Pages.
6. Сравнительная проверка: контент, URL, SEO, формы, артефакты.

### Этап 3: Серийная миграция (13 сайтов)

После успешного пилота — остальные 13 сайтов по отработанному сценарию, включая can.blagorussia.ru (САН).

### Этап 4: Astro-миграция (gallery)

Фото-галерея на Astro-компонентах из shared-assets.

### Этап 5: Переключение DNS + мониторинг

- Cloudflare DNS → GitHub Pages по каждому сайту.
- 301-редиректы со старых Blogger-URL; apex-редирект на www.
- Активация INFRA-031 (uptime-мониторинг).

### Этап 6: Финальная проверка всех 14 сайтов

Чек-лист 48 часов: контент, URL, SEO, формы (ПДн на Yandex Forms), артефакты СУМКа, uptime.

### Этап 7: Изоляция контура B (INFRA-035)

Перенос can.blagorussia.ru на отдельный аккаунт — только после успешного Этапа 6.

## Дизайн-решения

### Интерактивные элементы и формы

- Комментарии Blogger → Giscus либо отключаются с экспортом архива в markdown.
- Формы без ПДн → Formspree или Cloudflare Workers.
- Конкурсные формы ot-gorozan → embed Google Forms (без ПДн), собственный бэкенд в Фазе 4.
- Видео YouTube → Hugo-шорткод youtube.
- Поиск по сайту → Pagefind (статический индекс).

### Формы с персональными данными (152-ФЗ)

- Google Forms с ПДн на partnerstvo и nasa-istoria неприемлемы (иностранный обработчик).
- Миграция на Yandex Forms (инфраструктура РФ) или self-hosted форму на РФ-хостинге; embed через iframe.
- Архив старых ответов выгружается до отключения; Google Forms отключаются до переключения DNS.
- Согласие на обработку ПДн публикуется рядом с формой.

### Ярлыки, рубрики, SEO

- Ярлыки Blogger → Hugo tags; рубрики → categories; таблица соответствия в конфиге миграции.
- Meta-описания → front matter description; sitemap.xml и robots.txt генерирует Hugo.
- OG и Twitter-карты → partial из shared-assets.

### Главная страница (единый шаблон)

1. Шапка: логотип, навигация по рубрикам, поиск.
2. Hero-блок: миссия сайта и ключевое действие.
3. Лента последних постов карточками.
4. Блоки 3-6 ключевых рубрик.
5. Блок «Экосистема»: ссылки на смежные домены.
6. Футер: лицензионный блок, контакты, триггер CookieConsent.

Хаб <www.blagorussia.ru> — агрегатор лент сайтов и навигатор рубрик.

### Адреса страниц (URL)

- Сохраняем схему Blogger ради SEO: /YYYY/MM/slug.html через Hugo permalinks.
- Статические страницы /p/slug.html через aliases.
- Невоспроизводимые пути → 301 правилами Cloudflare (список ведёт url_mapping.py).

Пример конфигурации permalinks:

    [permalinks]
      posts = "/:year/:month/:filename.html"

### Общие артефакты СУМКа (минимальный набор всех 14 сайтов)

- Mobile-first layout: baseof.html (Hugo) / layout-компонент (Astro) + CSS breakpoints 360/768/1024.
- Шапка и подвал: partials header.html, footer.html (+ Astro-компоненты).
- CookieConsent.js + стили баннера.
- Футер-лицензия CC BY-NC 4.0 со ссылкой на LICENSE-CONTENT.
- Блок «Об экосистеме» со ссылками на 14 доменов.
- Favicon и OG-изображения; RSS index.xml, sitemap.xml, robots.txt.
- Meta-тег верификации Search Console.

Реестр соответствия артефактов СУМКа → реализация ведётся в docs/migration/SUMKA-MAPPING.md (создаётся отдельным PR INFRA-050 после дампа СУМКа.md).

## Риски и митигация

| Риск | Вероятность | Влияние | Митигация |
| :----- | :-----------: | :-------: | :---------- |
| Потеря SEO-трафика при смене URL | Средняя | Высокое | 301-редиректы + сохранение slug |
| Потеря изображений из Blogger | Средняя | Среднее | media_downloader.py + backup перед удалением |
| Несовместимость разметки (HTML → markdown) | Высокая | Среднее | Ручная правка сложных постов на пилоте |
| Простои при переключении DNS | Низкая | Высокое | Staging-прогон + мониторинг 48 часов |
| Blogger API rate limits | Средняя | Низкое | Batch-экспорт с паузами, кэш |
| 152-ФЗ при хранении ПДн за рубежом | Высокая | Высокое | Yandex Forms вместо Google Forms |

## Связи с другими задачами

- INFRA-031 — активируется после Этапа 5.
- INFRA-032 — полный архив Blogger-контента перед переключением DNS.
- INFRA-033 — shared-assets используется всеми мигрированными сайтами.
- INFRA-035 — Этап 7, после финальной проверки 14 сайтов.
- INFRA-049 — apex TLS blagorussia.ru: настроить редирект на www; не отказ, www валиден.

---

*Последнее обновление: 2026-09-18*
