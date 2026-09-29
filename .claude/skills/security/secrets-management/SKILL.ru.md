---
name: secrets-management
description: "Manage secrets safely: vaults, rotation, environment variables, scanning, and least privilege. Use for protecting credentials and keys."
category: security
tags: [secrets-management, security, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: secrets-management
author: ssrjkk
---
# Secrets Management (Управление секретами)

> Безопасное хранение и ротация секретов.

## Быстрый старт
```bash
# Никогда не коммитьте секреты в git
# Используйте vault или переменные окружения
export API_KEY="..."
```

## Когда использовать
- Любое приложение с кредами или ключами
- CI/CD, которому нужны секреты
- Мультисервисные окружения
- Комплаенс (PCI, HIPAA)

## Лучшие практики

### Хранение
- Vault (HashiCorp Vault, cloud KMS)
- Managed secret managers в облаке
- Секреты вне конфигов и образов
- Минимум — переменные окружения

### Ротация
- По расписанию или при инциденте
- Автоматизация где возможно
- Ротация без downtime
- Немедленный revoke скомпрометированных

### Сканирование
- Сканы репо и образов на утечки
- Блокировка секретов в git pre-commit (gitleaks)
- Алерты на экспозицию
- Ротация найденного в сканах

### Least privilege
- Минимальный доступ на сервис
- Скоуп ключей на ресурсы
- Короткоживущие креды
- Аудит доступа к секретам

## Зависимости
```bash
# gitleaks для сканирования git
go install github.com/gitleaks/gitleaks@latest
# или: pip install detect-secrets
```

## Примеры
```bash
# Запуск gitleaks для поиска секретов
gitleaks detect --source . -v
```
```python
# Загрузка секретов из env (никогда не хардкодить)
import os

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY not set")
```
```yaml
# Использование секретов GitHub Actions
name: Deploy
on: [push]
jobs:
  deploy:
    steps:
      - run: ./deploy.sh
        env:
          API_KEY: ${{ secrets.API_KEY }}
```
```bash
# Получение из vault (псевдо)
vault read secret/api_key
# или облако: gcloud secrets versions access latest --secret=api-key
```

## Пошаговое руководство
1. Аудит текущих секретов и их хранения.
2. Перенесите секреты в vault или env-переменные.
3. Уберите секреты из конфигов и истории.
4. Настройте pre-commit сканирование (gitleaks).
5. Ротируйте секреты и ревокайте раскрытые.
6. Минимальные права на сервис.
7. Автоматизируйте ротацию где возможно.
8. Мониторьте и аудируйте доступ.

## Валидация
1. Нет секретов в git-истории или репо
2. Секреты только из vault/env
3. Ротация без downtime
4. Сканирование в CI
5. Доступ скоуплен и аудируется

## Устранение неполадок
- Утёкший секрет: немедленно revoke и ротация.
- Простой при ротации: перекрывающиеся ключи.
- False positives сканов: аккуратные allowlists.