---
name: mongodb
description: "Design and operate MongoDB: document modeling, queries, indexes, aggregation, replication, and sharding. Use for flexible NoSQL data."
category: database
tags: [mongodb, nosql, document-db, queries, indexes, aggregation, atlas]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-26
updated: 2026-09-28
author: ssrjkk
---
# MongoDB

> Designing and operating flexible document databases with MongoDB.

## Quick Start
```bash
docker run --name mongo -p 27017:27017 -d mongo:8
mongosh
use app
db.users.insertOne({ name: "Alice", role: "admin" })
```

## When to Use
- Flexible or evolving document schemas
- High write throughput and horizontal scale
- Denormalized data with rich queries
- Prototyping where schema changes fast

## Best Practices

### Document Modeling
- Embed data read together; reference rarely-changed data
- Avoid unbounded arrays (prefer separate collections)
- Design for access patterns, not normalization
- Use `_id` or a unique index as the primary key

### Queries & Indexes
- Create indexes matching filter/sort patterns
- Use compound indexes with correct field order
- Prefer equality filters before range filters
- Monitor with `explain("executionStats")`

### Aggregation
- Use the aggregation pipeline for complex transforms
- Match/filter early, then group/project
- `$lookup` sparingly; prefer embedded data
- Cap stages and memory per pipeline

### Operations
- Use replica sets for HA; shard for scale
- Set `writeConcern` and `readPreference` deliberately
- Enable auth and TLS; never expose without auth
- Back up with mongodump or Atlas cloud backup

## Dependencies
```bash
docker run --name mongo -p 27017:27017 -d mongo:8
# Python driver
pip install pymongo
```

## Examples
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.app
users = db.users

# Create with unique index
users.create_index("email", unique=True)
users.insert_one({"name": "Alice", "email": "alice@example.com", "role": "admin"})
```
```python
# Query with filter and sort
result = users.find({"role": "admin"}).sort("created_at", -1).limit(10)
for user in result:
    print(user["name"])
```
```python
# Aggregation pipeline
pipeline = [
    {"$match": {"status": "paid"}},
    {"$group": {"_id": "$region", "total": {"$sum": "$amount"}}},
    {"$sort": {"total": -1}},
]
for row in db.orders.aggregate(pipeline):
    print(row)
```
```js
// mongosh: explain to verify index use
db.users.find({ email: "alice@example.com" }).explain("executionStats");
```

## Step-by-Step
1. Model documents around your read access patterns.
2. Decide embed vs reference for each relation.
3. Create indexes for the hot queries.
4. Write queries and aggregation pipelines.
5. Verify with `explain()` that indexes are used.
6. Set up a replica set for production.
7. Enable auth and TLS; restrict network exposure.
8. Configure backups and monitor metrics.

## Validation
1. Hot queries use indexes (explain shows IXSCAN)
2. Document model matches the access patterns
3. Aggregation results are correct
4. Replica set has a healthy primary
5. Backup/restore tested in staging

## Troubleshooting
- Slow queries: add/compound indexes; check sort order.
- Unbounded growth: split embedded arrays into collections.
- Connection drops: use connection pooling and retry writes.