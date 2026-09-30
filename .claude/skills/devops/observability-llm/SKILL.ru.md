---
name: observability-llm
description: "LLM observability with Langfuse/LangSmith"
category: devops
tags: [observability-llm, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: observability-llm
---
# LLM Observability (Наблюдаемость LLM)

> Мониторьте, трейсите и отлаживайте LLM-приложения с Langfuse и LangSmith.

## Быстрый старт
```python
# Langfuse — платформа наблюдаемости LLM
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context

langfuse = Langfuse(
    secret_key="sk-lf-...",
    public_key="pk-lf-..."
)

@observe(name="rag-query", as_type="generation")
def rag_query(question: str, context: str) -> str:
    # Автоматически трейсит токены, задержку и метаданные
    langfuse_context.update_current_generation(
        input=question,
        output="generated answer",
        usage={"promptTokens": 150, "completionTokens": 80, "totalTokens": 230},
        metadata={"retrieved_docs": 3, "model": "claude-sonnet-4"}
    )
    return "Generated answer"

# Ручной трейсинг
trace = langfuse.trace(name="document-pipeline")
span = trace.span(name="embedding-generation")
span.end()
trace.update(
    input={"query": "user question"},
    output={"answer": "AI response"}
)
```

```python
# LangSmith — наблюдаемость LangChain
from langsmith import Client
from langchain.callbacks.tracers import LangSmithTracer

import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls-..."
os.environ["LANGCHAIN_PROJECT"] = "my-llm-app"

tracer = LangSmithTracer()
llm.invoke("Hello", config={"callbacks": [tracer]})
```

## Ключевые концепции
Трейсите каждый LLM-вызов: задержка, токены, стоимость, метаданные. Отслеживайте версии промптов, параметры моделей и retrieval-контекст. Отлаживайте по полному трейс-визуализатору. Настройте мониторинг стоимости и качества.

## Когда использовать
- Продакшн-LLM-приложения, которым нужна отладка
- Контроль токенов и затрат по командам
- A/B-тестирование вариаций промптов
- Мониторинг регрессий качества и задержки

## Пошаговое руководство
1. Установите: `pip install langfuse` и задайте env-ключи `LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY`.
2. Декораторы: оберните функции генерации/RAG в `@observe` — SDK сам трейсит задержку, токены и метаданные.
3. Контекст: передавайте input/output, usage dict и retrieval-метаданные (id документов, модель, версии).
4. Дашборды: используйте представления Langfuse/LangSmith для группировки по сессии, проекту или версии промпта.
5. Мониторинг: алерты на всплеск затрат, регрессии задержки и доли ошибок по промпту/модели.
6. Итерации по промптам: сравнение трейсов и prompt-playground для A/B и закрепления победителя.

## Примеры
```python
# Полный RAG-пайплайн как вложенные спаны
from langfuse.decorators import observe, langfuse_context

@observe(name="retrieve")
def retrieve(query: str) -> list[str]:
    return ["doc-1", "doc-2"]  # из вашего vector store

@observe(name="generate")
def generate(query: str, docs: list[str]) -> str:
    langfuse_context.update_current_generation(
        input=query,
        output="answer text",
        usage={"promptTokens": 120, "completionTokens": 40, "totalTokens": 160},
        metadata={"docs": docs, "model": "claude-sonnet-4"},
    )
    return "answer text"

@observe(name="rag")
def rag(question: str) -> str:
    docs = retrieve(question)
    return generate(question, docs)
```
```bash
# Экспорт трейсов для офлайн-анализа
python -m langfuse export-json --project your-project --output ./traces.json
# или self-hosted стек
langfuse-compose up
```

## Лучшие практики
- Трейсьте каждый LLM-вызов: промпт, модель, токены, задержку.
- Трекайте стоимость на вызов и пользователя против злоупотреблений.
- Логируйте вход/выход для отладки и evals.
- Алерты на error rates, перерасход токенов и задержку.
- OpenTelemetry или вендор вроде Langfuse/LangSmith.
- Коррелируйте LLM-трейсы с метриками и логами приложения.

## Устранение неполадок
- Нет трейсов: проверьте, что SDK авто-инструментирует провайдера.
- Высокая стоимость: просмотрите промпты, кэш и тир модели.
- Спайки задержки: проверьте загрузку модели и retries.
- Приватность: редактируйте PII в логируемых промптах и ответах.

## Валидация
1. Трейсы появляются в дашборде Langfuse/LangSmith
2. Токены и стоимость трекаются точно
3. Разбивка задержки показывает, где тратится время
4. Поиск и фильтрация по метаданным/тегам работают
