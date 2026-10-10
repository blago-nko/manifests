> ⚠️ **ВАЖНО: ЭТА ЗАДАЧА ОТЛОЖЕНА (PHASE 2)**
>
> Настройка Cloudflare R2 требуется только ПОСЛЕ завершения основной миграции 13 сайтов на Hugo.
> Сейчас приоритетна задача **MIG-CORE-EXECUTE** (парсинг Blogger API).
> Не выполняйте шаги из этого руководства, пока не будет закрыта фаза миграции контента.


# Инструкция по настройке Cloudflare R2 Object Storage

## 1. Создание Bucketa

1. Войдите в [Cloudflare Dashboard](https://dash.cloudflare.com/).
2. Перейдите в раздел **R2 Object Storage** (в левой боковой панели).
3. Нажмите кнопку **Create Bucket**.
4. Имя бакета: `obrazslov-media`.
5. Регион: Выберите ближайший к вашей аудитории (например, Europe или US-East). Для России оптимально Europe (Франкфурт/Амстердам).
6. Нажмите **Create Bucket**.

## 2. Привязка Домена (Public Access / Custom Domain)

Чтобы файлы были доступны по красивому адресу `cdn.obrazslov.ru`, а не длинным URL от Cloudflare:

1. Откройте созданный бакет `obrazslov-media`.
2. Перейдите во вкладку **Settings** -> **Custom Domains**.
3. Нажмите **Add Custom Domain**.
4. Введите домен: `cdn.obrazslov.ru`.
5. Cloudflare предложит добавить DNS запись (CNAME). Если ваш DNS управляется через тот же аккаунт Cloudflare, подтвердите автоматически. Если нет — скопируйте значения CNAME и добавьте их у своего регистратора.
6. Дождитесь активации SSL сертификата (обычно занимает 1-5 минут).
7. После успешной проверки статус изменится на **Active**.

## 3. Получение API Keys (S3-Compatible Access)

Для работы Python-скриптов и CI/CD пайплайнов нам нужны ключи доступа S3.

1. В главном меню Cloudflare перейдите в **Account Details** -> **API Tokens**.
2. Нажмите **Create Token**.
3. Используйте шаблон **Start from Template** -> выберите **Cloudflare R2 Edit**.
4. Настройте права доступа:
   * **Permissions:** Account | Cloudflare R2 storage | Read and Write
   * **Resources:** Specific account selected (ваш аккаунт ID)
5. Нажмите **Continue to summary** -> **Create Token**.
6. Скопируйте полученные значения:
   * `Access Key ID`
   * `Secret Access Key`
   * `Endpoint URL` (выглядит как `https://<account_id>.r2.cloudflarestorage.com`)

⚠️ **Важно:** Сохраните эти ключи в переменных окружения (`.env`) или секретах GitHub Actions. Никогда не коммитьте их в Git!

## 4. Настройка CORS (Cross-Origin Resource Sharing)

Чтобы изображения корректно отображались на сайтах `*.obrazslov.ru`:

1. В настройках бакета найдите раздел **Settings** -> **CORS Policies**.
2. Добавьте новую политику:

```json
[
  {
    "AllowedOrigins": ["https://obrazslov.ru", "https://*.obrazslov.ru"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedHeaders": ["*"],
    "ExposeHeaders": [],
    "MaxAgeSeconds": 3000
  }
]
