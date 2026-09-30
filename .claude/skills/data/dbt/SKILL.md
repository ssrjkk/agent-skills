---
name: dbt
description: "Build analytics engineering workflows with dbt: models, tests, sources, macros, and documentation. Use for transform-layer data pipelines."
category: data
tags: [dbt, analytics, data-engineering, models, sql, testing, warehouse]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# dbt

> Transform-layer analytics engineering with dbt.

## Quick Start
```bash
pip install dbt-postgres
dbt init my_project
dbt run
```

## When to Use
- SQL-based transformation pipelines
- Data warehouse modeling (staging, marts)
- Testing and documenting data models
- Version-controlled analytics code

## Best Practices

### Project Structure
- Use layers: staging, intermediate, marts
- Model per grain; clear naming
- Use `ref()` for dependencies
- Keep models small and focused

### Modeling
- Build incremental models with `incremental_strategy`
- Use materialized views for base layers
- Deduplicate and type-cast in staging
- Add surrogate keys for dims

### Tests & Quality
- Add singular and generic tests
- Test primary keys, nulls, and relationships
- Use freshness tests on sources
- Gate merges on test pass

### Documentation
- Document models, columns, and sources
- Use `dbt docs generate` for the docs site
- Add `description` to every model
- Keep lineage clean

## Dependencies
```bash
pip install dbt-postgres dbt-bigquery
dbt init my_project
```

## Examples
```yaml
# dbt_project.yml
name: analytics
profile: default
model-paths: ["models"]
tests:
  +store_failures: true
```
```sql
-- models/staging/stg_orders.sql
SELECT
  id AS order_id,
  customer_id,
  amount,
  status,
  created_at
FROM {{ source('raw', 'orders') }}
WHERE status IS NOT NULL
```
```sql
-- models/marts/fct_orders.sql
SELECT
  customer_id,
  SUM(amount) AS lifetime_value,
  COUNT(*) AS order_count
FROM {{ ref('stg_orders') }}
GROUP BY 1
```
```yaml
# models/marts/schema.yml
version: 2
models:
  - name: fct_orders
    columns:
      - name: customer_id
        tests: [not_null]
```

## Step-by-Step
1. Initialize the project and configure the profile.
2. Define sources for raw tables.
3. Build staging models (clean, typed).
4. Build intermediate and mart models with `ref()`.
5. Add tests for keys, nulls, and freshness.
6. Add incremental strategies for large tables.
7. Document models and columns.
8. Run `dbt run && dbt test` in CI.

## Validation
1. `dbt run` succeeds
2. `dbt test` passes with no failures
3. Models build in dependency order
4. Incremental models only process new data
5. Docs generate with lineage

## Troubleshooting
- Test failures: fix the data or the model logic.
- Slow runs: add incremental and narrow the models.
- Dependency cycles: refactor model references.