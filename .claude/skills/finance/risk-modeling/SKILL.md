---
name: risk-modeling
description: "Build financial risk models: VaR, CVaR, Monte Carlo simulation, stress testing, and portfolio risk decomposition. Use for quantitative risk management."
category: finance
tags: [risk-modeling, var, cvar, monte-carlo, stress-testing, portfolio, quantitative, finance]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---

# Risk Modeling

> Building financial risk models with VaR, Monte Carlo simulation, and stress testing.

## Quick Start

```python
import numpy as np
import pandas as pd

def calculate_var(returns: pd.Series, confidence: float = 0.95) -> float:
    """Historical Value at Risk."""
    return np.percentile(returns, (1 - confidence) * 100)

def calculate_cvar(returns: pd.Series, confidence: float = 0.95) -> float:
    """Conditional VaR (Expected Shortfall)."""
    var = calculate_var(returns, confidence)
    return returns[returns <= var].mean()

# Example usage
returns = pd.Series(np.random.randn(1000) * 0.02)
print(f"VaR (95%): {calculate_var(returns):.4f}")
print(f"CVaR (95%): {calculate_cvar(returns):.4f}")
```

## When to Use

- Measuring portfolio risk for regulatory compliance (Basel III/IV)
- Setting risk limits for trading desks
- Stress testing portfolios against market shocks
- When you need to quantify potential losses

## Step-by-Step

### 1. Historical Simulation VaR

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

### 2. Monte Carlo Simulation

```python
def monte_carlo_var(
    mean_returns: np.ndarray,
    cov_matrix: np.ndarray,
    weights: np.ndarray,
    simulations: int = 10000,
    horizon_days: int = 10,
    confidence: float = 0.95
) -> dict:
    """Parametric VaR using Monte Carlo simulation."""
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

### 3. Stress Testing

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
            raise ValueError(f"Unknown scenario: {scenario}")

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

### 4. Risk Decomposition

```python
def risk_decomposition(returns: pd.DataFrame, weights: np.ndarray) -> pd.DataFrame:
    """Decompose portfolio risk by asset."""
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

### 5. Correlation Stress

```python
def correlation_stress_test(
    returns: pd.DataFrame,
    weights: np.ndarray,
    correlation_multiplier: float = 1.5
) -> dict:
    """Test portfolio under increased correlation regime."""
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

## Best Practices

- **Use multiple methods** — historical, parametric, and Monte Carlo
- **Backtest your risk models** against actual losses
- **Update correlation matrices** regularly — they change in crises
- **Include tail risk** — normal distributions underestimate extreme events
- **Document assumptions** — all models are wrong, some are useful

## Common Pitfalls

- Assuming normal distributions (fat tails matter)
- Using stale correlation matrices
- Ignoring liquidity risk
- Not stress testing against unprecedented scenarios
- Treating VaR as the only risk measure

## Examples

### Portfolio Risk Report

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

## Validation

```python
def test_var_calculation():
    returns = pd.Series(np.random.randn(10000) * 0.01)
    var = calculate_var(returns, 0.95)
    assert var < 0  # VaR should be negative (loss)
    assert abs(var) < 0.05  # Sanity check

def test_stress_test():
    portfolio = {'equities': 1000000, 'bonds': 500000}
    st = StressTest()
    result = st.run_scenario(portfolio, 'market_crash')
    assert result['total_loss'] < 0
```
