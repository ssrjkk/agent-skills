---
name: risk-modeling
description: "Создание финансовых моделей рисков: VaR, CVaR, симуляция Монте-Карло, стресс-тестирование и декомпозиция рисков портфеля. Для количественного управления рисками."
category: finance
tags: [risk-modeling, var, cvar, monte-carlo, stress-testing, portfolio, quantitative, finance]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---

# Моделирование рисков

> Создание финансовых моделей рисков с VaR, симуляцией Монте-Карло и стресс-тестированием.

## Быстрый старт

```python
import numpy as np
import pandas as pd

def calculate_var(returns: pd.Series, confidence: float = 0.95) -> float:
    """Исторический Value at Risk."""
    return np.percentile(returns, (1 - confidence) * 100)

def calculate_cvar(returns: pd.Series, confidence: float = 0.95) -> float:
    """Conditional VaR (Expected Shortfall)."""
    var = calculate_var(returns, confidence)
    return returns[returns <= var].mean()

# Пример использования
returns = pd.Series(np.random.randn(1000) * 0.02)
print(f"VaR (95%): {calculate_var(returns):.4f}")
print(f"CVaR (95%): {calculate_cvar(returns):.4f}")
```

## Когда использовать

- Измерение рисков портфеля для регуляторного соответствия (Базель III/IV)
- Установка лимитов риска для торговых подразделений
- Стресс-тестирование портфелей против рыночных шоков
- Когда нужно количественно оценить потенциальные убытки

## Пошагово

### 1. Историческая симуляция VaR

```python
class HistoricalVaR:
    def __init__(self, confidence=0.95, horizon_days=1):
        self.confidence = confidence
        self.horizon_days = horizon_days

    def calculate(self, returns: pd.DataFrame, portfolio_weights: np.ndarray) -> dict:
        portfolio_returns = returns.dot(portfolio_weights)

        var = np.percentile(portfolio_returns, (1 - self.confidence) * 100)
        cvar = portfolio_returns[portfolio_returns <= var].mean()

        return {
            'var': var * np.sqrt(self.horizon_days),
            'cvar': cvar * np.sqrt(self.horizon_days),
            'confidence': self.confidence,
        }
```

### 2. Симуляция Монте-Карло

```python
def monte_carlo_var(
    mean_returns: np.ndarray,
    cov_matrix: np.ndarray,
    weights: np.ndarray,
    simulations: int = 10000,
    horizon_days: int = 10,
    confidence: float = 0.95
) -> dict:
    """Параметрический VaR с использованием симуляции Монте-Карло."""
    daily_returns = np.random.multivariate_normal(
        mean_returns, cov_matrix * horizon_days, simulations
    )

    portfolio_returns = daily_returns.dot(weights)

    var = np.percentile(portfolio_returns, (1 - confidence) * 100)
    cvar = portfolio_returns[portfolio_returns <= var].mean()

    return {
        'var': var,
        'cvar': cvar,
        'mean_loss': -portfolio_returns.mean(),
        'worst_case': portfolio_returns.min(),
    }
```

### 3. Стресс-тестирование

```python
class StressTest:
    SCENARIOS = {
        'market_crash': {'equities': -0.30, 'bonds': 0.05, 'commodities': -0.20},
        'rate_shock': {'equities': -0.10, 'bonds': -0.15, 'commodities': 0.05},
        'credit_crisis': {'equities': -0.25, 'bonds': -0.10, 'commodities': -0.15},
        'pandemic': {'equities': -0.35, 'bonds': 0.10, 'commodities': -0.30},
    }

    def run_scenario(self, portfolio: dict, scenario: str) -> dict:
        if scenario not in self.SCENARIOS:
            raise ValueError(f"Неизвестный сценарий: {scenario}")

        shocks = self.SCENARIOS[scenario]
        total_loss = 0
        results = {}

        for asset_class, value in portfolio.items():
            if asset_class in shocks:
                loss = value * shocks[asset_class]
                total_loss += loss
                results[asset_class] = {'value': value, 'shock': shocks[asset_class], 'loss': loss}

        return {
            'scenario': scenario,
            'total_loss': total_loss,
            'details': results,
        }
```

### 4. Декомпозиция рисков

```python
def risk_decomposition(returns: pd.DataFrame, weights: np.ndarray) -> pd.DataFrame:
    """Декомпозиция рисков портфеля по активам."""
    cov = returns.cov()
    portfolio_var = weights.dot(cov).dot(weights)
    marginal_contrib = cov.dot(weights)
    component_contrib = weights * marginal_contrib
    pct_contrib = component_contrib / portfolio_var

    return pd.DataFrame({
        'weight': weights,
        'marginal_contrib': marginal_contrib,
        'component_contrib': component_contrib,
        'pct_contrib': pct_contrib,
    }, index=returns.columns)
```

### 5. Стресс-тест корреляций

```python
def correlation_stress_test(
    returns: pd.DataFrame,
    weights: np.ndarray,
    correlation_multiplier: float = 1.5
) -> dict:
    """Тестирование портфеля в режиме повышенных корреляций."""
    normal_corr = returns.corr()
    stressed_corr = normal_corr * correlation_multiplier
    np.fill_diagonal(stressed_corr.values, 1.0)

    normal_vol = returns.std()
    stressed_cov = np.outer(normal_vol, normal_vol) * stressed_corr

    normal_var = weights.dot(returns.cov()).dot(weights)
    stressed_var = weights.dot(stressed_cov).dot(weights)

    return {
        'normal_var': normal_var,
        'stressed_var': stressed_var,
        'var_increase': (stressed_var - normal_var) / normal_var,
    }
```

## Лучшие практики

- **Используйте несколько методов** — исторический, параметрический и Монте-Карло
- **Бэктестите модели рисков** против фактических убытков
- **Обновляйте матрицы корреляций** регулярно — они меняются в кризисах
- **Включайте хвостовые риски** — нормальные распределения недооценивают экстремальные события
- **Документируйте допущения** — все модели неверны, некоторые полезны

## Типичные ошибки

- Предположение о нормальных распределениях (тяжёлые хвосты важны)
- Использование устаревших матриц корреляций
- Игнорирование риска ликвидности
- Отсутствие стресс-тестирования против беспрецедентных сценариев
- Рассмотрение VaR как единственной меры риска

## Примеры

### Отчёт о рисках портфеля

```python
def generate_risk_report(portfolio_returns: pd.DataFrame, weights: np.ndarray) -> dict:
    var_95 = calculate_var(portfolio_returns.dot(weights), 0.95)
    var_99 = calculate_var(portfolio_returns.dot(weights), 0.99)
    cvar_95 = calculate_cvar(portfolio_returns.dot(weights), 0.95)

    decomposition = risk_decomposition(portfolio_returns, weights)

    return {
        'var_95': var_95,
        'var_99': var_99,
        'cvar_95': cvar_95,
        'max_drawdown': (portfolio_returns.dot(weights).cumsum().cummax() -
                        portfolio_returns.dot(weights).cumsum()).max(),
        'risk_contributions': decomposition['pct_contrib'].to_dict(),
    }
```

## Валидация

```python
def test_var_calculation():
    returns = pd.Series(np.random.randn(10000) * 0.01)
    var = calculate_var(returns, 0.95)
    assert var < 0  # VaR должен быть отрицательным (убыток)
    assert abs(var) < 0.05  # Проверка здравого смысла

def test_stress_test():
    portfolio = {'equities': 1000000, 'bonds': 500000}
    st = StressTest()
    result = st.run_scenario(portfolio, 'market_crash')
    assert result['total_loss'] < 0
```
