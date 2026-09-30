---
name: loki
description: "Operate log aggregation with Grafana Loki: agents, labels, queries (LogQL), retention, and dashboards. Use for log observability."
category: devops
tags: [loki, logging, logql, grafana, log-aggregation, retention]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Grafana Loki

> Log aggregation and querying with Loki.

## Quick Start
```bash
# single binary or docker compose with promtail + loki
docker run -p 3100:3100 -d grafana/loki:latest -config.file=/etc/loki/local-config.yaml
```

## When to Use
- Centralized log storage and querying
- Correlation with Prometheus metrics
- Log-based alerting
- Kubernetes pod logs at scale

## Best Practices

### Agents & Shipping
- Use Promtail or Alloy to ship logs
- Add structured labels (app, namespace, level)
- Keep label cardinality low
- Parse log lines into fields with pipelines

### Labels & Indexing
- Label by identifiers, not values (avoid explosion)
- Store high-cardinality fields as log content
- Use structured parsing (json, logfmt) in pipelines
- Streams keyed by label sets

### Querying (LogQL)
- Filter with `|=`, `|~`, `|json`, `|logfmt`
- Aggregate with range functions (`rate`, `count_over_time`)
- Use `{app="api"} |= "error" | json`
- Combine with PromQL metrics for correlation

### Operations
- Set retention and enforce limits
- Monitor ingestion and query latency
- Configure storage (filesystem/object store)
- Back up configuration and dashboards

## Dependencies
```bash
docker run -p 3100:3100 -d grafana/loki:latest -config.file=/etc/loki/local-config.yaml
# agent: promtail / alloy
```

## Examples
```yaml
# Promtail config
scrape_configs:
  - job_name: app
    static_configs:
      - targets: [localhost]
        labels:
          job: app
          __path__: /var/log/app/*.log
```
```logql
# Filter and count errors per minute
sum(rate({job="app"} |= "error" [1m])) by (level)
```
```logql
# Parse JSON and filter by field
{job="api"} | json | level="error" | message=~"timeout.*"
```
```yaml
# Loki limits
limits_config:
  retention_period: 720h
  max_query_lookback: 720h
  ingestion_rate_mb: 8
```

## Step-by-Step
1. Deploy Loki (single binary or HA).
2. Configure Promtail/Alloy to ship logs.
3. Set low-cardinality labels.
4. Add structured parsing pipelines.
5. Write LogQL queries for debugging and dashboards.
6. Add log-based alerts.
7. Set retention and limits.
8. Correlate logs with metrics in Grafana.

## Validation
1. Logs appear in Loki within expected latency
2. LogQL returns correct filtered results
3. Label cardinality stays low
4. Retention enforces the policy
5. Dashboards render logs with metrics

## Troubleshooting
- No logs: check Promtail targets and paths.
- Cardinality explosion: move high-cardinality values into log content.
- Slow queries: narrow label sets and time ranges.