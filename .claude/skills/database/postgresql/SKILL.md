---
name: postgresql
description: "Design and operate PostgreSQL databases: schema design, indexing, query optimization, transactions, and migrations. Use for any relational data layer."
category: database
tags: [postgresql, sql, database, indexing, transactions, migrations, relational]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-20
updated: 2026-09-28
author: ssrjkk
---
# PostgreSQL

> Designing and operating reliable PostgreSQL databases.

## Quick Start
```bash
docker run --name pg -e POSTGRES_PASSWORD=secret -p 5432:5432 -d postgres:17
psql -h localhost -U postgres
# CREATE DATABASE app;
```

## When to Use
- Relational data with strong consistency needs
- Transactions and complex joins
- Full-text search, JSONB, and geospatial (PostGIS)
- Analytics via materialized views and window functions

## Best Practices

### Schema Design
- Use proper types (uuid, timestamptz, jsonb) — avoid text-only columns
- Add foreign keys and constraints to enforce integrity
- Prefer normalized core; denormalize only for known hot reads
- Name tables in plural or singular consistently; use snake_case

### Indexing
- Index columns used in WHERE, JOIN, ORDER BY
- Prefer B-tree for equality/range; GIN for JSONB/arrays; BRIN for huge tables
- Create composite indexes matching query column order
- Remove unused indexes; analyze with `pg_stat_user_indexes`

### Performance
- Use `EXPLAIN (ANALYZE, BUFFERS)` to read plans
- Avoid `SELECT *`; fetch only needed columns
- Batch inserts with `COPY` or multi-row VALUES
- Use connection pooling (PgBouncer) in production

## Dependencies
```bash
docker run --name pg -e POSTGRES_PASSWORD=secret -p 5432:5432 -d postgres:17
# psql client:  psql -h localhost -U postgres
```

## Examples
```sql
-- Schema with types, constraints, and indexes
CREATE TABLE users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email text NOT NULL UNIQUE,
  role text NOT NULL DEFAULT 'member',
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_users_created ON users (created_at DESC);
```
```sql
-- Query optimization with EXPLAIN
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, email FROM users
WHERE created_at > now() - interval '7 days'
ORDER BY created_at DESC
LIMIT 50;
```
```sql
-- Window function for analytics
SELECT
  category,
  revenue,
  RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rnk
FROM monthly_sales;
```
```sql
-- JSONB querying with GIN index
CREATE INDEX idx_meta ON orders USING gin (meta);
SELECT id FROM orders WHERE meta @> '{"status": "paid"}';
```

## Step-by-Step
1. Model entities and relationships; decide types for each column.
2. Write the DDL with constraints (PK, FK, UNIQUE, NOT NULL).
3. Add indexes for the query patterns you actually use.
4. Write migrations (Alembic/Prisma/Flyway) and version them.
5. Load representative data and run `EXPLAIN (ANALYZE)` on hot queries.
6. Tune indexes and queries; add pooling for production.
7. Set up backups (pg_dump/WAL archiving) and a restore drill.
8. Monitor slow queries via `pg_stat_statements` and set alerts.

## Validation
1. Schema applies cleanly via migrations
2. Constraints reject invalid data
3. Hot queries run within target latency
4. `EXPLAIN` shows index usage on large tables
5. Backup and restore verified in staging

## Troubleshooting
- Slow query despite index: check composite index column order and `= NULL`.
- Lock waits: long transactions hold locks — keep them short.
- High memory: raise `shared_buffers` and `effective_cache_size` carefully.