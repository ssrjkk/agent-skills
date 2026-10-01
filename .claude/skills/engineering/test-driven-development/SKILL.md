---
name: test-driven-development
description: "Practice test-driven development: red-green-refactor, test design, refactoring safely, and coverage discipline. Use for reliable code evolution."
category: engineering
tags: [tdd, testing, red-green-refactor, refactoring, test-first, engineering]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Test-Driven Development

> Writing tests first to drive clean, reliable code.

## Quick Start
```text
1. RED: write a failing test
2. GREEN: make it pass minimally
3. REFACTOR: clean up safely
```

## When to Use
- New features and bug fixes
- Refactoring existing code safely
- Designing APIs by usage
- Reducing regression risk

## Best Practices

### Red-Green-Refactor
- Write one failing test at a time
- Implement the minimal code to pass
- Refactor without changing behavior
- Repeat in small cycles

### Test Design
- Test behavior, not implementation
- One assertion concept per test
- Name tests by expected behavior
- Cover boundaries and errors

### Refactoring Safely
- Run tests before/after each change
- Use small, mechanical refactors
- Keep tests green between steps
- Use the IDE's refactoring tools

### Discipline
- Never write code without a failing test
- Avoid skipping to "just make it work"
- Keep tests fast
- Cover the happy path and edge cases

## Dependencies
```bash
# pick a framework for your language
# Python: pytest, JS: jest, Go: testing
```

## Examples
```python
# 1. Write the failing test first
import pytest

def test_cart_total_includes_tax():
    cart = Cart()
    cart.add("book", 10.0)
    assert cart.total() == pytest.approx(10.9)  # 9% tax
```
```python
# 2. Minimal implementation to pass
class Cart:
    def __init__(self):
        self._items = []

    def add(self, name: str, price: float) -> None:
        self._items.append(price)

    def total(self) -> float:
        return sum(self._items) * 1.09
```
```python
# 3. Refactor: extract tax into a constant
TAX_RATE = 0.09

class Cart:
    def total(self) -> float:
        return sum(self._items) * (1 + TAX_RATE)
```
```python
# Add edge case tests
def test_cart_empty_total_is_zero():
    assert Cart().total() == 0.0

def test_cart_negative_price_rejected():
    with pytest.raises(ValueError):
        Cart().add("x", -1.0)
```

## Step-by-Step
1. Pick a small behavior to implement.
2. Write a failing test that expresses it (RED).
3. Run it and confirm it fails for the right reason.
4. Write the minimal code to pass (GREEN).
5. Run the suite; then refactor safely.
6. Repeat for the next behavior.
7. Add edge case and error tests.
8. Commit small, green increments.

## Validation
1. Every behavior is covered by a test that failed first
2. Refactors keep all tests green
3. Tests are fast and deterministic
4. Boundaries and errors are covered
5. The suite gates CI

## Troubleshooting
- Test too big: split into smaller behaviors.
- Over-implementing: write the minimal code to pass.
- Temptation to skip: remember tests prevent regressions.