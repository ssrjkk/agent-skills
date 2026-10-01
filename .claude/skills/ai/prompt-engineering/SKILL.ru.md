---
name: prompt-engineering
description: "Design effective prompts for LLMs: role framing, structured output, chain-of-thought, few-shot, and evaluation. Use to get reliable model behavior."
category: ai
tags: [prompt-engineering, ai, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: prompt-engineering
author: ssrjkk
---
# Prompt Engineering (Промпт-Инжиниринг)

> Проектирование промптов, которые надёжно направляют поведение LLM.

## Быстрый старт
```text
You are a senior Python code reviewer.
Review the code below for bugs, security issues, and style.
Output a markdown report with sections: Issues, Severity, Fix.
```

## Когда использовать
- Получение консистентного структурированного вывода от LLM
- Снижение галлюцинаций в критичных процессах
- Устойчивость промптов к разным моделям и версиям
- Промпты для агентов и инструментов

## Лучшие практики

### Фрейминг
- Дайте модели чёткую роль и задачу
- Укажите ограничения явно (формат, длина, тон)
- Давайте контекст до вопроса
- По возможности — одна задача на промпт

### Структурированный вывод
- Просите JSON/YAML со схемой
- Используйте few-shot примеры нужного формата
- Просите самопроверку: "validate your JSON before responding"
- Предпочитайте `response_format`/tools, если API поддерживает

### Рассуждение
- Используйте chain-of-thought для многошаговых задач
- Просите пошаговые рассуждения до финального ответа
- Держите рассуждения отдельно от итогового результата
- Не утекайте внутренние рассуждения в вывод пользователю

## Зависимости
```bash
pip install openai   # или anthropic, google-generativeai
```

## Примеры
```text
# Структурированное извлечение JSON
Extract entities from the text below as JSON.
Schema: {"name": string, "org": string|null, "confidence": float 0-1}
Return only valid JSON, no commentary.

Text: "Alice works at Acme and handles billing."
```

```text
# Chain-of-thought
Solve the math problem step by step, then give the final answer.
Show each calculation. End with: "Answer: <number>".

Problem: A train travels 240 km in 3 hours. What is the average speed?
```

```python
import openai

client = openai.OpenAI()
resp = client.chat.completions.create(
    model="gpt-6",
    messages=[
        {"role": "system", "content": "You extract entities to JSON."},
        {"role": "user", "content": '{"text": "Alice works at Acme"}'},
    ],
    response_format={"type": "json_object"},
)
print(resp.choices[0].message.content)
```

```python
# Оценка качества промпта на тестовом наборе
def score_prompt(prompt: str, cases: list[tuple[str, str]]) -> float:
    correct = 0
    for inp, expected in cases:
        out = run_model(prompt, inp)
        if normalize(out) == normalize(expected):
            correct += 1
    return correct / len(cases)
```

## Пошаговое руководство
1. Определите задачу, ожидаемый вывод и режимы отказа.
2. Напишите промпт с ролью и ограничениями; включите схему вывода.
3. Добавьте 2-3 few-shot примера точного формата.
4. Для задач на рассуждение — шаги с раздельным финальным ответом.
5. Тестируйте на отложенной выборке; меряйте точность и соблюдение формата.
6. Итерируйте: добавляйте неудачные кейсы, ужесточайте ограничения, убирайте шум.
7. Версионируйте промпты; фиксируйте модель и temperature.
8. Мониторьте дрейф и переоценивайте по расписанию.

## Валидация
1. Вывод парсится как валидный JSON/YAML при структурированном формате
2. Точность на eval-наборе соответствует цели
3. Промпт работает на целевых моделях
4. Нет prompt injection от пользовательского контента (песочница для недоверенного ввода)
5. Задержка и стоимость в рамках бюджета

## Устранение неполадок
- Вывод не JSON: ужесточите схему, добавьте few-shot, используйте response_format.
- Галлюцинации: добавьте grounding контекст и просите цитаты.
- Многословные ответы: ограничьте длину и формат в промпте.