---
name: sqlite
description: "Use SQLite for embedded relational storage: schema, WAL mode, transactions, indexing, and performance. Use for local and mobile data layers."
category: database
tags: [sqlite, database, embedded, local-storage, wal, transactions]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# SQLite

> Embedded relational storage with SQLite.

## Quick Start
```bash
sqlite3 app.db
CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT UNIQUE);
INSERT INTO users (email) VALUES ('a@b.com');
```

## When to Use
- Local/desktop/mobile storage
- Single-machine apps with small data
- Prototypes and embedded tools
- Read-heavy offline datasets

## Best Practices

### Schema
- Use INTEGER PRIMARY KEY or explicit rowid
- Prefer TEXT for dates (ISO) or REAL for timestamps
- Add UNIQUE and CHECK constraints
- Use `STRICT` tables (SQLite 3.37+) for typed data

### Concurrency
- Enable WAL mode for concurrent readers
- Use short write transactions
- Set `busy_timeout` to avoid SQLITE_BUSY
- Avoid long-running read transactions

### Performance
- Index columns used in WHERE/JOIN
- Use `PRAGMA` to tune (cache_size, mmap)
- Batch writes in transactions
- `VACUUM` periodically to reclaim space

### Durability
- Choose journal mode by need (WAL vs DELETE)
- Set `synchronous=NORMAL` in WAL for speed
- Back up via `.backup` or VACUUM INTO
- Test on the target filesystem

## Dependencies
```bash
sqlite3  # CLI
# Python: sqlite3 stdlib
```

## Examples
```sql
-- WAL and busy timeout
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=5000;
```
```sql
-- Schema with constraints
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  role TEXT NOT NULL DEFAULT 'member'
  CHECK (role IN ('member','admin'))
);
CREATE INDEX idx_users_role ON users(role);
```
```python
# Python usage with transactions
import sqlite3

conn = sqlite3.connect("app.db")
conn.execute("PRAGMA journal_mode=WAL")
with conn:
    conn.execute("INSERT INTO users (email, role) VALUES (?, ?)", ("a@b.com", "admin"))
for row in conn.execute("SELECT * FROM users"):
    print(row)
```
```python
# Batch writes in one transaction
with conn:
    conn.executemany(
        "INSERT INTO logs (ts, msg) VALUES (?, ?)",
        [(1, "a"), (2, "b"), (3, "c")],
    )
```

## Step-by-Step
1. Choose file location and open with pragmas (WAL).
2. Create schema with constraints and indexes.
3. Write with short transactions and `busy_timeout`.
4. Query with parameters to avoid injection.
5. Tune cache and synchronous for the workload.
6. Back up with `.backup`/`VACUUM INTO`.
7. Vacuum and re-analyze periodically.
8. Test concurrency on the target platform.

## Validation
1. Writes and reads are consistent
2. Concurrent reads work in WAL mode
3. No SQLITE_BUSY under expected load
4. Queries use indexes (EXPLAIN QUERY PLAN)
5. Backup restores correctly

## Troubleshooting
- SQLITE_BUSY: raise busy_timeout, shorten transactions.
- Database locked: check for open long transactions.
- Slow queries: add indexes; check `EXPLAIN QUERY PLAN`.