---
name: pytest
description: "Write reliable Python tests with pytest: fixtures, parametrize, mocking, async tests, and CI integration. Use for any Python testing."
category: qa
tags: [pytest, qa, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: pytest
author: ssrjkk
---
# pytest (Пайтест)

> Написание надёжных Python-тестов через pytest.

## Быстрый старт
```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=src --cov-report=term-missing
```

## Когда использовать
- Юнит-тесты функций и классов
- Интеграционные тесты с реальными сервисами
- Регрессионные сьюты в CI
- Тестирование async-кода и пайплайнов данных

## Лучшие практики

### Структура тестов
- Ясные имена: `test_<поведение>`
- На каждый тест — arrange, act, assert
- Одно поведение на тест
- Тесты в `tests/`, зеркаля пакет

### Фикстуры
- Фикстуры — для setup/teardown и общих ресурсов
- Скоупы (`function`, `session`, `module`)
- Делайте фикстуры узкими и компонуемыми
- Yield-фикстуры для очистки

### Параметризация
- `@pytest.mark.parametrize` для вариантов ввода
- Покрывайте границы и error-кейсы
- `pytest.raises` для ожидаемых исключений
- `monkeypatch` для env и сайд-эффектов

### Изоляция
- Мокайте внешние вызовы (`mock.patch`)
- В юнит-тестах без сети и файловой системы
- Для файловых тестов — `tmp_path`
- Держите тесты детерминированными и быстрыми

## Зависимости
```bash
pip install pytest pytest-cov pytest-asyncio
# мокинг: pytest-mock
```

## Примеры
```python
# Базовый тест с параметризацией
import pytest

def add(a, b):
    return a + b

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```
```python
# Фикстуры с очисткой
import pytest

@pytest.fixture
def temp_db(tmp_path):
    db = create_db(tmp_path / "test.db")
    yield db
    db.close()
```
```python
# Async тест
import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_fetch():
    data = await fetch_data()
    assert "items" in data
```
```python
# Мокирование внешнего вызова
from unittest.mock import patch

def test_api(mock_session):
    with patch("app.client.get", return_value={"ok": True}):
        result = app.client.get("/health")
    assert result == {"ok": True}
```

## Пошаговое руководство
1. Установите pytest и создайте директорию `tests/`.
2. Напишите сфокусированные тесты на ядро поведения.
3. Вынесите setup в фикстуры.
4. Параметризуйте варианты ввода и edge cases.
5. Для изоляции мокайте внешние сервисы.
6. Добавьте замер покрытия и порог.
7. Подключите pytest в CI на каждом PR.
8. Для скорости — `-x`, `--ff`, `-p no:cacheprovider`.

## Валидация
1. Все тесты проходят локально и в CI
2. Покрытие соответствует порогу проекта
3. Тесты не зависят от сети или абсолютных путей
4. Тесты детерминированы между запусками
5. Фейлы указывают на конкретное поведение

## Устранение неполадок
- Флаки: ищите общее состояние или зависимость от времени.
- Медленный сьют: помечайте интеграционные тесты и гоняйте юнит отдельно.
- Пробелы покрытия: проверьте, какие ветки не имеют ассертов.