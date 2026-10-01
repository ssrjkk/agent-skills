---
name: clickhouse
description: "Design and operate ClickHouse for OLAP analytics: columnar tables, engines, aggregations, partitioning, and performance. Use for analytics workloads."
category: database
tags: [clickhouse, olap, columnar, analytics, aggregations, partitioning]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# ClickHouse

> Columnar OLAP analytics with ClickHouse.

## Quick Start
```bash
docker run -p 8123:8123 -d clickhouse/clickhouse-server
clickhouse-client
```

## When to Use
- High-volume analytics and reporting
- Aggregations over large event datasets
- Timeseries and log analysis
- Dashboards and BI backends

## Best Practices

### Schema
- Use columnar MergeTree engines
- Choose the right engine (MergeTree, Replacing, Summing)
- Use LowCardinality for low-cardinality strings
- Pick types deliberately (DateTime, UInt, Float64)

### Partitioning & Order
- Partition by time for retention and scans
- Set ORDER BY to match filter/sort patterns
- Use TTL for data lifecycle
- Keep partitions balanced in size

### Querying
- Aggregate with GROUP BY; use materialized views
- Filter early; avoid SELECT * on wide tables
- Use sampling for very large results
- Leverage `argMax`, `uniq`, and `quantile` functions

### Operations
- Monitor disk, CPU, and query performance
- Use `system.query_log` for diagnostics
- Back up parts and metadata
- Distribute with Distributed tables when needed

## Dependencies
```bash
docker run -p 8123:8123 -d clickhouse/clickhouse-server
# Python: pip install clickhouse-connect
```

## Examples
```sql
-- Columnar table with TTL and partition
CREATE TABLE events (
  ts DateTime,
  user_id UInt64,
  action LowCardinality(String),
  value Float64
) ENGINE = MergeTree
PARTITION BY toYYYYMM(ts)
ORDER BY (user_id, ts)
TTL toDateTime(ts) + INTERVAL 90 DAY;
```
```sql
-- Aggregation query
SELECT
  toDate(ts) AS day,
  uniq(user_id) AS active_users,
  sum(value) AS total
FROM events
WHERE ts >= now() - INTERVAL 7 DAY
GROUP BY day
ORDER BY day;
```
```sql
-- Quantiles and argMax
SELECT
  quantile(0.95)(value) AS p95,
  argMax(action, ts) AS last_action
FROM events;
```
```python
import clickhouse_connect

client = clickhouse_connect.get_client(host="localhost", port=8123)
rows = client.query("SELECT count() FROM events").result_rows
print(rows)
```

## Step-by-Step
1. Choose the MergeTree engine and table layout.
2. Set partitioning and ORDER BY for access patterns.
3. Add TTL for retention.
4. Write aggregations with the right functions.
5. Add materialized views for hot aggregations.
6. Monitor query_log and disk.
7. Tune max_threads and memory.
8. Back up and plan scaling.

## Validation
1. Aggregations return correct results
2. Queries scan minimal partitions
3. TTL removes expired data
4. Query latency within budget at scale
5. Backups restore correctly

## Troubleshooting
- Slow queries: check partitions scanned and ORDER BY.
- High disk: adjust TTL and partition size.
- Memory errors: lower max_memory_usage or optimize queries.