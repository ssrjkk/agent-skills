---
name: github-actions
description: "Automate CI/CD with GitHub Actions: workflows, jobs, matrices, caching, artifacts, and reusable workflows. Use for build, test, and deploy pipelines."
category: devops
tags: [github-actions, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: github-actions
author: ssrjkk
---
# GitHub Actions (ГитХаб Экшенс)

> Автоматизация build, test и deploy пайплайнов через GitHub Actions.

## Быстрый старт
```bash
# Добавьте .github/workflows/ci.yml и запушьте
# Workflow запускается автоматически при push/PR
```

## Когда использовать
- Запуск тестов и линтеров на каждом PR
- Сборка и публикация артефактов
- Деплой в облако, реестры и Pages
- Scheduled-задачи и обновление зависимостей

## Лучшие практики

### Дизайн workflow
- Разделяйте CI/CD на отдельные workflow или jobs
- Для порядка используйте `needs`; для комбо версий — `matrix`
- Кэшируйте зависимости (`actions/cache`) для скорости
- Секреты храните в repo/org secrets; никогда не в YAML

### Безопасность
- Пиньте версии действий (`@v4`) или SHA коммитов
- Используйте `permissions:` минимальный скоуп на job
- Санизируйте недоверенный ввод (PR из форков)
- Избегайте `pull_request_target`, если не работаете с секретами аккуратно

### Эффективность
- Триггерите только по релевантным путям (`on: push: paths:`)
- Используйте concurrency для отмены устаревших запусков
- Переиспользуйте workflow через `workflow_call`
- Загружайте артефакты только когда нужно

## Зависимости
```bash
# Ничего не нужно — на GitHub-hosted раннерах есть общие инструменты.
# Пиньте версии:
#   actions/checkout@v4, actions/setup-python@v5, actions/cache@v4
```

## Примеры
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: pytest tests/ -q
```
```yaml
# Деплой по тегу с permissions
name: Deploy

on:
  push:
    tags: ["v*"]

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "deploying ${{ github.ref_name }}"
        env:
          TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```
```yaml
# Переиспользуемый workflow
name: Quality
on:
  workflow_call:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run lint
```
```yaml
# Scheduled + кэш
name: Nightly

on:
  schedule:
    - cron: "0 2 * * *"

jobs:
  nightly:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ hashFiles('requirements.txt') }}
      - run: pip install -r requirements.txt
```

## Пошаговое руководство
1. Определите триггер (`on`) и разбивку на jobs.
2. Сделайте checkout кода и настройте рантайм языка.
3. Кэшируйте зависимости для скорости.
4. Запускайте lint, typecheck и тесты параллельно, где возможно.
5. Добавьте шаг сборки/публикации после успеха.
6. Добавьте job деплоя с `needs` и защитой environment.
7. Выставьте `permissions` минимально; секреты — в настройках репо.
8. Смотрите логи Actions; добавляйте status badges в README.

## Валидация
1. Workflow зелёный на push и PR
2. Matrix покрывает поддерживаемые версии
3. Артефакты/секреты используются корректно (без утечек в логи)
4. Кэш измеримо ускоряет запуски
5. Устаревшие запуски отменяются через concurrency

## Устранение неполадок
- "Permission denied" на push/deploy: проверьте `permissions` и скоуп токена.
- Секреты не найдены: определите их в настройках repo/org.
- Flaky запуски: пиньте версии действий и образы раннеров.