---
name: django
description: "Build secure web applications with Django: models, views, ORM, admin, auth, REST APIs, and deployment. Use for Python web backends."
category: backend
tags: [django, backend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: django
author: ssrjkk
---
# Django (Джанго)

> Создание безопасных веб-приложений с батарейками в комплекте на Django.

## Быстрый старт
```bash
pip install django djangorestframework
django-admin startproject mysite .
python manage.py migrate
python manage.py runserver
```

## Когда использовать
- Сайты с большим объёмом контента и админ-панелями
- Приложения со встроенным auth и ORM
- Быстрая CRUD-разработка
- Безопасные дефолты из коробки

## Лучшие практики

### Модели
- Проектируйте модели под домен
- Используйте явные типы полей и ограничения
- Добавляйте индексы для горячих запросов
- Схему ведите через миграции, а не сырой SQL

### Вьюхи и URL
- Организуйте по приложениям: `myapp/models.py`, `views.py`, `urls.py`
- Для переиспользуемого поведения — class-based views
- Для API — DRF с сериализаторами и viewsets
- Держите вьюхи тонкими; бизнес-логика — в сервисах

### Безопасность
- Не доверяйте клиентскому вводу: валидируйте формами/сериализаторами
- CSRF и XSS-защита Django — по умолчанию
- Пароли — дефолтными PBKDF2/argon2
- В админке минимальные права; используйте permissions

### Производительность
- select_related, чтобы избежать N+1
- Фильтрация QuerySet, а не Python-циклы
- Кэшируйте тяжёлые страницы и запросы
- В проде `DEBUG=False` и безопасные настройки

## Зависимости
```bash
pip install django djangorestframework
pip install -D pytest pytest-django factory-boy
```

## Примеры
```python
from django.db import models

class Order(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="orders")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("new", "New"), ("paid", "Paid")], default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["user", "created_at"])]
```
```python
from django.views.generic import ListView

class OrderListView(ListView):
    model = Order
    template_name = "orders/list.html"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related("user")
```
```python
from rest_framework import serializers, viewsets

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "amount", "status", "created_at"]

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
```
```python
# Паттерн сервисного слоя
def create_order(user, items) -> Order:
    total = sum(item.price for item in items)
    order = Order.objects.create(user=user, amount=total)
    order.items.set(items)
    return order
```

## Пошаговое руководство
1. Создайте проект и приложения через `startproject`/`startapp`.
2. Смоделируйте домен через Django-модели и миграции.
3. Зарегистрируйте модели в админке для внутренних инструментов.
4. Соберите вьюхи или DRF сериализаторы/viewsets.
5. Добавьте шаблоны для server-rendered страниц (если есть).
6. Добавьте валидацию, permissions и тесты.
7. Оптимизируйте запросы; добавьте кэш на горячие места.
8. Деплойте с `collectstatic`, Gunicorn и reverse proxy.

## Валидация
1. `python manage.py check` проходит
2. `migrate` применяется чисто
3. Тесты проходят (модель, вьюха, API, permissions)
4. Админка и API работают с корректным auth
5. Нет явных N+1 в ключевых вьюхах

## Устранение неполадок
- N+1: используйте `select_related`/`prefetch_related`.
- CSRF-ошибки в API: используйте DRF или аккуратно исключайте session-free эндпоинты.
- Конфликты миграций: приведите состояние моделей в порядок, затем регенерируйте миграции.