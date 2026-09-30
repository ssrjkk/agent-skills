---
name: platform-engineering
description: "Platform engineering with Backstage/Port"
category: devops
tags: [platform-engineering, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: platform-engineering
---
# Platform Engineering

> Стройте внутренние developer-платформы на Backstage и Port для удобных процессов разработки.

## Быстрый старт
```yaml
# app-config.yaml — конфигурация Backstage
app:
  title: Internal Developer Platform
  baseUrl: https://developer.example.com

backend:
  baseUrl: https://developer.example.com
  listen: { port: 7007 }

organization:
  name: My Company

integrations:
  github:
    - host: github.com
      token: ${GITHUB_TOKEN}

techdocs:
  builder: 'local'
  generators:
    techdocs: 'docker'

catalog:
  rules:
    - allow: [Component, API, Resource, System, Domain]
  locations:
    - type: url
      target: https://github.com/org/service-catalog/blob/main/catalog-info.yaml
      rules:
        - allow: [Component, API]
```

```yaml
# catalog-info.yaml — определение сущности сервиса
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-service
  description: Payment processing service
  annotations:
    github.com/project-slug: org/payment-service
    backstage.io/techdocs-ref: dir:.
    jenkins.io/github-folder: org/payment-service
spec:
  type: service
  lifecycle: production
  owner: platform-team
  system: payment-platform
  dependsOn:
    - resource:default/postgres-main
    - api:default/payment-api
  providesApis: [payment-api]
  consumedApis: [fraud-detection-api]
```

## Ключевые концепции
Platform engineering рассматривает платформу как продукт. Backstage/Port дают service catalog, software templates, tech docs и scorecards. Golden paths снижают когнитивную нагрузку на разработчиков.

## Когда использовать
- Организации с 10+ микросервисами, которым нужна стандартизация
- Команды, тратящие слишком много времени на конфигурацию инфраструктуры
- Стандартизация деплоя и окружений
- Улучшение developer experience и сокращение onboarding

## Пошаговое руководство
1. Запустите developer-портал: скаффолд Backstage (`npx @backstage/create-app`) или blueprint в Port с полями метаданных сервиса.
2. Смоделируйте golden path: определите шаблоны сервисов (API, service, worker) через software templates / self-service actions Port.
3. Зарегистрируйте каталог: закоммитьте `catalog-info.yaml` для каждого сервиса с owner, system, зависимостями и API-границами.
4. Подключите CI/CD: настройте SCM-интеграцию и repository-backend события для авторегистрации новых репозиториев.
5. Опубликуйте документацию: включите TechDocs из markdown репозитория — живая документация из кода.
6. Добавьте governance: scorecards с проверками зрелости (покрытие SLO, обновление зависимостей, cost tags) и отчёты в портале.

## Примеры
```yaml
# catalog-info.yaml — полная сущность со связями
apiVersion: backstage.io/v1alpha1
kind: System
metadata:
  name: payment-platform
  description: Core payments system
spec:
  owner: platform-team
---
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-service
  annotations:
    github.com/project-slug: org/payment-service
    backstage.io/techdocs-ref: dir:.
spec:
  type: service
  lifecycle: production
  owner: platform-team
  system: payment-platform
  dependsOn:
    - resource:default/postgres-main
  providesApis: [payment-api]
  consumedApis: [fraud-detection-api]
```
```bash
# Добавьте сущность в catalog locations, затем запушьте для синхронизации
kubectl port-forward svc/backstage-backend 7007:7007
curl http://localhost:7007/api/catalog/entities?filter=kind=component
```

## Лучшие практики
- Golden paths с self-service шаблонами и guardrails.
- Backstage или Port для портала разработчика и каталога.
- Стандартизируйте CI/CD, окружения и секреты между командами.
- Меряйте принятие и фидбек; итерируйте платформу.
- Автоматизируйте провижининг через IaC и апрув-воркфлоу.
- Платформенные команды подотчётны через SLO на golden paths.

## Устранение неполадок
- Низкое принятие: снизьте трение и документируйте golden path.
- Дрейф: энфорсьте политики и шаблоны в CI.
- Проблемы доступа: аудит RBAC и ролей портала.
- Медленный онбординг: автоматизируйте скаффолдинг end to end.

## Валидация
1. Backstage/Port стартует и рендерит service catalog
2. Software templates создают репозитории с корректным скаффолдом
3. TechDocs рендерит документацию из репозиториев кода
4. Scorecards отслеживают метрики зрелости сервисов
