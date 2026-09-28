---
name: redis
description: "Use Redis for caching, sessions, queues, rate limiting, and pub/sub: data structures, persistence, eviction, and clustering. Use for any high-performance data layer."
category: database
tags: [redis, database, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: redis
author: ssrjkk
---
# Redis (Редис)

> Высокопроизводительное in-memory хранилище для кэша и real-time нагрузок.

## Быстрый старт
```bash
docker run --name redis -p 6379:6379 -d redis:7
redis-cli ping  # PONG
```

## Когда использовать
- Кэширование горячих чтений перед базой данных
- Хранилище сессий и rate limiting
- Очереди и pub/sub для развязки сервисов
- Real-time счётчики, лидерборды и распределённые блокировки

## Лучшие практики

### Моделирование данных
- Выбирайте правильную структуру: STRING, HASH, LIST, SET, ZSET
- HASH — для объектов; ZSET — для рейтингов; SET — для уникальности
- Используйте короткие ключи с префиксом: `app:user:123:profile`
- Ставьте TTL на ключи кэша; избегайте неограниченного роста

### Кэширование
- Cache-aside: читайте кэш, при промахе грузите БД и заполняйте
- Для блокировок используйте `SET NX EX`; Lua-скрипты — для атомарности
- Выбирайте политику вытеснения (allkeys-lru) и maxmemory
- Инвалидируйте при записи или используйте короткие TTL с write-through

### Надёжность
- Включайте AOF или RDB персистентность
- В проде используйте Redis Cluster или Sentinel для HA
- Задайте `maxmemory` и мониторьте `INFO memory`
- Никогда не храните секреты или PII с длинными TTL

## Зависимости
```bash
docker run --name redis -p 6379:6379 -d redis:7
# Python клиент
pip install redis
```

## Примеры
```python
import redis

r = redis.Redis.from_url("redis://localhost:6379/0")

# Cache-aside паттерн
def get_user(user_id: str):
    key = f"app:user:{user_id}:profile"
    cached = r.get(key)
    if cached:
        return cached
    profile = db.fetch_user(user_id)   # медленный путь
    r.set(key, profile, ex=300)
    return profile
```
```python
# Rate limiting через INCR + EXPIRE (token bucket)
def rate_limit(user_id: str, limit: int = 10, window: int = 60) -> bool:
    key = f"rate:{user_id}:{int(time.time() // window)}"
    count = r.incr(key)
    if count == 1:
        r.expire(key, window)
    return count <= limit
```
```python
# Распределённая блокировка через Lua
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
# ... критическая секция ...
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

## Пошаговое руководство
1. Выберите структуры данных под ваши паттерны доступа.
2. Определите нейминг ключей и стратегию TTL заранее.
3. Реализуйте cache-aside или write-through для горячих данных.
4. Добавьте rate limiting и распределённые блокировки там, где есть общее состояние.
5. Настройте персистентность (AOF) и политику вытеснения.
6. Настройте Cluster/Sentinel для доступности в проде.
7. Мониторьте `INFO`, slowlog и использование памяти; ставьте алерты.
8. Добавьте health checks и учения по отказоустойчивости.

## Валидация
1. `redis-cli ping` возвращает PONG
2. Cache hits мгновенные; промахи корректно заполняются
3. TTL истекают ключи как ожидается
4. Блокировки освобождаются по таймауту даже при падении
5. Нет out-of-memory при настроенных maxmemory + eviction

## Устранение неполадок
- Ключ вытеснен слишком рано: поднимите maxmemory или смените политику.
- Stale cache: согласуйте инвалидацию с записью или укоротите TTL.
- Единая точка отказа: включите Sentinel или Cluster.