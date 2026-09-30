---
name: clean-architecture
description: "Structure codebases with clean architecture: layers, dependency rule, use cases, ports and adapters. Use for maintainable large codebases."
category: engineering
tags: [clean-architecture, engineering, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: clean-architecture
author: ssrjkk
---
# Clean Architecture (Чистая архитектура)

> Организация кодовых баз для поддерживаемости и тестируемости.

## Быстрый старт
```text
Слои (снаружи -> внутрь):
  Frameworks/Drivers -> Interface -> Application -> Domain
Правило зависимостей: зависимости направлены только внутрь.
```

## Когда использовать
- Большие долгоживущие кодовые базы
- Сложные бизнес-домены
- Команды, которым нужна тестируемость
- Системы с меняющейся инфраструктурой

## Лучшие практики

### Правило зависимостей
- Зависимости только внутрь
- Домен без импортов фреймворков
- Внешние слои зависят от интерфейсов
- Инверсия через DI

### Слои
- Domain: сущности и бизнес-правила
- Application: use cases и порты
- Interface: контроллеры/презентеры
- Infrastructure: БД, HTTP, внешнее

### Use cases
- Каждое бизнес-действие — use case
- Use cases тонкие и сфокусированные
- Порты определяют интерфейсы вовне
- Адаптеры реализуют порты

### Границы
- Пересекайте границы через интерфейсы
- Маппинг данных на границе (DTO)
- Фреймворки на краях
- Слой тестируется изолированно

## Зависимости
```bash
# язык-агностик; помогает DI-контейнер
```

## Примеры
```python
# Домен-сущность (без импортов фреймворков)
class Order:
    def __init__(self, items: list[float]):
        if any(i <= 0 for i in items):
            raise ValueError("invalid item")
        self.items = items

    def total(self) -> float:
        return sum(self.items)
```
```python
# Порт (интерфейс вовне)
from abc import ABC, abstractmethod

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None: ...

    @abstractmethod
    def find(self, order_id: int) -> Order | None: ...
```
```python
# Use case в application-слое
class CreateOrder:
    def __init__(self, repo: OrderRepository):
        self._repo = repo

    def execute(self, items: list[float]) -> Order:
        order = Order(items)
        self._repo.save(order)
        return order
```
```python
# Адаптер, реализующий порт
class SqlOrderRepository(OrderRepository):
    def save(self, order: Order) -> None:
        db.insert("orders", {"items": order.items})
```

## Пошаговое руководство
1. Сначала определите доменные сущности и бизнес-правила.
2. Найдите use cases (действия), которые должно поддерживать приложение.
3. Определите порты (интерфейсы), нужные домену.
4. Реализуйте адаптеры (БД, HTTP) вне домена.
5. Свяжите всё через dependency injection.
6. Держите фреймворки на краях.
7. Тестируйте домен и use cases без инфраструктуры.
8. Соблюдайте правило зависимостей.

## Валидация
1. Домен без импортов фреймворков
2. Зависимости направлены внутрь
3. Use cases тестируются без инфраструктуры
4. Смена БД/HTTP-библиотеки не протекает в ядро
5. Каждый слой тестируется независимо

## Устранение неполадок
- Проникновение фреймворка: переносите framework-код в адаптеры.
- Анемичный домен: бизнес-правила в сущности.
- Дырявые границы: маппинг данных на границах через DTO.