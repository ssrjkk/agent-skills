---
name: prometheus-grafana
description: "Set up monitoring with Prometheus and Grafana: metrics, exporters, alerting rules, dashboards, and SLO tracking. Use for observability."
category: devops
tags: [prometheus, grafana, monitoring, metrics, alerting, dashboards, observability]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-26
updated: 2026-09-28
author: ssrjkk
---
# Prometheus & Grafana

> Monitoring systems with Prometheus metrics and Grafana dashboards.

## Quick Start
```bash
docker run -p 9090:9090 -v prometheus.yml:/etc/prometheus/prometheus.yml -d prom/prometheus
docker run -p 3000:3000 -d grafana/grafana
# Grafana: localhost:3000 admin/admin
```

## When to Use
- Collecting time-series metrics from services
- Dashboards for latency, errors, and saturation
- Alerting on thresholds and SLO burn
- Kubernetes and infra monitoring

## Best Practices

### Instrumentation
- Expose `/metrics` in Prometheus format
- Use counters (increasing), gauges, histograms
- Label metrics moderately (avoid cardinality explosion)
- Use client libraries for the language

### Scraping & Storage
- Set sane scrape intervals (15-60s)
- Use `service_discovery` or static targets
- Limit retention and use TSDB best practices
- Configure recording rules for hot queries

### Alerting
- Define alerts with PromQL thresholds
- Use Alertmanager for routing and dedup
- Alert on symptoms (SLOs), not just metrics
- Set for, `pending`, and proper severity

### Dashboards
- Build focused dashboards per service
- Use RED (Rate, Errors, Duration) and USE patterns
- Add panels with meaningful units
- Track SLOs with burn-rate panels

## Dependencies
```bash
# Python client
pip install prometheus-client
# or Node:
npm i prom-client
```

## Examples
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: app
    static_configs:
      - targets: ["app:8080"]
rule_files:
  - alerts.yml
```
```yaml
# alerts.yml
groups:
  - name: app
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 10m
        labels: { severity: critical }
        annotations: { summary: "Error rate above 5%" }
```
```python
from prometheus_client import Counter, Histogram, start_http_server
import random, time

REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["status"])
LATENCY = Histogram("http_request_duration_seconds", "Request latency")

start_http_server(8080)
while True:
    REQUESTS.labels(status="200").inc()
    with LATENCY.time():
        time.sleep(random.uniform(0.01, 0.2))
```
```promql
# PromQL: error ratio per service
sum(rate(http_requests_total{status=~"5.."}[5m]))
  / sum(rate(http_requests_total[5m]))
```

## Step-by-Step
1. Instrument services to expose `/metrics`.
2. Configure Prometheus scraping and storage.
3. Add alerting rules and Alertmanager.
4. Connect Grafana as the data source.
5. Build dashboards with RED/USE patterns.
6. Track SLOs with burn-rate alerts.
7. Secure with auth and TLS.
8. Monitor the monitor: alert on Prometheus itself.

## Validation
1. `/metrics` exposed and scraped successfully
2. Dashboards show correct metrics and units
3. Alerts fire and route correctly
4. Cardinality stays within limits
5. Retention matches your needs

## Troubleshooting
- Missing metrics: check the scrape target and path.
- High cardinality: reduce dynamic label values.
- No data in Grafana: verify the data source and time range.