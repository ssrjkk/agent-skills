---
name: sre-slos
description: "SRE SLI/SLO/SLA implementation"
category: devops
tags: [sre, sli, slo, sla, reliability, monitoring]
models: [sonnet, opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# SRE SLOs

> Implement Service Level Indicators, Objectives, and Agreements following SRE best practices.

## Quick Start
```yaml
# slo-config.yaml — Service level configuration
apiVersion: sre.google.com/v1
kind: SLO
metadata:
  name: api-availability
  service: payment-api
spec:
  description: "Payment API availability SLO"
  target: 99.9  # percentage
  window: 28d   # rolling window
  
  indicator:
    type: availability
    definition: |
      # SLI: Ratio of successful requests
      good_events = count(status_code < 500)
      valid_events = count(status_code != 0)
      sli = good_events / valid_events
  
  burnRateAlerts:
    - severity: page
      threshold: 0.01  # minutes of error budget consumed per minute
      lookback: 1h
    - severity: ticket
      threshold: 0.001
      lookback: 6h
---
# Error budget policy
apiVersion: sre.google.com/v1
kind: ErrorBudget
metadata:
  name: api-error-budget
spec:
  sloRef: api-availability
  policy:
    # Stop deployments when error budget is depleted
    deployFreeze:
      enabled: true
      remainingBudgetPercent: 20
```

```python
# SLO Monitoring with Prometheus
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

## Key Concepts
SLIs measure service reliability (latency, availability, durability). SLOs set targets (e.g., 99.9% availability over 28 days). Error budget = (1 - SLO) × total events. Use burn rate alerts for early detection.

## When to Use
- Defining reliability expectations for services
- Making data-driven decisions about deployment velocity
- Balancing feature development with reliability investment

## Step-by-Step
1. Pick service boundaries: define the user-visible promise (e.g., "API replies within 300ms p50, 99.9% available").
2. Define SLIs as ratios: good events / valid events, per endpoint, aggregated over a rolling window.
3. Set SLO targets with error budgets: availability = 99.9% over 28 days → budget = 43 min of downtime.
4. Wire monitoring: export latency histograms and counters from Prometheus; compute SLIs with recording rules.
5. Add burn-rate alerts: page on 2h lookback at 14.4x budget consumption, ticket on 6h/1d windows.
6. Gate change velocity: pause deployments when remaining budget crosses the policy threshold (e.g., 20%).

## Examples
```yaml
# Multi-window burn-rate alert (two tiers)
groups:
  - name: slo-alerts
    rules:
      - alert: APIAvailabilityBurnRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[2h]))
          / sum(rate(http_requests_total[2h])) > 0.02
        # 2h window, ~14.4x budget consumption at 99.9% SLO
        annotations:
          summary: "API availability error budget burning fast"
```
```python
# Compute SLO compliance from a Prometheus Query API response
from prometheus_api_client import PrometheusConnect
p = PrometheusConnect(url="http://prometheus:9090")
sli_good = p.custom_query('sum(rate(http_requests_total{status<"500"}[28d]))')
sli_valid = p.custom_query('sum(rate(http_requests_total[28d]))')
print("availability:", float(sli_good[0]["value"][1]) / float(sli_valid[0]["value"][1]))
```

## Best Practices
- Define SLIs that measure real user experience, not internals.
- Set SLOs with error budgets and burn-rate alerts.
- Use the four golden signals: latency, traffic, errors, saturation.
- Track availability and latency over rolling windows.
- Review SLO attainment in a monthly review.
- Tie releases to error-budget health.

## Troubleshooting
- Budget exhausted: freeze risky changes and focus on reliability.
- Noisy alerts: tune burn-rate windows and thresholds.
- SLI drift: keep the measurement definition stable and reviewed.
- Unreachable SLO: renegotiate with stakeholders and improve.

## Validation
1. SLIs are accurately measured and reported
2. SLO compliance dashboard shows current and historical status
3. Error budget alerts fire correctly during degradation
4. Deployment gates respect error budget policy
