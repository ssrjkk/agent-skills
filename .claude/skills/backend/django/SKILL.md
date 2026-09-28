---
name: django
description: "Build secure web applications with Django: models, views, ORM, admin, auth, REST APIs, and deployment. Use for Python web backends."
category: backend
tags: [django, python, web, orm, models, admin, rest, backend]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-26
updated: 2026-09-28
author: ssrjkk
---
# Django

> Building secure, batteries-included web apps with Django.

## Quick Start
```bash
pip install django djangorestframework
django-admin startproject mysite .
python manage.py migrate
python manage.py runserver
```

## When to Use
- Content-heavy sites and admin panels
- Apps needing built-in auth and ORM
- Rapid CRUD development
- Secure defaults out of the box

## Best Practices

### Models
- Design models to mirror the domain
- Use explicit field types and constraints
- Add indexes for hot queries
- Manage schema with migrations, not raw SQL

### Views & URLs
- Organize by app: `myapp/models.py`, `views.py`, `urls.py`
- Use class-based views for reusable behavior
- Use DRF for APIs with serializers and viewsets
- Keep views thin; business logic in services

### Security
- Never trust client input: validate with forms/serializers
- Use Django's CSRF and XSS protections by default
- Store passwords with default PBKDF2/argon2
- Apply least privilege in admin; use permissions

### Performance
- Select related to avoid N+1 queries
- Use `QuerySet` filtering instead of Python loops
- Cache heavy pages and queries
- Set `DEBUG=False` and secure settings in prod

## Dependencies
```bash
pip install django djangorestframework
pip install -D pytest pytest-django factory-boy
```

## Examples
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
# Service layer pattern
def create_order(user, items) -> Order:
    total = sum(item.price for item in items)
    order = Order.objects.create(user=user, amount=total)
    order.items.set(items)
    return order
```

## Step-by-Step
1. Start the project and apps with `startproject`/`startapp`.
2. Model the domain with Django models and migrations.
3. Register models in the admin for internal tooling.
4. Build views or DRF serializers/viewsets.
5. Add templates for server-rendered pages (if any).
6. Add validation, permissions, and tests.
7. Optimize queries; add caching where hot.
8. Deploy with `collectstatic`, Gunicorn, and a reverse proxy.

## Validation
1. `python manage.py check` passes
2. `migrate` applies cleanly
3. Tests pass (model, view, API, permission)
4. Admin and API work with proper auth
5. No obvious N+1 queries in key views

## Troubleshooting
- N+1 queries: use `select_related`/`prefetch_related`.
- CSRF errors in API: use DRF or exempt session-free endpoints carefully.
- Migration conflicts: fix model state, then regenerate migrations.