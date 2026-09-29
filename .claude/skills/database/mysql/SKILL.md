---
name: mysql
description: "Design and operate MySQL: schema, InnoDB tuning, indexing, transactions, replication, and query optimization. Use for relational workloads."
category: database
tags: [mysql, database, innodb, indexing, transactions, replication, sql]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# MySQL

> Designing and operating MySQL databases.

## Quick Start
```bash
docker run --name mysql -e MYSQL_ROOT_PASSWORD=secret -p 3306:3306 -d mysql:8
mysql -h 127.0.0.1 -u root -p
```

## When to Use
- Relational data with strong consistency
- Web application backends (read-heavy)
- Transactions and standard SQL
- Proven operational tooling

## Best Practices

### Schema
- Use InnoDB (default) for transactions and FK
- Choose column types deliberately (INT, VARCHAR, DATETIME)
- Use utf8mb4 for full Unicode
- Normalize core; denormalize for hot reads

### Indexing
- Index columns used in WHERE/JOIN/ORDER BY
- Leftmost-prefix rule for composite indexes
- Cover frequently used columns to avoid lookups
- Avoid functions on indexed columns in WHERE

### Performance
- Use `EXPLAIN` to read query plans
- Batch inserts; avoid row-by-row in loops
- Set `innodb_buffer_pool_size` for cache
- Use connection pooling in apps

### Operations
- Enable binary logging for replication/backup
- Use a replica for reads when needed
- Set `max_connections` and monitor slow queries
- Back up with mysqldump or Percona tools

## Dependencies
```bash
docker run --name mysql -e MYSQL_ROOT_PASSWORD=secret -p 3306:3306 -d mysql:8
# client: mysql -h 127.0.0.1 -u root -p
```

## Examples
```sql
-- Schema with types and indexes
CREATE TABLE users (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'member',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_email (email),
  KEY idx_created (created_at)
) ENGINE=InnoDB;
```
```sql
-- Transaction with rollback safety
START TRANSACTION;
INSERT INTO orders (user_id, amount) VALUES (1, 99.99);
UPDATE users SET balance = balance - 99.99 WHERE id = 1;
COMMIT; -- or ROLLBACK on error
```
```sql
-- EXPLAIN to verify index usage
EXPLAIN SELECT id, email FROM users
WHERE created_at >= '2026-01-01' ORDER BY created_at LIMIT 50;
```
```sql
-- Batch insert
INSERT INTO logs (ts, level, msg) VALUES
  ('2026-09-01', 'info', 'a'),
  ('2026-09-01', 'warn', 'b');
```

## Step-by-Step
1. Model entities; choose column types and charset.
2. Write DDL with keys, indexes, and constraints.
3. Migrate with a versioned tool (Flyway/Alembic).
4. Add indexes for real query patterns.
5. Run `EXPLAIN` on hot queries.
6. Tune InnoDB and connection pooling.
7. Set up replication and backups.
8. Monitor slow queries and lock waits.

## Validation
1. Schema applies cleanly via migrations
2. `EXPLAIN` shows index usage
3. Transactions roll back on failure
4. Replica is in sync (for read scaling)
5. Backup/restore tested

## Troubleshooting
- Slow query: check EXPLAIN and composite index order.
- Deadlocks: keep transactions short; consistent lock order.
- High load: buffer pool, connection pool, read replicas.