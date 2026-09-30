---
name: sre-slos
description: "SRE SLI/SLO/SLA implementation"
category: devops
tags: [sre-slos, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: sre-slos
---
# SRE SLOs

> Внедряйте Service Level Indicators, Objectives и Agreements по SRE-практикам.

## Быстрый старт
```yaml
# slo-config.yaml — конфигурация уровня сервиса
apiVersion: sre.google.com/v1
kind: SLO
metadata:
  name: api-availability
  service: payment-api
spec:
  description: "Payment API availability SLO"
  target: 99.9  # процент
  window: 28d   # скользящее окно

  indicator:
    type: availability
    definition: |
      # SLI: доля успешных запросов
      good_events = count(status_code < 500)
      valid_events = count(status_code != 0)
      sli = good_events / valid_events

  burnRateAlerts:
    - severity: page
      threshold: 0.01  # минут бюджета ошибок в минуту
      lookback: 1h
    - severity: ticket
      threshold: 0.001
      lookback: 6h
---
# Политика error budget
apiVersion: sre.google.com/v1
kind: ErrorBudget
metadata:
  name: api-error-budget
spec:
  sloRef: api-availability
  policy:
    deployFreeze:
      enabled: true
      remainingBudgetPercent: 20
```

```python
# Мониторинг SLO с Prometheus
from prometheus_client import Histogram, Counter
import time

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

def track_request(method: str, endpoint: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                REQUEST_COUNT.labels(method=method, endpoint=endpoint, status="200").inc()
                return result
            except Exception:
                REQUEST_COUNT.labels(method=method, endpoint=endpoint, status="500").inc()
                raise
            finally:
                REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(time.time() - start)
        return wrapper
    return decorator
```

## Ключевые концепции
SLI измеряют надёжность сервиса (задержка, доступность, долговечность). SLO задают цели (например, 99.9% доступность за 28 дней). Error budget = (1 - SLO) × всего событий. Burn-rate алармы дают раннее обнаружение.

## Когда использовать
- Определение ожиданий надёжности для сервисов
- Решения на основе данных о скорости деплоя
- Баланс разработки фич и инвестиций в надёжность

## Пошаговое руководство
1. Определите границы сервиса: обещание для пользователя (например, «API отвечает за 300мс p50, доступность 99.9%»).
2. SLI как отношения: good events / valid events, по endpoint, агрегация в скользящем окне.
3. SLO с error budget: доступность 99.9% за 28 дней → бюджет = 43 минуты даунтайма.
4. Подключите мониторинг: экспортируйте гистограммы задержек и счётчики в Prometheus; SLI через recording rules.
5. Burn-rate алармы: page на 2h окне при 14.4x расходе бюджета, ticket на 6h/1d окнах.
6. Гейты изменений: ставьте деплой на паузу, когда остаток бюджета падает ниже порога политики (например, 20%).

## Примеры
```yaml
# Burn-rate аларма с двумя окнами
groups:
  - name: slo-alerts
    rules:
      - alert: APIAvailabilityBurnRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[2h]))
          / sum(rate(http_requests_total[2h])) > 0.02
        # 2h окно, ~14.4x расход бюджета при SLO 99.9%
        annotations:
          summary: "burning through API availability budget fast"
```
```python
# Расчёт SLO compliance из ответа Prometheus Query API
from prometheus_api_client import PrometheusConnect
p = PrometheusConnect(url="http://prometheus:9090")
sli_good = p.custom_query('sum(rate(http_requests_total{status<"500"}[28d]))')
sli_valid = p.custom_query('sum(rate(http_requests_total[28d]))')
print("availability:", float(sli_good[0]["value"][1]) / float(sli_valid[0]["value"][1]))
```

## Лучшие практики
- SLI на реальный пользовательский опыт, не внутренности.
- SLO с error budgets и burn-rate алертами.
- Четыре золотых сигнала: задержка, трафик, ошибки, насыщение.
- Доступность и задержка по скользящим окнам.
- Ежемесячный ревью достижения SLO.
- Релизы привязаны к здоровью error budget.

## Устранение неполадок
- Бюджет исчерпан: заморозьте рискованные изменения и фокусируйтесь на надёжности.
- Шумные алерты: настройте окна burn-rate и пороги.
- Дрейф SLI: стабильное определение метрики и ревью.
- Недостижимый SLO: пересогласуйте со стейкхолдерами и улучшайте.

## Валидация
1. SLI точно измеряются и отчёты строятся
2. Дашборд SLO compliance показывает текущий и исторический статус
3. Error budget алармы срабатывают при деградации
4. Деплой-гейты учитывают политику error budget
