---
name: prompt-caching
description: "Optimize LLM cost and latency with prompt caching: cacheable prefixes, cache-control headers, context layout, and cache-aware prompting. Use for high-volume apps."
category: ai
tags: [prompt-caching, ai, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: prompt-caching
author: ssrjkk
---
# Prompt Caching (Кэширование промптов)

> Снижение стоимости и задержки LLM через кэширование повторяющихся префиксов промптов.

## Быстрый старт
```python
# Стабильный контент первым, пометьте его как cacheable
resp = client.chat.completions.create(
    model="gpt-6",
    messages=[
        {"role": "system", "content": LONG_SYSTEM_PROMPT},
        {"role": "user", "content": dynamic_question},
    ],
    extra_headers={"Cache-Control": "ttl=3600, min_tokens=1024"},
)
```

## Когда использовать
- Чат с длинными system-промптами или определениями tools
- Агенты с большим контекстом, повторяющимся между ходами
- RAG-приложения со стабильными системными инструкциями
- Высоконагруженные эндпоинты, где важна стоимость

## Лучшие практики

### Раскладка
- Стабильный контент первым: system prompt, tools, статичный контекст
- Динамический контент последним: пользовательские ходы, retrieved chunks
- Держите стабильный префикс во всех запросах
- Минимальный кэшируемый размер зависит от провайдера (например, 1024+ токенов)

### Cache-Control
- Пометьте кэшируемые сегменты cache-control заголовками
- TTL под ваш паттерн доступа
- Не кэшируйте секреты или per-user данные
- Проверяйте cache hits через usage metadata (`cached_tokens`)

### Дизайн под кэш
- Держите system prompt идентичным между вызовами
- Отделяйте статичные определения tools от динамического ввода
- Переиспользуйте один префикс для всего диалога
- Эфемерные данные — в конце контекста

### Измерение
- Отслеживайте cached vs uncached токены в usage
- Меряйте снижение задержки на запрос
- Мониторьте cache hit rate со временем
- Сравнивайте стоимость до и после оптимизации

## Зависимости
```bash
pip install openai anthropic
```

## Примеры
```python
import openai

client = openai.OpenAI()

# Стабильный префикс: system + tools, помечен cacheable
STATIC = [
    {"role": "system", "content": "You are a senior support agent."},
    {"role": "user", "content": "Available tools: search, refund, escalate."},
]

def ask(question: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-6",
        messages=STATIC + [{"role": "user", "content": question}],
        extra_headers={"Cache-Control": "ttl=3600, min_tokens=1024"},
    )
    usage = resp.usage
    print("cached:", getattr(usage, "prompt_tokens_details", None))
    return resp.choices[0].message.content
```
```python
# Anthropic-style cache control
import anthropic

client = anthropic.Anthropic()

def ask(question: str) -> str:
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=[
            {"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}},
        ],
        messages=[{"role": "user", "content": question}],
    )
    print("cache:", resp.usage.cache_creation_input_tokens, resp.usage.cache_read_input_tokens)
    return resp.content[0].text
```
```python
# Сессионное кэширование: стабильный system на весь диалог
def chat_session():
    messages = list(STATIC)
    while True:
        q = input("> ")
        resp = client.chat.completions.create(
            model="gpt-6", messages=messages + [{"role": "user", "content": q}],
            extra_headers={"Cache-Control": "ttl=3600, min_tokens=1024"},
        )
        answer = resp.choices[0].message.content
        messages.append({"role": "user", "content": q})
        messages.append({"role": "assistant", "content": answer})
        print(answer)
```
```python
# Проверка cache hits из usage metadata
def report_cache(usage) -> dict:
    details = getattr(usage, "prompt_tokens_details", None) or {}
    cached = getattr(details, "cached_tokens", 0)
    total = usage.prompt_tokens
    return {"cached": cached, "total": total, "rate": cached / total if total else 0}
```

## Пошаговое руководство
1. Найдите стабильный префикс в промптах (system, tools, статика).
2. Переместите динамический контент в конец контекста.
3. Пометьте префикс cacheable механизмом провайдера.
4. Проверяйте cache hits в usage metadata.
5. Меряйте задержку и стоимость до/после.
6. Настройте TTL и минимальные токены под ваш трафик.
7. Не кэшируйте per-user или секретные данные.
8. Мониторьте hit rate и держите префикс байт-в-байт идентичным.

## Валидация
1. Usage показывает cached токены на повторных запросах
2. Задержка падает для кэшируемой части
3. Стоимость на запрос заметно снижается
4. Ответы остаются корректными после cache hits
5. Секретов нет в кэшируемом префиксе

## Устранение неполадок
- Нет cache hits: префикс различается между вызовами — держите его байт-в-байт идентичным.
- Короткие промпты: поднимите префикс выше минимума провайдера.
- Инвалидация кэша: изменение префикса инвалидирует — проектируйте под стабильность.