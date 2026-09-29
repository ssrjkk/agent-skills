---
name: test-driven-development
description: "Practice test-driven development: red-green-refactor, test design, refactoring safely, and coverage discipline. Use for reliable code evolution."
category: engineering
tags: [test-driven-development, engineering, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: test-driven-development
author: ssrjkk
---
# Test-Driven Development (Разработка через тесты)

> Тесты первыми — для чистого и надёжного кода.

## Быстрый старт
```text
1. RED: напишите падающий тест
2. GREEN: минимально его пройдите
3. REFACTOR: уберите дубли безопасно
```

## Когда использовать
- Новые фичи и фиксы багов
- Безопасный рефакторинг существующего кода
- Дизайн API через использование
- Снижение риска регрессий

## Лучшие практики

### Red-Green-Refactor
- Один падающий тест за раз
- Минимальная реализация для прохода
- Рефакторинг без смены поведения
- Повторяйте маленькими циклами

### Дизайн тестов
- Тестируйте поведение, не реализацию
- Одна концепция ассерта на тест
- Имена по ожидаемому поведению
- Покрывайте границы и ошибки

### Безопасный рефакторинг
- Тесты до/после каждого изменения
- Маленькие механические рефакторинги
- Тесты зелёные между шагами
- Инструменты рефакторинга IDE

### Дисциплина
- Никогда не пишите код без падающего теста
- Не пропускайте "просто заработает"
- Тесты быстрые
- Покрывайте happy path и edge cases

## Зависимости
```bash
# выберите фреймворк под ваш язык
# Python: pytest, JS: jest, Go: testing
```

## Примеры
```python
# 1. Сначала пишем падающий тест
import pytest

def test_cart_total_includes_tax():
    cart = Cart()
    cart.add("book", 10.0)
    assert cart.total() == pytest.approx(10.9)  # 9% налог
```
```python
# 2. Минимальная реализация для прохода
class Cart:
    def __init__(self):
        self._items = []

    def add(self, name: str, price: float) -> None:
        self._items.append(price)

    def total(self) -> float:
        return sum(self._items) * 1.09
```
```python
# 3. Рефакторинг: налог в константу
TAX_RATE = 0.09

class Cart:
    def total(self) -> float:
        return sum(self._items) * (1 + TAX_RATE)
```
```python
# Edge case тесты
def test_cart_empty_total_is_zero():
    assert Cart().total() == 0.0

def test_cart_negative_price_rejected():
    with pytest.raises(ValueError):
        Cart().add("x", -1.0)
```

## Пошаговое руководство
1. Выберите маленькое поведение для реализации.
2. Напишите падающий тест, выражающий его (RED).
3. Запустите и убедитесь, что падает по правильной причине.
4. Напишите минимальный код для прохода (GREEN).
5. Прогоните сьют; затем рефакторите безопасно.
6. Повторите для следующего поведения.
7. Добавьте edge case и error тесты.
8. Коммитьте маленькими зелёными инкрементами.

## Валидация
1. Каждое поведение покрыто тестом, падавшим сначала
2. Рефакторинги держат все тесты зелёными
3. Тесты быстрые и детерминированные
4. Границы и ошибки покрыты
5. Сьют гейтит CI

## Устранение неполадок
- Слишком большой тест: разбейте на мелкие поведения.
- Пере-реализация: пишите минимальный код для прохода.
- Желание пропустить: помните, тесты предотвращают регрессии.