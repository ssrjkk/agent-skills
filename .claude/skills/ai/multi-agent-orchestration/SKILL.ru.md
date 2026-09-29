---
name: multi-agent-orchestration
description: "Design and run multi-agent systems: orchestrator-worker, routing, handoffs, shared state, and coordination patterns. Use for complex agent teams."
category: ai
tags: [multi-agent-orchestration, ai, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: multi-agent-orchestration
author: ssrjkk
---
# Multi-Agent Orchestration (Оркестрация мультиагентов)

> Координация нескольких специализированных агентов в надёжные системы.

## Быстрый старт
```python
# Оркестратор выбирает воркера по задаче; воркеры возвращают результаты
from dataclasses import dataclass

@dataclass
class AgentResult:
    task: str
    output: str
```

## Когда использовать
- Задачи с разной специализацией (research, код, ревью)
- Параллелимые независимые подзадачи
- Длинные workflow, разбитые на надёжные шаги
- Сложные домены, которые один агент обрабатывает плохо

## Лучшие практики

### Оркестратор-воркер
- Оркестратор планирует, делегирует и собирает результаты
- Воркеры одноцелевые и stateless
- Ясный контракт передачи задач
- Лимиты конкурентных воркеров и общих шагов

### Роутинг и хендоффы
- Роутите по типу задачи, а не по догадкам
- Явные handoff-сообщения (намерение + контекст)
- Валидируйте вывод воркера до передачи
- При фейле роутинга — дефолтный воркер

### Общее состояние
- Общий стор для фактов и артефактов
- Избегайте дублирования контекста; ссылайтесь по ID
- Координируйте записи против гонок
- Логируйте полный трейс выполнения

### Надёжность
- Retry фейл-воркеров с backoff
- Таймауты и бюджеты на воркера
- Детекция циклов и deadlock
- Агрегация частичных результатов при фейле

## Зависимости
```bash
pip install openai pydantic
# опционально: langgraph, autogen, crewai
```

## Примеры
```python
# Минимальный оркестратор
def orchestrate(task: str, workers: dict) -> dict:
    plan = plan_task(task)          # выбирает имена воркеров
    results = {}
    for name, sub in plan.items():
        results[name] = workers[name](sub)
    return {"plan": plan, "results": results}
```
```python
# Контракт воркера
def researcher(query: str) -> str:
    return run_llm(f"Research: {query}")

def reviewer(text: str) -> str:
    return run_llm(f"Review for correctness and style:\n{text}")
```
```python
# Роутинг по намерению
def route(task: str) -> str:
    intent = classify(task)
    if intent == "research":
        return "researcher"
    if intent == "review":
        return "reviewer"
    return "general"
```
```python
# Параллельное выполнение через thread pool
from concurrent.futures import ThreadPoolExecutor

def run_parallel(workers: dict, tasks: dict) -> dict:
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {name: ex.submit(workers[name], task) for name, task in tasks.items()}
        return {name: f.result() for name, f in futures.items()}
```

## Пошаговое руководство
1. Разбейте домен на одноцелевые роли воркеров.
2. Определите контракт хендоффа (задача, контекст, формат вывода).
3. Постройте оркестратор: планирование и роутинг.
4. Добавьте стор общего состояния для артефактов.
5. Запускайте независимые подзадачи параллельно с лимитами.
6. Добавьте retries, таймауты и бюджеты.
7. Валидируйте выводы на каждом хендоффе.
8. Трассируйте и логируйте полное выполнение.

## Валидация
1. Оркестратор завершается в рамках бюджета шагов/времени
2. Воркеры получают корректно сформированные задачи
3. Хендоффы переносят нужный контекст
4. Параллельные задачи не портят общее состояние
5. Фейлы деградируют аккуратно с частичными результатами

## Устранение неполадок
- Deadlock: уберите циклические хендоффы; добавьте таймауты.
- Потеря контекста при хендоффе: передавайте намерение + суммари явно.
- Сбойный воркер: валидируйте выводы и добавьте шаг ревью.