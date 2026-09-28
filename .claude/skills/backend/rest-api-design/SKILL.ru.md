---
name: rest-api-design
description: "Design consistent REST APIs: resource modeling, status codes, pagination, versioning, error contracts, and documentation. Use for any API design task."
category: backend
tags: [rest-api-design, backend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: rest-api-design
author: ssrjkk
---
# REST API Design (Проектирование REST API)

> Проектирование консистентных, эволюционируемых REST API.

## Быстрый старт
```text
Ресурсы:   /users, /users/{id}, /users/{id}/orders
Методы:    GET list/detail, POST create, PUT replace, PATCH partial, DELETE
Статусы:   200, 201, 204, 400, 401, 403, 404, 409, 422, 429, 500
```

## Когда использовать
- Публичные или внутренние HTTP API
- Проектирование до реализации
- Версионирование и эволюция существующих API
- SDK и клиенты, потребляющие API

## Лучшие практики

### Ресурсы
- Моделируйте существительные как ресурсы, действия — как подресурсы
- Множественное число: `/users`, а не `/user`
- Вложенность только при реальном владении: `/users/{id}/orders`
- Связи — через ID, а не вложенные объекты

### Методы и статусы
- Используйте HTTP-методы по назначению (GET/POST/PUT/PATCH/DELETE)
- 201 с Location при создании, 204 при удалении
- 422 для валидации, 409 для конфликтов
- Ошибки единообразно: code, message, details

### Пагинация и фильтрация
- Пагинация списков: page/limit или cursor
- Cursor-based для стабильности
- Фильтрация через query-параметры, не через пути
- Сортировка через явный `sort`

### Версионирование и эволюция
- Версионируйте API: префикс URL или заголовок
- Аддитивные изменения внутри версии
- Deprecate с заголовками и уведомлениями
- Документируйте всё в OpenAPI

## Зависимости
```bash
# Инструменты дизайна/документации
npm i -D @redocly/cli
# или Python
pip install openapi-spec-validator
```

## Примеры
```yaml
# OpenAPI минимальный ресурс user
openapi: 3.1.0
info:
  title: Users API
  version: v1
paths:
  /users:
    get:
      parameters:
        - name: limit
          in: query
          schema: { type: integer, maximum: 100 }
      responses:
        "200":
          description: Paginated users
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UserInput"
      responses:
        "201":
          description: Created
```
```json
// Единый контракт ошибок
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request body",
    "details": [{ "field": "email", "reason": "must be a valid email" }],
    "request_id": "req_abc123"
  }
}
```
```text
// Форма пагинации
GET /users?limit=25&cursor=eyJpZCI6MTAwfQ

{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTI1fQ",
    "has_more": true
  }
}
```
```python
# Пример маршрутизации
# GET /v1/users -> list
# POST /v1/users -> create
# GET /v1/users/{id} -> detail
# PATCH /v1/users/{id} -> partial update
# DELETE /v1/users/{id} -> 204
```

## Пошаговое руководство
1. Определите ресурсы и их связи из домена.
2. Задайте эндпоинты с корректными методами и путями.
3. Опишите схемы запросов/ответов и статус-коды.
4. Добавьте пагинацию, фильтрацию и сортировку в списки.
5. Создайте единый контракт ошибок.
6. Определите стратегию версионирования заранее.
7. Напишите OpenAPI-спеку и провалидируйте.
8. Сгенерируйте доки и SDK из спеки.

## Валидация
1. Все пути следуют конвенции именования ресурсов
2. Статус-коды соответствуют семантике HTTP
3. Ошибки имеют единую форму
4. Списки пагинированы со стабильным курсором
5. OpenAPI-спека валидна и полностью документирована

## Устранение неполадок
- Слишком вложенные пути: упрощайте, если нет реального владения.
- Несогласованные ошибки: централизуйте маппинг ошибок.
- Breaking changes: бампайте версию вместо смены семантики.