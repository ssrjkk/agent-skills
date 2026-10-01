---
name: llm-evals
description: "Build evaluation suites for LLM applications: golden datasets, metrics, LLM-as-judge, regression gates, and CI integration. Use for trustworthy model behavior."
category: ai
tags: [llm-evals, ai, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: llm-evals
author: ssrjkk
---
# LLM Evals (Оценка LLM)

> Измерение и защита качества LLM-приложений через evaluation-сьюты.

## Быстрый старт
```bash
pip install pytest openai
# соберите golden-набор, оцените ответы, гейтите релизы в CI
```

## Когда использовать
- Отслеживание качества промптов и моделей со временем
- Сравнение вариантов промптов и версий моделей
- Поиск регрессий до релиза
- Уверенность в продакшн-агентах и RAG

## Лучшие практики

### Golden-наборы
- Покрывайте happy paths, edge cases и adversarial вводы
- Используйте реальные запросы плюс синтетические вариации
- Включайте ожидаемые ответы или рубрики на кейс
- Держите набор небольшим (20-100) и поддерживаемым

### Метрики
- exact-match — для структурированного вывода (JSON, коды)
- similarity — для свободного текста (семантическая или лексическая)
- LLM-as-judge с рубрикой — для субъективного качества
- Считайте скоре по метрике и агрегируйте по набору

### LLM-as-Judge
- Дайте судье явную рубрику оценки
- Где можно — референс-ответы
- Используйте другую модель, чем оцениваемая
- Калибруйте: выборочно сверяйте судью с человеческими метками

### CI-гейтинг
- Прогоняйте evals на каждом PR для изменённых промптов/моделей
- Ставьте пороги; фейльте при регрессиях
- Держите флаки-проверки вне блокирующего пути
- Репортите diff против базлайна

## Зависимости
```bash
pip install pytest openai numpy
# опционально: ragas, promptfoo, deepeval
```

## Примеры
```python
import json
import openai

client = openai.OpenAI()

def run_case(prompt: str, user_input: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-6",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input},
        ],
    )
    return resp.choices[0].message.content
```
```python
# Golden-набор с ожидаемым структурированным выводом
GOLDEN = [
    {
        "input": "Alice works at Acme.",
        "expected": {"name": "Alice", "org": "Acme"},
    },
    {
        "input": "No company mentioned here.",
        "expected": {"name": None, "org": None},
    },
]

def exact_match(out: str, expected: dict) -> bool:
    try:
        return json.loads(out) == expected
    except json.JSONDecodeError:
        return False
```
```python
# LLM-as-judge с рубрикой
JUDGE_PROMPT = """Rate the answer 1-5 using this rubric:
5 = correct, complete, well-grounded. 1 = wrong or off-topic.
Return only the number."""

def judge(answer: str) -> int:
    resp = client.chat.completions.create(
        model="gpt-6",
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user", "content": answer},
        ],
    )
    return int(resp.choices[0].message.content)
```
```python
# Регрессионный гейт
def run_suite() -> float:
    scores = []
    for case in GOLDEN:
        out = run_case(PROMPT, case["input"])
        scores.append(1.0 if exact_match(out, case["expected"]) else 0.0)
    return sum(scores) / len(scores)

def test_no_regression():
    assert run_suite() >= 0.9, "Eval score dropped below threshold"
```

## Пошаговое руководство
1. Определите, что значит "хорошо": формат, фактологичность, полезность.
2. Соберите golden-набор с рубриками или ожидаемыми ответами.
3. Выберите метрики: exact-match, similarity или LLM-as-judge.
4. Реализуйте харнесс оценки и агрегацию результатов.
5. Зафиксируйте базовый скоре на текущем промпте/модели.
6. Добавьте регрессионный гейт в CI с порогом.
7. Проверяйте качество судьи против человеческих меток.
8. Расширяйте набор по мере нахождения фейлов в проде.

## Валидация
1. Evals детерминированы на одинаковых входах
2. Пороговый гейт блокирует явные регрессии
3. Скоре судьи коррелирует с человеческой оценкой
4. Golden-набор покрывает основные фейлы
5. Время прогона практично для каждого PR

## Устранение неполадок
- Дрейф судьи: перекалибруйте рубрику и сверяйте метки.
- Flaky скоре: чините недетерминизм (temperature, модель, seed).
- Слишком много кейсов: приоритизируйте сигнальные вводы, убирайте дубли.