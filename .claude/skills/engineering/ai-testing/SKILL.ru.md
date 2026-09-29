---
name: ai-testing
description: "AI-powered test generation and validation"
category: engineering
tags: [ai-testing, engineering, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: ai-testing
---
# AI Testing (AI-Тестирование)

> Генерируйте, валидируйте и поддерживайте тесты с помощью AI-генерации.

## Быстрый старт
```python
# AI-генерация тестов через Claude
from anthropic import Anthropic
import ast
import os

client = Anthropic()

def generate_tests(source_file: str) -> str:
    "Генерация юнит-тестов для Python-модуля с помощью AI."
    with open(source_file) as f:
        source = f.read()

    tree = ast.parse(source)
    functions = [node.name for node in ast.walk(tree)
                 if isinstance(node, ast.FunctionDef) and not node.name.startswith('_')]
    classes = [node.name for node in ast.walk(tree)
               if isinstance(node, ast.ClassDef)]

    prompt = f'''Сгенерируйте полный набор pytest-тестов для модуля.

Module: {os.path.basename(source_file)}
Functions: {', '.join(functions)}
Classes: {', '.join(classes)}

Requirements:
- Coverage: happy path, edge cases, error handling
- Используйте pytest fixtures для setup
- Включите property-based тесты там, где уместно
- Mock внешних зависимостей (I/O, сеть, БД)
- Достичь coverage > 90%

Source code:
<source>
{source}
</source>

Generate tests only:'''

    response = client.messages.create(
        model="claude-sonnet-4-5",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096
    )

    return response.content[0].text

# AI-валидация качества тестов
def validate_test_quality(test_code: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        messages=[{"role": "user", "content": f'''Оцените набор тестов по:

1. Coverage: покрыты ли edge cases?
2. Isolation: тесты изолированы?
3. Maintainability: читаемость?
4. Completeness: чего не хватает?

Test code:
<test_code>
{test_code}
</test_code>

Score each category 1-10 и перечислите пробелы.'''}],
        max_tokens=1000
    )
    return response.content[0].text
```

```bash
# Запуск сгенерированных тестов
pytest tests/ --cov=src --cov-report=term-missing

# Регенерация тестов при изменении исходников в CI:
# если coverage упал более чем на 5%, перегенерировать тесты
```

## Ключевые концепции
AI пишет тесты быстрее, но их нужно валидировать. Комбинируйте AI-генерацию с классическими инструментами (coverage, mutation testing). Проверяйте сгенерированные тесты — они могут галлюцинировать API или терять контекст.

## Когда использовать
- Легаси-кодбазы без тестового покрытия
- Быстрое прототипирование, где писать тесты вручную долго
- Генерация тестовых данных и фикстур
- CI-пайплайн с подсказками тестов для нового кода

## Пошаговое руководство
1. Разберите модуль: обойдите AST и соберите публичные функции, классы и сигнатуры.
2. Соберите промпт: попросите модель сгенерировать pytest с фикстурами, edge cases и моками внешних зависимостей.
3. Сгенерируйте и сохраните: запишите AI-тесты в `tests/` (имя вида `test_<module>.py`).
4. Запустите coverage: `pytest tests/ --cov=src --cov-report=term-missing` и посмотрите пробелы.
5. Проверьте качество: попросите модель оценить coverage/isolation/maintainability; фиксите галлюцинации повторным прогоном.
6. Автоматизируйте в CI: перегенерируйте тесты при падении coverage > 5%; для числовых/логических функций добавьте property-based кейсы.

## Примеры
```python
# Автоматическая регенерация тестов после изменения исходника
import subprocess, pathlib

def regenerate_for(source: str) -> None:
    tests = generate_tests(source)          # из Quick Start
    out = pathlib.Path("tests") / f"test_{pathlib.Path(source).stem}.py"
    out.write_text(tests)
    subprocess.run(["pytest", str(out), "--cov=src", "--cov-report=term-missing"], check=False)
```
```bash
# Quality gate в CI
pytest tests/ --cov=src --cov-fail-under=80 --cov-report=term-missing
# Mutation testing spot-check
pip install mutmut && mutmut run --paths-to-mutate src/
```

## Валидация
1. AI-тесты проходят при прогоне по исходникам
2. Coverage достигает порога (> 80%)
3. В сгенерированных тестах нет галлюцинированных вызовов
4. Тесты детерминированы (одинаковые результаты на каждом прогоне)
