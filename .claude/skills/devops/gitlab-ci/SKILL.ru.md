---
name: gitlab-ci
description: "Configures GitLab CI/CD pipelines with stages, jobs, and GitLab Runner. Use for Git-native automation and deployment."
category: devops
tags: [gitlab-ci, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: gitlab-ci
---
# GitLab CI/CD

> Git-интегрированный CI/CD с мощной оркестрацией пайплайнов.

## Быстрый старт
```yaml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  image: node:20
  script:
    - npm ci
    - npm test

build:
  stage: build
  script:
    - npm run build
  artifacts:
    paths:
      - dist/
```

## Когда использовать
- Репозитории на GitLab
- Auto DevOps деплой
- Мультипроектные пайплайны
- Интеграция с Container Registry

## Лучшие практики
- Ясные имена jobs; одна задача на стадию.
- Кэшируйте зависимости и используйте `needs` для скорости.
- Секреты в CI/CD variables, masked и scoped.
- `rules` вместо only/except для триггеров по веткам.
- Загружайте артефакты и отчёты для видимости.
- Переиспользуйте логику через `include` и шаблоны.

## Пошаговое руководство
1. Добавьте `.gitlab-ci.yml` в корень репозитория
2. Настройте стадии и jobs
3. Настройте GitLab Runner
4. Запушьте, чтобы запустить пайплайн
5. Добавьте кэш и rules
6. Обезопасьте переменные и деплой

## Зависимости
```bash
# Локальный runner
gitlab-runner register
```

## Примеры
```yaml
# Job с кэшем и rules
test:
  stage: test
  image: node:20
  cache:
    key: npm
    paths: [node_modules/]
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  script:
    - npm ci
    - npm test
```
```yaml
# Переиспользуемый шаблон через include
include:
  - template: Security/SAST.gitlab-ci.yml
  - local: /ci/deploy.gitlab-ci.yml

deploy:
  stage: deploy
  image: docker:24
  services: [docker:24-dind]
  only:
    - main
  script:
    - docker build -t $CI_REGISTRY_IMAGE .
    - docker push $CI_REGISTRY_IMAGE
  environment: production
```

## Ресурсы
- [GitLab CI Docs](https://docs.gitlab.com/ee/ci)

## Устранение неполадок
- **Job завис в статусе pending** — у runner не совпали теги. Добавьте
  `tags: [docker]` в job или зарегистрируйте runner с нужными тегами.
- **Падение на `npm ci`** — устаревший кэш. Очистите кэш через
  *CI/CD → Pipelines → Run pipeline* или обновите `key` у кэша.
- **Deploy-стадия пропущена** — `only: [main]` блокирует ветки;
  используйте `rules: [if: '$CI_COMMIT_BRANCH == "main"']` для гибкости.
- **Runner работает на `sh`, а не `bash`** — задайте `image` каждому job
  или пишите POSIX-совместимые команды (`|| true`, без `set -o pipefail`).

## Валидация
1. Пайплайн стартует на коммит
2. Все стадии выполняются по порядку
3. Деплой проходит успешно
