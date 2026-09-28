---
name: docker
description: "Containerize applications with Docker: Dockerfiles, images, networking, volumes, compose, and production hardening. Use for any deployable service."
category: devops
tags: [docker, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: docker
author: ssrjkk
---
# Docker (Докер)

> Контейнеризация приложений через Docker для консистентного деплоя.

## Быстрый старт
```bash
docker build -t myapp .
docker run -p 8080:8080 myapp
docker compose up -d
```

## Когда использовать
- Консистентные окружения между dev, test и prod
- Микросервисы и изолированные зависимости
- CI/CD артефакты, одинаковые везде
- Локальная разработка с базами данных и сервисами

## Лучшие практики

### Dockerfile
- Используйте multi-stage сборки для лёгких образов
- Предпочитайте официальные и закреплённые базовые образы (`alpine:3.20`)
- Запускайте от non-root; копируйте только нужное
- Порядок слоёв: зависимости сначала, код последним (лучше кэш)

### Образы
- Держите образы маленькими: distroless или alpine, если можно
- Тегируйте по SHA коммита и semver; избегайте `latest` в проде
- Сканируйте образы через `docker scout` или Trivy
- Используйте `--platform` для multi-arch сборок

### Рантайм
- Задавайте лимиты ресурсов (`--memory`, `--cpus`)
- Для персистентных данных используйте volumes
- Предпочитайте `init: true` или `tini` для переработки зомби
- Добавляйте healthcheck, чтобы оркестраторы управляли жизненным циклом

## Зависимости
```bash
# Docker Desktop или docker engine + compose plugin
docker --version
docker compose version
```

## Примеры
```dockerfile
# Multi-stage Node сборка
FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-alpine AS runtime
ENV NODE_ENV=production
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]
```
```yaml
# docker-compose.yml
services:
  web:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:8080/health"]
      interval: 10s
      retries: 3
  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
volumes:
  pgdata:
```
```bash
# Сборка и пуш с метаданными
docker build -t ghcr.io/org/myapp:${GITHUB_SHA} .
docker push ghcr.io/org/myapp:${GITHUB_SHA}
```
```bash
# Инспекция и отладка
docker exec -it myapp sh
docker logs --follow myapp
docker image prune -f
```

## Пошаговое руководство
1. Напишите multi-stage Dockerfile с закреплёнными базовыми образами.
2. Упорядочьте слои для эффективного кэша (зависимости до кода).
3. Запускайте от non-root; добавьте healthcheck.
4. Собирайте и тестируйте локально через `docker build` и `docker run`.
5. Соберите сервисы через Compose для локальной интеграции (app + db + cache).
6. Тегируйте образы по SHA коммита; пушите в registry.
7. Сканируйте на уязвимости перед деплоем.
8. Задайте лимиты ресурсов и настройте ротацию логов.

## Валидация
1. `docker build` проходит без предупреждений
2. `docker run` стартует и отвечает на healthcheck
3. Скан образа не показывает критических уязвимостей
4. Compose-стек стартует чисто через `docker compose up`
5. Non-root контейнер не может писать в защищённые пути

## Устранение неполадок
- "Cannot connect to the Docker daemon": запустите Docker Desktop/engine.
- Образ слишком большой: перейдите на multi-stage и более лёгкий базовый образ.
- "Address already in use": смените маппинг порта или остановите конфликтующий контейнер.