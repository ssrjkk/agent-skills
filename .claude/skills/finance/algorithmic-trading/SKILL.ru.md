---
name: algorithmic-trading
description: "Создание систем алгоритмической торговли: бэктестинг, разработка стратегий, исполнение ордеров, управление рисками и пайплайны рыночных данных. Для количественных финансов."
category: finance
tags: [algorithmic-trading, backtesting, strategy, quantitative, finance, market-data, execution, risk]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---

# Алгоритмическая торговля

> Создание систем алгоритмической торговли с бэктестингом, стратегиями и управлением рисками.

## Быстрый старт

```python
import pandas as pd
import numpy as np

class MovingAverageCrossover:
    """Простая стратегия возврата к среднему."""

    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, prices: pd.Series) -> pd.Series:
        short_ma = prices.rolling(self.short_window).mean()
        long_ma = prices.rolling(self.long_window).mean()

        signals = pd.Series(0, index=prices.index)
        signals[short_ma > long_ma] = 1   # Покупка
        signals[short_ma < long_ma] = -1  # Продажа

        return signals

    def backtest(self, prices: pd.Series, initial_capital=100000):
        signals = self.generate_signals(prices)
        positions = signals.diff().fillna(0)

        portfolio = pd.DataFrame(index=prices.index)
        portfolio['returns'] = prices.pct_change()
        portfolio['position'] = signals.shift(1)
        portfolio['strategy_returns'] = portfolio['position'] * portfolio['returns']

        portfolio['cumulative_returns'] = (1 + portfolio['strategy_returns']).cumprod()
        portfolio['equity'] = initial_capital * portfolio['cumulative_returns']

        return portfolio
```

## Когда использовать

- Создание автоматизированных торговых систем для акций, крипто или фьючерсов
- Бэктестинг торговых стратегий перед реальным деплоем
- Когда ручная торговля слишком медленная или эмоциональная
- Необходимость системного управления рисками

## Пошагово

### 1. Пайплайн рыночных данных

```python
import asyncio
from dataclasses import dataclass

@dataclass
class Tick:
    symbol: str
    price: float
    volume: float
    timestamp: float

class MarketDataFeed:
    def __init__(self):
        self.subscribers: list[callable] = []

    def subscribe(self, callback):
        self.subscribers.append(callback)

    async def stream(self, symbols: list[str]):
        """Подключение к биржевому WebSocket и эмиссия тиков."""
        while True:
            tick = await self._receive_tick(symbols)
            for callback in self.subscribers:
                callback(tick)
```

### 2. Проектирование стратегии

```python
from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def on_tick(self, tick: Tick) -> float:
        """Возвращает целевой размер позиции (от -1 до 1)."""
        pass

    @abstractmethod
    def on_bar(self, bars: pd.DataFrame) -> float:
        """Возвращает сигнал на основе OHLCV баров."""
        pass

class MeanReversionStrategy(Strategy):
    def __init__(self, lookback=20, threshold=2.0):
        self.lookback = lookback
        self.threshold = threshold

    def on_bar(self, bars: pd.DataFrame) -> float:
        prices = bars['close'].tail(self.lookback)
        z_score = (prices.iloc[-1] - prices.mean()) / prices.std()

        if z_score > self.threshold:
            return -1.0  # Перекупленность, продавать
        elif z_score < -self.threshold:
            return 1.0   # Перепроданность, покупать
        return 0.0
```

### 3. Движок бэктестинга

```python
class BacktestEngine:
    def __init__(self, initial_capital=100000, commission=0.001):
        self.initial_capital = initial_capital
        self.commission = commission

    def run(self, strategy: Strategy, data: pd.DataFrame) -> dict:
        capital = self.initial_capital
        position = 0
        trades = []

        for i in range(len(data)):
            signal = strategy.on_bar(data.iloc[:i+1])

            if signal > 0 and position <= 0:
                # Покупка
                shares = int(capital * signal / data.iloc[i]['close'])
                cost = shares * data.iloc[i]['close'] * (1 + self.commission)
                capital -= cost
                position += shares
                trades.append(('BUY', i, shares, data.iloc[i]['close']))

            elif signal < 0 and position > 0:
                # Продажа
                revenue = position * data.iloc[i]['close'] * (1 - self.commission)
                capital += revenue
                trades.append(('SELL', i, position, data.iloc[i]['close']))
                position = 0

        final_value = capital + position * data.iloc[-1]['close']
        return {
            'final_value': final_value,
            'total_return': (final_value - self.initial_capital) / self.initial_capital,
            'num_trades': len(trades),
            'trades': trades,
        }
```

### 4. Управление рисками

```python
class RiskManager:
    def __init__(self, max_position_pct=0.1, max_drawdown_pct=0.2):
        self.max_position_pct = max_position_pct
        self.max_drawdown_pct = max_drawdown_pct
        self.peak_equity = 0

    def check_position_size(self, order_value: float, portfolio_value: float) -> bool:
        return order_value / portfolio_value <= self.max_position_pct

    def check_drawdown(self, current_equity: float) -> bool:
        self.peak_equity = max(self.peak_equity, current_equity)
        drawdown = (self.peak_equity - current_equity) / self.peak_equity
        return drawdown <= self.max_drawdown_pct

    def calculate_stop_loss(self, entry_price: float, risk_pct: float = 0.02) -> float:
        return entry_price * (1 - risk_pct)
```

### 5. Исполнение ордеров

```python
import aiohttp

class OrderExecutor:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    async def place_order(self, symbol: str, side: str, quantity: float, price: float):
        async with aiohttp.ClientSession() as session:
            order = {
                'symbol': symbol,
                'side': side,
                'quantity': quantity,
                'price': price,
                'type': 'LIMIT',
            }
            headers = {'Authorization': f'Bearer {self.api_key}'}
            async with session.post(f'{self.api_url}/orders', json=order, headers=headers) as resp:
                return await resp.json()
```

## Лучшие практики

- **Всегда делайте бэктест** перед реальной торговлей
- **Включайте проскальзывание и комиссии** в бэктесты
- **Используйте walk-forward анализ** для избежания переобучения
- **Внедряйте circuit breakers** для экстремальных рыночных условий
- **Логируйте всё** — сделки, сигналы, ошибки
- **Начинайте с paper trading** перед реальными деньгами

## Типичные ошибки

- Переобучение на исторических данных (curve fitting)
- Игнорирование транзакционных издержек и проскальзывания
- Look-ahead bias в бэктестах
- Отсутствие обработки пробелов в данных или ошибок
- Работа без лимитов риска

## Примеры

### Метрики производительности

```python
def calculate_metrics(returns: pd.Series) -> dict:
    total_return = (1 + returns).prod() - 1
    annual_return = (1 + total_return) ** (252 / len(returns)) - 1
    volatility = returns.std() * np.sqrt(252)
    sharpe = annual_return / volatility if volatility > 0 else 0

    cumulative = (1 + returns).cumprod()
    drawdown = cumulative / cumulative.cummax() - 1
    max_drawdown = drawdown.min()

    return {
        'total_return': total_return,
        'annual_return': annual_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_drawdown,
    }
```

## Валидация

```python
def test_strategy():
    prices = pd.Series(np.random.randn(100).cumsum() + 100)
    strategy = MovingAverageCrossover()
    portfolio = strategy.backtest(prices)
    assert 'equity' in portfolio.columns
    assert len(portfolio) == len(prices)
```
