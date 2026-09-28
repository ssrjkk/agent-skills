---
name: redis
description: "Use Redis for caching, sessions, queues, rate limiting, and pub/sub: data structures, persistence, eviction, and clustering. Use for any high-performance data layer."
category: database
tags: [redis, cache, sessions, queues, pubsub, rate-limiting, in-memory]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-20
updated: 2026-09-28
author: ssrjkk
---
# Redis

> High-performance in-memory data store for caching and real-time workloads.

## Quick Start
```bash
docker run --name redis -p 6379:6379 -d redis:7
redis-cli ping  # PONG
```

## When to Use
- Caching hot reads in front of a database
- Session storage and rate limiting
- Queues and pub/sub for decoupling
- Real-time counters, leaderboards, and distributed locks

## Best Practices

### Data Modeling
- Pick the right structure: STRING, HASH, LIST, SET, ZSET
- Use HASH for objects; ZSET for ranked data; SET for uniqueness
- Use short, prefixed keys: `app:user:123:profile`
- Set TTLs on cache keys; avoid unbounded growth

### Caching
- Cache-aside: read cache, on miss load DB and populate
- Use `SET NX EX` for locks; Lua scripts for atomicity
- Choose eviction policy (allkeys-lru) and maxmemory
- Invalidate on write or use short TTLs with write-through

### Reliability
- Enable AOF or RDB persistence for durability
- Use Redis Cluster or Sentinel for HA in production
- Set `maxmemory` and monitor `INFO memory`
- Never store secrets or PII with long TTLs

## Dependencies
```bash
docker run --name redis -p 6379:6379 -d redis:7
# Python client
pip install redis
```

## Examples
```python
import redis

r = redis.Redis.from_url("redis://localhost:6379/0")

# Cache-aside pattern
def get_user(user_id: str):
    key = f"app:user:{user_id}:profile"
    cached = r.get(key)
    if cached:
        return cached
    profile = db.fetch_user(user_id)   # slow path
    r.set(key, profile, ex=300)
    return profile
```
```python
# Rate limiting with INCR + EXPIRE (token bucket style)
def rate_limit(user_id: str, limit: int = 10, window: int = 60) -> bool:
    key = f"rate:{user_id}:{int(time.time() // window)}"
    count = r.incr(key)
    if count == 1:
        r.expire(key, window)
    return count <= limit
```
```python
# Distributed lock with Lua
unlock = r.register_script("""
if redis.call('get', KEYS[1]) == ARGV[1] then
  return redis.call('del', KEYS[1])
else
  return 0
end
""")

lock_key = "app:lock:checkout"
token = "uuid-123"
r.set(lock_key, token, nx=True, ex=10)
# ... critical section ...
unlock(keys=[lock_key], args=[token])
```
```python
# Pub/Sub
pubsub = r.pubsub()
pubsub.subscribe("events")
for message in pubsub.listen():
    print(message["data"])
r.publish("events", "user:created")
```

## Step-by-Step
1. Choose the data structures matching your access patterns.
2. Define key naming and TTL strategy up front.
3. Implement cache-aside or write-through for hot data.
4. Add rate limiting and distributed locks where shared state exists.
5. Configure persistence (AOF) and eviction policy.
6. Set up Cluster/Sentinel for production availability.
7. Monitor `INFO`, slowlog, and memory usage; alert on thresholds.
8. Add health checks and failover drills.

## Validation
1. `redis-cli ping` returns PONG
2. Cache hits return instantly; misses populate correctly
3. TTLs expire keys as expected
4. Locks release after timeout even on crash
5. No out-of-memory with maxmemory + eviction configured

## Troubleshooting
- Key evicted too early: raise maxmemory or use different eviction policy.
- Stale cache: align invalidation with writes or shorten TTL.
- Single point of failure: enable Sentinel or Cluster.