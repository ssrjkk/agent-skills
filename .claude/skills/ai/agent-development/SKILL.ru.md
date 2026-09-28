---
name: agent-development
description: "Build reliable LLM agents and agentic workflows: tool use, memory, loops, guardrails, and evaluation. Use for autonomous AI systems."
category: ai
tags: [agent-development, ai, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: agent-development
author: ssrjkk
---
# Agent Development (Разработка агентов)

> Создание надёжных LLM-агентов с инструментами, памятью и защитами.

## Быстрый старт
```bash
pip install openai
# определите инструменты, цикл и лимиты безопасности
```

## Когда использовать
- Автоматизация многошаговых задач, требующих решений
- Ассистенты по коду, исследовательские агенты, поддержка клиентов
- Workflow, которые вызывают инструменты и итерируют
- Когда одного промпта недостаточно

## Лучшие практики

### Дизайн инструментов
- Давайте инструментам ясные имена, описания и JSON-схемы
- Делайте инструменты детерминированными и осознающими сайд-эффекты
- Валидируйте вход инструментов; возвращайте структурированные ошибки
- Держите поверхность инструментов маленькой и сфокусированной

### Цикл агента
- Структура: perceive -> decide -> act -> observe
- Ограничьте число шагов (max_iterations)
- Детектируйте циклы и застревания; добавьте условие остановки
- Логируйте каждый шаг (инструмент, вход, выход) для отладки

### Память
- Используйте short-term контекст + long-term хранилище (vector DB)
- Суммаризируйте диалог под размер контекстного окна
- Персистируйте важное состояние между сессиями
- Разделяйте факты о пользователе и факты сессии

### Безопасность
- Ограничьте разрушительные инструменты (delete, deploy, pay) апрувами
- Песочница для исполнения кода; запрет опасных команд
- Добавьте guardrails: фильтры контента, лимиты бюджета, таймауты
- Экранируйте prompt injection в выводах инструментов и пользовательских данных

## Зависимости
```bash
pip install openai pydantic
# опционально: langgraph, crewai или свой цикл
```

## Примеры
```python
from pydantic import BaseModel, Field

class WeatherTool:
    name = "get_weather"
    description = "Get current weather for a city"
    schema = {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
    }

    def run(self, city: str) -> str:
        return f"Weather in {city}: sunny, 22C"
```
```python
# Минимальный цикл агента с лимитом шагов
def run_agent(user_input: str, tools: dict, max_steps: int = 10) -> str:
    messages = [{"role": "user", "content": user_input}]
    for _ in range(max_steps):
        resp = call_llm(messages, tools=list(tools.values()))
        if not resp.tool_calls:
            return resp.content
        for call in resp.tool_calls:
            result = tools[call.function.name].run(**call.function.arguments)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
    return "Reached max steps without final answer."
```
```python
# Апрув-гейт для разрушительных действий
def run_tool_safe(name: str, args: dict) -> str:
    if name in DANGEROUS_TOOLS:
        if not confirm(f"Approve {name}({args})? "):
            return "Action denied by user."
    return tools[name].run(**args)
```
```python
# Сжатие контекста под окно
def compress(messages, keep_last=6):
    head = messages[:2]                      # system + оригинал
    tail = messages[-keep_last:]
    summary = summarize(messages[2:-keep_last])
    return head + [{"role": "assistant", "content": f"[Summary] {summary}"}] + tail
```

## Пошаговое руководство
1. Определите цель агента, входы и критерии остановки.
2. Спроектируйте небольшой набор инструментов с ясными схемами.
3. Реализуйте цикл perceive-decide-act с max steps.
4. Добавьте память: short-term контекст и персистентное хранилище.
5. Ограничьте опасные действия апрувами.
6. Добавьте guardrails: бюджет, таймаут, фильтры контента.
7. Оцените на бенчмарке репрезентативных задач.
8. Логируйте трассы для отладки и регрессий.

## Валидация
1. Агент завершает задачи в пределах max steps
2. Нет бесконечных циклов и повторяющихся одинаковых действий
3. Разрушительные инструменты требуют апрува
4. Ошибки инструментов обрабатываются корректно (retry или объяснение)
5. Стоимость и задержка в рамках бюджета на eval-наборе

## Устранение неполадок
- Агент зацикливается: ужесточите max_steps и детектируйте повторные вызовы.
- Неверные вызовы инструментов: улучшите описания и схемы.
- Переполнение контекста: суммаризируйте и обрезайте старые ходы.