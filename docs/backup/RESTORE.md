# 🔄 Runbook восстановления из бэкапов

> Процедуры восстановления ключевых файлов экосистемы (INFRA-032).

## Источник 1: ветка backups (основной, автоматический)

Архивы: `backups/manifests-YYYY-MM-DD.tar.gz` в ветке `backups` (4 последних).

    git fetch origin backups
    git show backups:backups/manifests-2026-09-21.tar.gz > /tmp/restore.tar.gz
    tar -tzf /tmp/restore.tar.gz
    mkdir -p /tmp/restore-dir && tar -xzf /tmp/restore.tar.gz -C /tmp/restore-dir

Далее — перенести файлы в рабочую ветку и оформить PR как обычное изменение.

## Источник 2: Cloudflare R2 (этап 2)

    aws s3 cp s3://<R2_BUCKET>/manifests-<DATE>.tar.gz . \
      --endpoint-url=https://<account>.r2.cloudflarestorage.com

Требуется: secrets `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET`.

## Источник 3: Codeberg-зеркало (этап 2)

    git clone https://codeberg.org/<owner>/manifests.git mirror
    # взять файлы из mirror/main

## Проверка после восстановления

    python -c "import yaml; yaml.safe_load(open('docs/manifests.yaml',encoding='utf-8')); print('yaml OK')"
    python scripts/update_status.py
    git diff --stat

Завершить PR-ом с восстановленными файлами; в описании указать причину и дату бэкапа.

---

*Последнее обновление: 2026-09-17*
