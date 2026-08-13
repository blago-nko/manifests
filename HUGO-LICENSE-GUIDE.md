# Руководство по лицензированию Hugo-проектов

При создании Hugo-проектов в экосистеме blago-nko используйте следующую структуру.

## Структура репозитория

````text
web-example.ru/
├── LICENSE                    # MIT License (для всего кода)
├── LICENSE-CONTENT            # CC BY 4.0 (для контента)
├── README.md                  # С секцией лицензирования
├── hugo.toml                  # MIT
├── layouts/                   # MIT (шаблоны)
├── static/                    # MIT (статика)
├── assets/                    # MIT (CSS/JS)
├── .github/workflows/         # MIT (CI/CD)
└── content/                   # CC BY 4.0 (контент)
    ├── LICENSE                # Дополнительный файл CC BY 4.0
    └── posts/
        └── статьи.md
````

## Файл content/LICENSE

Создайте дополнительный файл `content/LICENSE` с текстом:

```text
Контент этого раздела лицензирован под Creative Commons Attribution-ShareAlike 4.0 International.

Copyright (c) 2026 НП «Общественное благополучие Воронежа»

Полный текст лицензии см. в файле LICENSE-CONTENT в корне репозитория.
```

## .gitattributes

Добавьте `.gitattributes` для маркировки типов файлов:

```gitattributes
# Код - MIT
*.go      linguist-language=Go
*.js      linguist-language=JavaScript
*.html    linguist-language=HTML
*.css     linguist-language=CSS

# Контент - CC BY 4.0
content/* linguist-detectable=false
```
