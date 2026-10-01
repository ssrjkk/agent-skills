---
name: sql-querying
description: "Write correct and efficient SQL: joins, aggregations, window functions, CTEs, and query optimization. Use for any relational data access."
category: data
tags: [sql, database, queries, joins, aggregations, window-functions, cte]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-25
updated: 2026-09-28
author: ssrjkk
---
# SQL Querying

> Writing correct, efficient SQL for analysis and applications.

## Quick Start
```sql
SELECT status, COUNT(*) AS cnt
FROM orders
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY status
ORDER BY cnt DESC;
```

## When to Use
- Reporting and ad-hoc analysis
- Application data access (ORMs under the hood)
- Data pipelines and ETL validation
- Any time you need relational answers

## Best Practices

### Readability
- Format queries with clear clauses and aliases
- Use CTEs (WITH) to break complex logic into steps
- Name columns meaningfully with aliases
- Add comments for non-obvious business logic

### Correctness
- Know join semantics: INNER vs LEFT vs FULL
- Watch for fan-out: one-to-many joins multiply rows
- Use DISTINCT deliberately, not by reflex
- Handle NULLs in WHERE/aggregations explicitly

### Aggregation
- Aggregate with GROUP BY on non-aggregated columns
- Use window functions for rankings, running totals, deltas
- Filter with HAVING on aggregates, WHERE on rows
- Use COUNT(DISTINCT ...) for unique counts

### Performance
- Only select needed columns
- Filter early with WHERE before joins
- Ensure indexes support filters and joins
- Avoid functions on indexed columns in WHERE

## Dependencies
```bash
# psql (PostgreSQL), sqlite3, or your database client
psql "postgres://localhost/app"
```

## Examples
```sql
-- CTE + window function: top product per category
WITH ranked AS (
  SELECT
    category,
    product,
    revenue,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS rn
  FROM sales
)
SELECT category, product, revenue
FROM ranked
WHERE rn = 1;
```
```sql
-- Running total with window function
SELECT
  date,
  amount,
  SUM(amount) OVER (ORDER BY date) AS running_total
FROM daily_revenue;
```
```sql
-- Join with aggregation, filter early
SELECT c.name, COUNT(o.id) AS orders
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.created_at >= '2026-01-01'
GROUP BY c.name
HAVING COUNT(o.id) > 0
ORDER BY orders DESC;
```
```sql
-- Compare this month vs last month
SELECT
  product,
  SUM(CASE WHEN date_trunc('month', d) = date_trunc('month', CURRENT_DATE)
           THEN amount ELSE 0 END) AS this_month,
  SUM(CASE WHEN date_trunc('month', d) = date_trunc('month', CURRENT_DATE) - INTERVAL '1 month'
           THEN amount ELSE 0 END) AS last_month
FROM revenue
GROUP BY product;
```

## Step-by-Step
1. State the question you need answered in plain language.
2. Identify the tables and the join keys.
3. Write WHERE filters first, then joins, then aggregation.
4. Add GROUP BY / window functions for the desired shape.
5. Format with CTEs if the query is complex.
6. Check correctness on a small sample.
7. Review the plan (EXPLAIN) for obvious inefficiency.
8. Validate the numbers against a known baseline.

## Validation
1. Query returns expected row counts (no fan-out surprises)
2. Aggregations match independent totals
3. NULLs and edge dates handled correctly
4. Runs within target time on production data
5. Results are reproducible

## Troubleshooting
- Duplicate rows: check join fan-out; dedupe keys.
- Slow query: filter earlier, add indexes, simplify.
- Wrong totals: verify join semantics and NULL handling.