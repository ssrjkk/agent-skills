---
name: observability-sre-highload
description: "Implements full-stack Observability (VictoriaMetrics, Loki, Vector, OpenTelemetry, Beyla eBPF, Pyroscope), SRE SLI/SLO/Error Budgets, and Highload Stateful clusters (CloudNativePG, Kafka KRaft Strimzi, ClickHouse Keeper). Use for resilient high-throughput production systems."
category: devops
tags: [observability, sre, prometheus, opentelemetry, pyroscope, postgresql, kafka, clickhouse]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# Observability, SRE & Highload Stateful Infrastructure

> Unified metrics, logs, traces, and eBPF FlameGraphs paired with SLO burn-rate alerts and HA PostgreSQL, Kafka KRaft, and ClickHouse.

## Quick Start
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

## When to Use
- Building a unified observability stack correlating Prometheus/VictoriaMetrics, Loki/Vector JSON logs, Tempo traces, and Pyroscope eBPF profiles
- Instrumenting legacy or polyglot services without code changes using Grafana Beyla eBPF auto-instrumentation
- Defining SLIs, SLOs (99.9% / 99.95%), Error Budget burn-rate alerts, and Blameless Postmortems
- Operating HA PostgreSQL (CloudNativePG + PgBouncer + WAL-G), ZooKeeper-less Apache Kafka (KRaft on Strimzi), and ClickHouse clusters

## Best Practices
- Never put high-cardinality fields (user_id, email, request_id, IP) into Prometheus or Loki labels; keep them inside structured JSON log fields.
- Include trace_id and span_id in every JSON log line so engineers jump directly from a Loki log entry to a Tempo trace and Pyroscope FlameGraph.
- Alert on symptoms and SLO Error Budget burn rates rather than noisy single-node CPU spikes.
- Deploy CloudNativePG with at least 3 instances spread across availability zones, transaction-mode PgBouncer, and continuous WAL archiving to S3.
- Run Apache Kafka strictly in KRaft mode (no ZooKeeper) with dedicated controller and broker KafkaNodePools and S3 Tiered Storage.
- Use lightweight C++ ClickHouse Keeper instead of ZooKeeper for ReplicatedMergeTree coordination in ClickHouse clusters.

## Dependencies
```bash
# Install VictoriaMetrics, Loki, OpenTelemetry Operator, and CloudNativePG Helm charts
helm repo add cnpg https://cloudnative-pg.github.io/charts
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
```

## Examples
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

## Step-by-Step
1. Deploy OpenTelemetry Collector with batch and memory_limiter processors to receive OTLP traces and metrics.
2. Run Grafana Beyla and Pyroscope eBPF DaemonSets for zero-code RED telemetry and continuous CPU/memory FlameGraphs.
3. Ship container JSON logs via Vector into Grafana Loki, stripping high-cardinality attributes from index labels.
4. Define Availability and Latency SLIs/SLOs and configure multi-window burn-rate alerts in Alertmanager.
5. Deploy a 3-instance CloudNativePG cluster with synchronous quorum replication, PgBouncer Pooler, and S3 PITR backups.
6. Deploy a Strimzi Kafka cluster with kraft: enabled and separate controller/broker KafkaNodePools.
7. Validate failover RTO (< 10 seconds for CloudNativePG primary promotion) using Chaos Mesh pod-kill experiments.

## Validation
1. Grafana correlates metrics, Loki JSON logs, Tempo traces, and Pyroscope profiles via shared trace_id
2. Prometheus cardinality audit confirms zero unbounded labels (user_id, ip, request_id) in time-series indexes
3. Deleting the CloudNativePG primary pod promotes a standby automatically in under 10 seconds with zero data loss
4. Strimzi Kafka KRaft cluster operates with zero ZooKeeper pods and maintains healthy under-replicated partition count (0)

## Troubleshooting
- Prometheus or Loki OOM due to cardinality explosion — drop dynamic labels (user_id, path with UUIDs) in Vector/RelabelConfig.
- PostgreSQL max_connections exhausted during traffic spike — route application traffic through the CloudNativePG PgBouncer Pooler in transaction mode.
- ALTER TABLE hangs all concurrent SELECTs on PostgreSQL — set lock_timeout = '2s' in migrations so DDL fails fast instead of queuing behind long queries.
- Kafka consumer lag growing steadily — verify partition count matches or exceeds consumer pod count in the consumer group.
