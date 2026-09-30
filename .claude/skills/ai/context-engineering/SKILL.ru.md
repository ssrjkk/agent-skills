---
name: context-engineering
description: "Curate LLM context windows for quality and cost: system prompts, compaction, just-in-time retrieval, progressive disclosure, and token budgets. Use for effective agent context."
category: ai
tags: [context-engineering, ai, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: context-engineering
author: ssrjkk
---
# Context Engineering (Контекст-инжиниринг)

> Курирование контекстного окна LLM для качества и цены.

## Быстрый старт
```python
# Держите маленький стабильный system prompt, берите только нужное
SYSTEM = "You are a concise senior engineer."
TASK = "Fix the bug in src/auth.py"
```

## Когда использовать
- Длинные агентные сессии, выходящие за окно
- RAG, где много контекста вредит качеству
- Чувствительные к стоимости высоконагруженные вызовы
- Multi-turn агенты с потребностями в памяти

## Лучшие практики

### Бюджет контекста
- Токен-бюджет на секцию (system, задача, память, retrieval)
- System prompt маленький и информативный
- Обрезайте retrieved chunks до top-k и релевантных фрагментов
- Резервируйте место под ответ

### Компакция
- Суммаризируйте старые ходы вместо сырой истории
- Структурированные суммари (решения, действия, открытые вопросы)
- Последние ходы держите дословно для когерентности
- Триггер компакции по порогу токенов

### Progressive Disclosure
- Детали грузите только по необходимости (lazy retrieval)
- Суммари + указатели на глубокие доки
- Уточняющие вопросы до загрузки большого контекста
- Примеры кэшируйте, не повторяйте

### Качество retrieval
- Извлекайте по запросу, а не всё сразу
- Реранкинг и дедупликация перед вставкой
- Цитируйте источники для проверки
- Держите вставленный контекст свежим

## Зависимости
```bash
pip install tiktoken openai
# токенизатор для бюджета
```

## Примеры
```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    return len(enc.encode(text))

BUDGET = {"system": 500, "task": 1000, "memory": 1500, "retrieval": 2000}
print(count_tokens("hello world"))
```
```python
# Компакция со структурированным суммари
def compact(history: list[dict], summary: str, keep_last: int = 6) -> list[dict]:
    return [
        {"role": "system", "content": f"Conversation summary so far:\n{summary}"}
    ] + history[-keep_last:]
```
```python
# Lazy retrieval: только по необходимости
def build_context(question: str, memory: dict) -> str:
    chunks = []
    if "codebase" in question.lower():
        chunks += retrieve("code", question, k=4)
    if "api" in question.lower():
        chunks += retrieve("api_docs", question, k=2)
    return "\n\n".join(chunks)[:BUDGET["retrieval"]]
```
```python
# Обрезка под бюджет токенов
def trim_to_budget(text: str, budget: int) -> str:
    tokens = enc.encode(text)
    if len(tokens) <= budget:
        return text
    return enc.decode(tokens[:budget]) + "\n...[trimmed]"
```

## Пошаговое руководство
1. Определите токен-бюджет на секцию для задачи.
2. Напишите плотный system prompt с ролью и ограничениями.
3. Извлекайте только нужное текущему ходу (lazy).
4. Вставляйте top-k, дедуплицированные, цитируемые чанки.
5. Суммаризируйте старые ходы в структурированную память.
6. Обрезайте длинный контент до бюджета.
7. Меряйте использование токенов и стоимость на вызов.
8. Итерируйте бюджеты по качеству ответов.

## Валидация
1. Ответы остаются корректными при росте сессии
2. Стоимость токенов на вызов в рамках бюджета
3. Извлечённый контекст релевантен (recall@k)
4. Компакция сохраняет решения и факты
5. Нет overflow-ошибок в проде

## Устранение неполадок
- Переполнение контекста: компактируйте раньше и обрезайте сильнее.
- Потеря фактов после компакции: улучшите формат суммари.
- Низкое качество при большом контексте: уменьшайте число чанков, держите релевантное.