---
name: clean-architecture
description: "Structure codebases with clean architecture: layers, dependency rule, use cases, ports and adapters. Use for maintainable large codebases."
category: engineering
tags: [clean-architecture, architecture, hexagonal, dependency-rule, use-cases]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Clean Architecture

> Organizing codebases for maintainability and testability.

## Quick Start
```text
Layers (outer -> inner):
  Frameworks/Drivers -> Interface -> Application -> Domain
Dependency rule: dependencies point inward only.
```

## When to Use
- Large, long-lived codebases
- Complex business domains
- Teams needing testability
- Systems with changing infrastructure

## Best Practices

### Dependency Rule
- Dependencies point inward only
- Domain has no framework imports
- Outer layers depend on interfaces
- Invert dependencies with DI

### Layers
- Domain: entities and business rules
- Application: use cases and ports
- Interface: controllers/presenters
- Infrastructure: DB, HTTP, external

### Use Cases
- Model each business action as a use case
- Keep use cases thin and focused
- Ports define interfaces to the outside
- Adapters implement ports

### Boundaries
- Cross boundaries with interfaces
- Map data at the boundary (DTOs)
- Keep frameworks at the edges
- Test each layer in isolation

## Dependencies
```bash
# language-agnostic; DI container helps
```

## Examples
```python
# Domain entity (no framework imports)
class Order:
    def __init__(self, items: list[float]):
        if any(i <= 0 for i in items):
            raise ValueError("invalid item")
        self.items = items

    def total(self) -> float:
        return sum(self.items)
```
```python
# Port (interface to the outside)
from abc import ABC, abstractmethod

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None: ...

    @abstractmethod
    def find(self, order_id: int) -> Order | None: ...
```
```python
# Use case in the application layer
class CreateOrder:
    def __init__(self, repo: OrderRepository):
        self._repo = repo

    def execute(self, items: list[float]) -> Order:
        order = Order(items)
        self._repo.save(order)
        return order
```
```python
# Adapter implementing the port
class SqlOrderRepository(OrderRepository):
    def save(self, order: Order) -> None:
        db.insert("orders", {"items": order.items})
```

## Step-by-Step
1. Define the domain entities and business rules first.
2. Identify use cases (actions) the app must support.
3. Define ports (interfaces) the domain needs.
4. Implement adapters (DB, HTTP) outside the domain.
5. Wire everything with dependency injection.
6. Keep frameworks at the edges.
7. Test domain and use cases without infra.
8. Keep the dependency rule enforced.

## Validation
1. Domain has no framework imports
2. Dependencies point inward
3. Use cases are testable without infra
4. Changing a DB/HTTP lib doesn't ripple through the core
5. Each layer is independently testable

## Troubleshooting
- Framework creep: move framework code to adapters.
- Anemic domain: put business rules in entities.
- Leaky boundaries: map data at the boundaries with DTOs.