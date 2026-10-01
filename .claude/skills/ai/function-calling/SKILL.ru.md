---
name: function-calling
description: "Implement robust LLM function/tool calling: schemas, multi-call handling, validation, error recovery, and structured execution. Use for agent tool use."
category: ai
tags: [function-calling, ai, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: function-calling
author: ssrjkk
---
# Function Calling (Вызов функций)

> Подключение LLM к реальным функциям через надёжный tool calling.

## Быстрый старт
```bash
pip install openai
# объявите tools, дайте модели их вызвать, выполните и зациклите
```

## Когда использовать
- Запрос данных, вычислений или действий от модели
- Структурированное извлечение в определённые входы функций
- Agentic workflow с чередованием рассуждений и вызовов
- Снижение галлюцинаций через ограничение вывода схемами

## Лучшие практики

### Схемы инструментов
- Пишите ясные полные JSON-схемы на функцию
- Используйте `description` на каждом параметре
- Задавайте `required` и разумные `enum`/`pattern`
- Имена параметров должны говорить сами за себя

### Цикл вызова
- Детектируйте tool_calls; выполняйте; добавляйте результаты как `tool` сообщения
- Поддерживайте несколько вызовов в одном ответе
- Включайте `tool_call_id` в каждый результат
- Ограничьте итерации во избежание runaway-циклов

### Валидация и восстановление
- Валидируйте аргументы до выполнения
- Возвращайте структурированные ошибки, которые читает модель
- Никогда не выполняйте опасные tools без апрува
- Логируйте полный трейс вызовов для отладки

### Промптинг
- Давайте модели контекст: когда вызывать каждый tool
- Просите использовать tools вместо угадывания ответов
- Примеры использования tools — в system prompt
- Описания tools должны соответствовать реальному поведению

## Зависимости
```bash
pip install openai pydantic
# опционально: instructor для schema-guided вызовов
```

## Примеры
```python
import openai

client = openai.OpenAI()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
        },
    }
]

resp = client.chat.completions.create(
    model="gpt-6",
    messages=[{"role": "user", "content": "Weather in Tokyo?"}],
    tools=TOOLS,
)
call = resp.choices[0].message.tool_calls[0]
print(call.function.name, call.function.arguments)
```
```python
# Выполнение вызова и возврат результата
import json

def dispatch(name: str, args: dict) -> str:
    if name == "get_weather":
        return weather_api(args["city"])
    return json.dumps({"error": f"unknown tool: {name}"})

result = dispatch(call.function.name, json.loads(call.function.arguments))
messages = [
    {"role": "user", "content": "Weather in Tokyo?"},
    resp.choices[0].message,
    {"role": "tool", "tool_call_id": call.id, "content": result},
]
final = client.chat.completions.create(model="gpt-6", messages=messages, tools=TOOLS)
print(final.choices[0].message.content)
```
```python
# Обработка нескольких вызовов
def run_tools(message) -> list[dict]:
    results = []
    for call in message.tool_calls:
        args = json.loads(call.function.arguments)
        results.append(
            {"role": "tool", "tool_call_id": call.id, "content": dispatch(call.function.name, args)}
        )
    return results
```
```python
# Валидация через pydantic до выполнения
from pydantic import BaseModel, ValidationError

class WeatherArgs(BaseModel):
    city: str
    units: str = "metric"

def safe_dispatch(name: str, args: dict) -> str:
    try:
        if name == "get_weather":
            w = WeatherArgs(**args)
            return weather_api(w.city, w.units)
        return f'{{"error": "unknown tool {name}"}}'
    except ValidationError as e:
        return f'{{"error": "invalid args: {e}"}}'
```

## Пошаговое руководство
1. Напишите функции, которые модель должна вызывать.
2. Определите JSON-схемы с описаниями и required-полями.
3. Отправьте первый запрос с `tools` и намерением пользователя.
4. Выполните возвращённые `tool_calls` и добавьте результаты с ID.
5. Циклите, пока модель не вернёт финальный текстовый ответ.
6. Валидируйте аргументы; возвращайте структурированные ошибки.
7. Добавьте guardrails для опасных действий.
8. Логируйте трейсы; тестируйте edge cases и битые аргументы.

## Валидация
1. Модель выдаёт валидные schema-conforming вызовы на тестовом наборе
2. Multi-call ответы выполняются по порядку
3. Ошибки возвращаются модели для восстановления
4. Цикл завершается в пределах лимита итераций
5. Опасные инструменты требуют явного апрува

## Устранение неполадок
- Модель не вызывает tools: добавьте примеры использования в system prompt.
- Невалидный JSON-args: ослабьте схемы или используйте guided generation.
- Циклы: ограничьте итерации и детектируйте повторяющиеся одинаковые вызовы.