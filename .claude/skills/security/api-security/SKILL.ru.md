---
name: api-security
description: "Secure web APIs: authentication, authorization, rate limiting, input validation, and abuse protection. Use for hardening any API."
category: security
tags: [api-security, security, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: api-security
author: ssrjkk
---
# API Security (Безопасность API)

> Укрепление API против типовых угроз.

## Быстрый старт
```text
1. Аутентифицируйте каждый запрос
2. Авторизуйте каждое действие
3. Валидируйте весь ввод
4. Rate-limit злоупотребления
```

## Когда использовать
- Публичные и внутренние API
- Auth, платежи и эндпоинты данных
- Любой API, доступный недоверенным клиентам
- Ревью безопасности перед релизом

## Лучшие практики

### Аутентификация
- Проверенная схема (OAuth2, API keys, JWT)
- Никакой самописной криптографии
- Токены захешированы, с expiry
- Ротация ключей

### Авторизация
- Проверка прав на каждом эндпоинте
- Минимальные scopes
- Не доверяйте claims клиента сами по себе
- Проверки владения

### Валидация ввода
- Типы, длины и диапазоны
- Параметризация всех запросов
- Отклонение лишних полей
- Лимиты размера пейлоадов

### Защита от злоупотреблений
- Rate limit на пользователя/IP/ключ
- Квоты на эндпоинт
- Детекция и блокировка аномалий
- Консистентные ошибки

## Зависимости
```bash
# язык-агностик; используйте security middleware фреймворка
```

## Примеры
```python
# Rate limiting (псевдо)
def rate_limit(key: str, limit: int, window: int) -> bool:
    count = redis.incr(f"rl:{key}")
    if count == 1:
        redis.expire(f"rl:{key}", window)
    return count <= limit

@app.route("/api/login", methods=["POST"])
def login():
    if not rate_limit(request.remote_addr, limit=10, window=60):
        return jsonify({"error": "rate_limited"}), 429
    ...
```
```python
# Валидация ввода
from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    def _strong(cls, v):
        if not re.search(r"[A-Za-z]", v) or not re.search(r"\d", v):
            raise ValueError("password needs letters and digits")
        return v
```
```python
# Проверка владения
def get_order(user_id: int, order_id: int):
    order = db.get_order(order_id)
    if order is None or order.user_id != user_id:
        raise NotFound("order")  # без утечки информации
    return order
```
```python
# Консистентные ошибки
def error(code: str, status: int):
    return jsonify({"error": {"code": code, "status": status}}), status
```

## Пошаговое руководство
1. Аутентифицируйте все эндпоинты (кроме public health).
2. Авторизация на каждый ресурс и действие.
3. Валидируйте каждый ввод схемами.
4. Параметризуйте запросы; отклоняйте лишние поля.
5. Rate-limit на пользователя/IP и эндпоинт.
6. Лимиты пейлоадов и ответов.
7. Консистентные минимальные ошибки.
8. Ревью безопасности перед релизом.

## Валидация
1. Неаутентифицированные запросы отклоняются
2. Неавторизованные действия запрещены
3. Невалидный ввод возвращает 400/422
4. Rate limits срабатывают при злоупотреблении
5. Ошибки не утекают внутренности

## Устранение неполадок
- Обход auth: убедитесь, что проверки на каждом эндпоинте.
- Энумерация: общие ошибки для not-found vs forbidden.
- Злоупотребления: настройте rate limits и добавьте детекцию аномалий.