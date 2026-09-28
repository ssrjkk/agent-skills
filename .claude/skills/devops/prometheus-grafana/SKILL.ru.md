---
name: prometheus-grafana
description: "Set up monitoring with Prometheus and Grafana: metrics, exporters, alerting rules, dashboards, and SLO tracking. Use for observability."
category: devops
tags: [prometheus-grafana, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: prometheus-grafana
author: ssrjkk
---
# Prometheus & Grafana (Прометей и Графана)

> Мониторинг систем через метрики Prometheus и дашборды Grafana.

## Быстрый старт
```bash
docker run -p 9090:9090 -v prometheus.yml:/etc/prometheus/prometheus.yml -d prom/prometheus
docker run -p 3000:3000 -d grafana/grafana
# Grafana: localhost:3000 admin/admin
```

## Когда использовать
- Сбор time-series метрик с сервисов
- Дашборды задержек, ошибок и насыщения
- Алерты по порогам и SLO burn
- Мониторинг Kubernetes и инфраструктуры

## Лучшие практики

### Инструментация
- Отдавайте `/metrics` в формате Prometheus
- Counters (растущие), gauges, histograms
- Метки умеренно (без cardinality explosion)
- Клиентские библиотеки под язык

### Scrape и хранение
- Разумные интервалы (15-60s)
- `service_discovery` или статические targets
- Ограничьте retention; используйте best practices TSDB
- Recording rules для горячих запросов

### Алерты
- Правила с порогами PromQL
- Alertmanager для маршрутизации и дедупликации
- Алертьте на симптомы (SLO), а не только метрики
- `for`, pending и корректная серьёзность

### Дашборды
- Сфокусированные дашборды на сервис
- Паттерны RED (Rate, Errors, Duration) и USE
- Панели с понятными единицами
- SLO-трекинг через burn-rate панели

## Зависимости
```bash
# Python клиент
pip install prometheus-client
# или Node:
npm i prom-client
```

## Примеры
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
# PromQL: доля ошибок по сервису
sum(rate(http_requests_total{status=~"5.."}[5m]))
  / sum(rate(http_requests_total[5m]))
```

## Пошаговое руководство
1. Инструментируйте сервисы: отдавайте `/metrics`.
2. Настройте scrape и хранение Prometheus.
3. Добавьте правила алертов и Alertmanager.
4. Подключите Grafana как источник данных.
5. Соберите дашборды по RED/USE паттернам.
6. Трекайте SLO через burn-rate алерты.
7. Обеспечьте auth и TLS.
8. Мониторьте сам монитор: алерты на сам Prometheus.

## Валидация
1. `/metrics` отдаётся и скрейпится успешно
2. Дашборды показывают корректные метрики и единицы
3. Алерты срабатывают и маршрутизируются корректно
4. Кардинальность в пределах лимитов
5. Retention соответствует потребностям

## Устранение неполадок
- Метрик нет: проверьте scrape target и путь.
- Высокая кардинальность: уменьшайте динамические значения меток.
- Нет данных в Grafana: проверьте источник данных и временной диапазон.