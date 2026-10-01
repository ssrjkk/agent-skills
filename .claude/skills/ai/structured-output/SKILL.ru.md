---
name: structured-output
description: "Force LLMs to emit valid, schema-constrained structured output: JSON modes, function calling, JSON Schema validation, and error recovery. Use for reliable data extraction."
category: ai
tags: [structured-output, ai, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: structured-output
author: ssrjkk
---
# Structured Output (Структурированный вывод)

> Получение от LLM валидного, ограниченного схемой вывода.

## Быстрый старт
```bash
pip install openai pydantic jsonschema
# объединяйте response_format с JSON Schema для гарантированной формы
```

## Когда использовать
- Извлечение данных в типизированные записи
- Ответы API, которые должны соответствовать контракту
- Генерация аргументов tool/function
- Снижение нагрузки от битого вывода

## Лучшие практики

### Дизайн схемы
- Строгая JSON Schema под форму вывода
- `additionalProperties: false` — отбрасывать лишнее
- Держите схемы плоскими и примитивными, где можно
- Версионируйте схемы вместе с кодом

### Выбор режима
- Предпочитайте `response_format` провайдера (json_object / json_schema)
- Если вывод идёт в tool — function calling
- Без structured mode — few-shot + валидация
- Никогда не доверяйте невалидированному тексту

### Валидация и восстановление
- Валидируйте каждый ответ по схеме
- При ошибке — повторный промпт с сообщением об ошибке
- Ограничьте retries; фолбэк на запись по умолчанию
- Логируйте битые ответы для настройки промпта

## Зависимости
```bash
pip install openai pydantic jsonschema
```

## Примеры
```python
import json
import openai
from jsonschema import validate, ValidationError

client = openai.OpenAI()

SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0},
        "emails": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["name", "age"],
    "additionalProperties": False,
}

def extract(text: str) -> dict:
    resp = client.chat.completions.create(
        model="gpt-6",
        messages=[{"role": "user", "content": f"Extract from: {text}"}],
        response_format={"type": "json_schema", "json_schema": {"name": "person", "schema": SCHEMA}},
    )
    return json.loads(resp.choices[0].message.content)
```
```python
# Валидация и восстановление при фейле
def safe_extract(text: str, retries: int = 2) -> dict:
    for attempt in range(retries):
        raw = extract(text)
        try:
            validate(instance=raw, schema=SCHEMA)
            return raw
        except ValidationError as e:
            print(f"retry {attempt}: {e.message}")
    return {"name": "unknown", "age": 0}
```
```python
# Извлечение через Pydantic
from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str
    age: int = Field(ge=0)
    emails: list[str] = []

resp = client.beta.chat.completions.parse(
    model="gpt-6",
    messages=[{"role": "user", "content": "Alice is 30, email a@b.com"}],
    response_format=Person,
)
print(resp.choices[0].message.parsed.model_dump())
```
```python
# JSON mode фолбэк для провайдеров без json_schema
def extract_json_mode(text: str) -> dict:
    resp = client.chat.completions.create(
        model="gpt-6",
        messages=[
            {"role": "system", "content": "Respond only with valid JSON matching the schema."},
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content)
```

## Пошаговое руководство
1. Определите точную форму вывода как JSON Schema.
2. Выберите строжайший режим провайдера (schema > json_object > few-shot).
3. Реализуйте извлечение со схемой.
4. Валидируйте каждый ответ; при несовпадении — повторный промпт с ошибкой.
5. Добавьте лимиты retries и безопасные дефолты.
6. Логируйте фейлы для улучшения промпта или схемы.
7. Добавьте тесты на реалистичные вводы, включая edge cases.
8. Версионируйте схемы и мониторьте дрейф.

## Валидация
1. Весь вывод парсится как валидный JSON
2. Каждый вывод удовлетворяет схеме (программная проверка)
3. Невалидные вводы всё равно дают schema-conforming записи
4. Восстановление через retry работает без бесконечных циклов
5. Изменения контракта версионируются

## Устранение неполадок
- Вывод не проходит схему: ужесточите промпт, добавьте примеры или сузьте схему.
- Ошибки `additionalProperties`: есть лишние поля — поправьте схему.
- Модель игнорирует формат: переключитесь на function calling или guided generation.