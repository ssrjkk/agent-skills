---
name: fastapi
description: "Build high-performance Python APIs with FastAPI: routing, Pydantic validation, async, dependency injection, OpenAPI, and testing. Use for any Python backend."
category: backend
tags: [fastapi, backend, russian]
models: [sonnet, opus]
version: "1.0"
author: ssrjkk
language: ru
original: fastapi
---
# FastAPI (ФастАПИ)

> Высокопроизводительный Python-фреймворк для API с автоматической OpenAPI-документацией.

## Быстрый старт
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
# http://localhost:8000/docs  (Swagger UI)
```

## Когда использовать
- REST или async API на Python
- Микросервисы и serverless-обработчики
- Проекты, которым нужны валидация, типизированные контракты и OpenAPI-схема
- Async-нагрузки (HTTP-клиенты, WebSockets, фоновые задачи)

## Лучшие практики

### Структура
- Организуйте по фичам: `routers/`, `schemas/`, `services/`, `models/`
- Используйте APIRouter на ресурс; подключайте их в приложение
- Держите бизнес-логику в сервисах, а не в обработчиках маршрутов
- Выносите Pydantic-схемы в отдельный модуль

### Валидация и типы
- Определяйте модели запросов/ответов через Pydantic
- Используйте `Depends` для общей логики (auth, сессии БД)
- Задавайте `response_model` на каждом эндпоинте
- Предпочитайте `Annotated`-зависимости для читаемости

### Async
- Используйте `async def` для I/O-bound эндпоинтов
- Для БД предпочитайте async SQLAlchemy/asyncpg
- Выносите CPU-bound работу в threadpool (`run_in_executor`)
- Избегайте блокирующих вызовов в event loop

## Зависимости
```bash
pip install fastapi uvicorn[standard] pydantic
pip install -D pytest httpx pytest-asyncio
```

## Примеры
```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated

app = FastAPI(title="Items API")

class Item(BaseModel):
    name: str
    price: float

class ItemOut(BaseModel):
    id: int
    name: str
    price: float

def get_session():
    # инжектируемая зависимость
    yield {"conn": "pool"}

@app.post("/items", response_model=ItemOut, status_code=201)
async def create_item(item: Item, session: Annotated[dict, Depends(get_session)]):
    return ItemOut(id=1, **item.model_dump())
```
```python
# Паттерн роутера
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}")
async def get_user(user_id: int):
    if user_id < 0:
        raise HTTPException(status_code=400, detail="Invalid id")
    return {"id": user_id}
```
```python
# Async БД через asyncpg
import asyncpg
from fastapi import Depends

async def get_pool():
    pool = await asyncpg.create_pool(dsn="postgres://localhost/app")
    try:
        yield pool
    finally:
        await pool.close()
```
```python
# Фоновая задача
from fastapi import BackgroundTasks

async def send_email(email: str):
    pass  # отправка в фоне

@app.post("/notify")
async def notify(email: str, bg: BackgroundTasks):
    bg.add_task(send_email, email)
    return {"ok": True}
```

## Пошаговое руководство
1. Скаффолд: создайте `main.py` с FastAPI-приложением и импортируйте роутеры.
2. Определите Pydantic-схемы для каждой модели запроса и ответа.
3. Пишите обработчики с `response_model` и корректными статус-кодами.
4. Добавьте зависимости (`Depends`) для auth, сессий БД и настроек.
5. Используйте async-обработчики и async-драйверы БД для конкурентности.
6. Добавьте exception handlers для единообразных ошибок.
7. Пишите тесты на `httpx` + `pytest`; переопределяйте зависимости для изоляции.
8. Валидируйте OpenAPI-схему в CI; фиксируйте зависимости.

## Валидация
1. `uvicorn main:app` стартует чисто
2. `/docs` отображает схемы с корректными типами
3. `pytest` проходит (юнит + интеграция с TestClient)
4. Невалидный ввод возвращает 422 с деталями Pydantic
5. Модели ответов совпадают с объявленными схемами

## Устранение неполадок
- 422 на валидном вводе: проверьте типы полей Pydantic против JSON.
- Медленные async-эндпоинты: ищите блокирующие sync-вызовы в `async def`.
- Циклические импорты: выносите схемы в общий модуль.