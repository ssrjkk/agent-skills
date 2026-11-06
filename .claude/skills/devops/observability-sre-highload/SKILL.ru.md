---
name: observability-sre-highload
description: "Implements full-stack Observability (VictoriaMetrics, Loki, Vector, OpenTelemetry, Beyla eBPF, Pyroscope), SRE SLI/SLO/Error Budgets, and Highload Stateful clusters (CloudNativePG, Kafka KRaft Strimzi, ClickHouse Keeper). Use for resilient high-throughput production systems."
category: devops
tags: [observability, sre, prometheus, opentelemetry, pyroscope, postgresql, kafka, clickhouse]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
language: ru
original: observability-sre-highload
author: ssrjkk
---
# Observability, SRE & Highload Stateful Infrastructure (Наблюдаемость, SRE и Highload БД)

> Четыре столпа телеметрии (метрики, логи, трейсы, eBPF-профилирование), контроль Error Budget и отказоустойчивые кластеры БД.

## Быстрый старт
```bash
# Deploy OpenTelemetry + Pyroscope eBPF profiler, HA CloudNativePG, and Kafka KRaft
kubectl apply -f labs/nextgen_2027_pack/otel-collector-and-pyroscope.yaml
kubectl apply -f labs/baremetal_and_ha_db_pack/cloudnativepg-ha-cluster.yaml
kubectl apply -f labs/baremetal_and_ha_db_pack/kafka-kraft-strimzi.yaml
```

```promql
# Multi-window RED 5xx error percentage over 5 minutes
sum(rate(http_requests_total{job="backend-api",status=~"5.."}[5m]))
/
sum(rate(http_requests_total{job="backend-api"}[5m])) * 100
```

## Когда использовать
- Построение единого контура наблюдаемости со связкой метрик VictoriaMetrics, логов Vector/Loki, трейсов Tempo и профилей Pyroscope по trace_id
- Автоматический сбор RED-метрик и распределенных трейсов без правок кода через eBPF-агент Grafana Beyla
- Внедрение SRE-процессов: расчет SLI/SLO, контроль выгорания Error Budget и проведение Blameless Postmortems
- Эксплуатация отказоустойчивых кластеров PostgreSQL 16 (CloudNativePG), Apache Kafka в режиме KRaft (Strimzi) и аналитических витрин ClickHouse

## Лучшие практики
- Никогда не добавляйте высококардинальные поля (user_id, email, request_id, IP) в лейблы Prometheus или Loki — храните их в теле JSON-лога.
- Прокидывайте trace_id в каждую строку JSON-лога для мгновенного перехода из лога Loki в трейс Tempo и профиль CPU Pyroscope.
- Настраивайте пейджинг дежурного по скорости выгорания Error Budget (Burn Rate) и симптомам деградации, а не по разовым всплескам CPU.
- Разворачивайте CloudNativePG минимум на 3 реплики в разных зонах доступности с пулером PgBouncer (transaction mode) и архивацией WAL в S3.
- Запускайте новые кластеры Apache Kafka исключительно в режиме KRaft (без ZooKeeper) через оператор Strimzi с выгрузкой холодных сегментов в S3.
- Используйте легковесный ClickHouse Keeper на C++ вместо тяжелого JVM ZooKeeper для координации таблиц ReplicatedMergeTree.

## Зависимости
```bash
# Install VictoriaMetrics, Loki, OpenTelemetry Operator, and CloudNativePG Helm charts
helm repo add cnpg https://cloudnative-pg.github.io/charts
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
```

## Примеры
```python
# Compute monthly SLO downtime budget in minutes and allowed 5xx error count
def calc_error_budget(slo_percent: float, monthly_requests: int) -> dict:
    error_fraction = (100.0 - slo_percent) / 100.0
    downtime_minutes = round(30 * 24 * 60 * error_fraction, 2)
    allowed_failures = int(monthly_requests * error_fraction)
    return {"slo": slo_percent, "downtime_min": downtime_minutes, "allowed_5xx": allowed_failures}

assert calc_error_budget(99.9, 100_000_000) == {"slo": 99.9, "downtime_min": 43.2, "allowed_5xx": 100000}
```

```yaml
# CloudNativePG 3-node HA PostgreSQL 16 cluster with S3 WAL backup and Prometheus monitoring
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: pg-production-ha
  namespace: databases
spec:
  instances: 3
  imageName: ghcr.io/cloudnative-pg/postgresql:16.4
  storage:
    storageClass: local-nvme-topolvm
    size: 200Gi
  monitoring:
    enablePodMonitor: true
```

## Пошаговое руководство
1. Разверните OpenTelemetry Collector с процессорами memory_limiter и batch для приема OTLP-метрик и трейсов.
2. Поднимите DaemonSet-агенты Grafana Beyla и Pyroscope для eBPF-трассировки без правок кода и построения FlameGraph-профилей.
3. Настройте сбор JSON-логов через Vector в Grafana Loki с очисткой высококардинальных меток.
4. Зафиксируйте целевые SLI/SLO и настройте многооконные алерты на выгорание Error Budget в Alertmanager.
5. Разверните кластер PostgreSQL 16 из 3 узлов под управлением CloudNativePG с пулером PgBouncer и непрерывным бэкапом WAL в S3.
6. Запустите кластер Apache Kafka в режиме KRaft через оператор Strimzi с разделением пулов controller и broker.
7. Проверьте время автоматического переключения мастера (RTO < 10 с) через эксперимент pod-kill в Chaos Mesh.

## Валидация
1. В Grafana работает сквозной переход от метрик и логов Loki к трейсам Tempo и профилям Pyroscope по общему trace_id
2. Аудит кардинальности Prometheus подтверждает отсутствие безразмерных меток (user_id, ip, request_id) в индексах
3. При удалении мастер-пода CloudNativePG реплика автоматически становится новым мастером быстрее чем за 10 секунд без потери данных
4. Кластер Strimzi Kafka работает в режиме KRaft без подов ZooKeeper при нулевом количестве недореплицированных партиций

## Устранение неполадок
- Падение Prometheus или Loki по OOM из-за взрыва кардинальности — удалите динамические поля (UUID в URL, user_id) из labels через relabel_configs.
- Исчерпание max_connections в PostgreSQL на пике нагрузки — переключите сервисы на подключение через пулер PgBouncer в режиме transaction.
- Миграция ALTER TABLE заблокировала все чтение таблицы — всегда задавайте SET lock_timeout = '2s' перед выполнением DDL-миграций.
- Постоянный рост Consumer Lag в Kafka — убедитесь, что число партиций топика не меньше числа подов-консьюмеров в группе.
