---
name: pytest
description: "Write reliable Python tests with pytest: fixtures, parametrize, mocking, async tests, and CI integration. Use for any Python testing."
category: qa
tags: [pytest, python, testing, fixtures, mocking, parametrize, coverage]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-26
updated: 2026-09-28
author: ssrjkk
---
# pytest

> Writing reliable Python tests with pytest.

## Quick Start
```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=src --cov-report=term-missing
```

## When to Use
- Unit tests for functions and classes
- Integration tests with real services
- Regression suites in CI
- Testing async code and data pipelines

## Best Practices

### Test Structure
- Name tests clearly: `test_<behavior>`
- Arrange, act, assert per test
- One behavior per test
- Put tests in `tests/` mirroring the package

### Fixtures
- Use fixtures for setup/teardown and shared resources
- Scope fixtures (`function`, `session`, `module`)
- Make fixtures narrow and composable
- Yield fixtures for cleanup

### Parametrization
- Use `@pytest.mark.parametrize` for input variants
- Cover boundaries and error cases
- Use `pytest.raises` for expected exceptions
- Use `monkeypatch` for env and side effects

### Isolation
- Mock external calls (`mock.patch`)
- Avoid network and filesystem in unit tests
- Use `tmp_path` for file-based tests
- Keep tests deterministic and fast

## Dependencies
```bash
pip install pytest pytest-cov pytest-asyncio
# mocking: pytest-mock
```

## Examples
```python
# Basic test with parametrize
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
# Fixtures with cleanup
import pytest

@pytest.fixture
def temp_db(tmp_path):
    db = create_db(tmp_path / "test.db")
    yield db
    db.close()
```
```python
# Async test
import pytest
import pytest_asyncio

@pytest.mark.asyncio
async def test_fetch():
    data = await fetch_data()
    assert "items" in data
```
```python
# Mocking external call
from unittest.mock import patch

def test_api(mock_session):
    with patch("app.client.get", return_value={"ok": True}):
        result = app.client.get("/health")
    assert result == {"ok": True}
```

## Step-by-Step
1. Install pytest and set up a `tests/` directory.
2. Write focused tests for the core behavior.
3. Extract setup into fixtures.
4. Parametrize input variants and edge cases.
5. Mock external services for isolation.
6. Add coverage measurement and a threshold.
7. Wire pytest into CI on every PR.
8. Run with `-x`, `--ff`, and `-p no:cacheprovider` for speed.

## Validation
1. All tests pass locally and in CI
2. Coverage meets the project threshold
3. No tests depend on network or fixed absolute paths
4. Tests are deterministic across runs
5. Failures point to the specific behavior

## Troubleshooting
- Flaky tests: find shared state or timing dependence.
- Slow suite: mark integration tests and run unit separately.
- Coverage gaps: check which branches lack assertions.