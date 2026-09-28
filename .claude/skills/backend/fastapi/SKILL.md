---
name: fastapi
description: "Build high-performance Python APIs with FastAPI: routing, Pydantic validation, async, dependency injection, OpenAPI, and testing. Use for any Python backend."
category: backend
tags: [fastapi, python, api, async, pydantic, openapi, backend]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
author: ssrjkk
created: 2026-09-20
updated: 2026-09-28
---
# FastAPI

> High-performance Python API framework with automatic OpenAPI docs.

## Quick Start
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
# http://localhost:8000/docs  (Swagger UI)
```

## When to Use
- REST or async APIs in Python
- Microservices and serverless handlers
- Projects needing validation, typed contracts, and OpenAPI schema
- Async workloads (HTTP clients, WebSockets, background tasks)

## Best Practices

### Structure
- Organize by feature: `routers/`, `schemas/`, `services/`, `models/`
- Use APIRouter per resource; include them in the app
- Keep business logic in services, not in route handlers
- Put Pydantic schemas in a dedicated module

### Validation & Types
- Define request/response models with Pydantic
- Use `Depends` for shared logic (auth, DB sessions)
- Set `response_model` on every endpoint
- Prefer `Annotated` dependencies for clarity

### Async
- Use `async def` for I/O-bound endpoints
- Prefer async SQLAlchemy/asyncpg for DB access
- Offload CPU-bound work to a threadpool (`run_in_executor`)
- Avoid blocking calls in the event loop

## Dependencies
```bash
pip install fastapi uvicorn[standard] pydantic
pip install -D pytest httpx pytest-asyncio
```

## Examples
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
    # injected dependency
    yield {"conn": "pool"}

@app.post("/items", response_model=ItemOut, status_code=201)
async def create_item(item: Item, session: Annotated[dict, Depends(get_session)]):
    return ItemOut(id=1, **item.model_dump())
```
```python
# Router pattern
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}")
async def get_user(user_id: int):
    if user_id < 0:
        raise HTTPException(status_code=400, detail="Invalid id")
    return {"id": user_id}
```
```python
# Async DB with asyncpg
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
# Background task
from fastapi import BackgroundTasks

async def send_email(email: str):
    pass  # send in background

@app.post("/notify")
async def notify(email: str, bg: BackgroundTasks):
    bg.add_task(send_email, email)
    return {"ok": True}
```

## Step-by-Step
1. Scaffold: create `main.py` with the FastAPI app and import routers.
2. Define Pydantic schemas for every request and response model.
3. Write route handlers with `response_model` and correct status codes.
4. Add dependencies (`Depends`) for auth, DB sessions, and settings.
5. Use async handlers and async DB drivers for concurrency.
6. Add exception handlers for consistent error responses.
7. Write tests with `httpx` + `pytest`; override dependencies for isolation.
8. Validate the generated OpenAPI schema in CI; lock your dependencies.

## Validation
1. `uvicorn main:app` starts cleanly
2. `/docs` renders schemas with correct types
3. `pytest` passes (unit + integration with TestClient)
4. Invalid input returns 422 with Pydantic details
5. Response models match declared schemas

## Troubleshooting
- 422 on valid input: check Pydantic field types vs JSON types.
- Slow async endpoints: look for blocking sync calls in `async def`.
- Circular imports: move schemas to a shared module.