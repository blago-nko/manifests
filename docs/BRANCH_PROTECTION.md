# 🔒 Branch Protection Rules

## Описание

Все репозитории экосистемы blago-nko защищены правилами ветки `main`.

## Настроенные правила

### 1. Require status checks

- ✅ compliance-check
- ✅ readme-license-check

### 2. Enforce administrators

Применяется ко всем (включая владельцев).

### 3. No force pushes

❌ Запрещён `git push --force`.

### 4. Require pull request

✅ Все изменения должны проходить через Pull Request.

## Скрипт настройки

Расположение: `/workspaces/setup_branch_protection.sh`

## Дата

21 августа 2026 г.
