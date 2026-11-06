# Карта 10: Эксплуатация и Траблшутинг Баз Данных (PostgreSQL, Redis, Kafka)

DevOps и SRE инженеру регулярно приходится диагностировать деградацию БД, настраивать пулеры соединений и проверять бэкапы.

---

## 1. PostgreSQL: Диагностика в реальном времени (SQL-шпаргалка дежурного)

### Поиск зависших и долгих запросов (атака клонов / тяжелые аналитические запросы)
```sql
SELECT pid, now() - pg_stat_activity.query_start AS duration, usename, state, wait_event_type, query
FROM pg_stat_activity
WHERE state != 'idle'
  AND (now() - pg_stat_activity.query_start) > interval '5 seconds'
ORDER BY duration DESC;
```
- **Мягко отменить запрос:** `SELECT pg_cancel_backend(<pid>);`
- **Жестко убить сессию (если не помогло):** `SELECT pg_terminate_backend(<pid>);`

### Поиск блокировок (Кто кого держит в Lock Queue)
Частая причина зависания миграций (`ALTER TABLE`), которые берут `ACCESS EXCLUSIVE` лок и встают в очередь за длинной транзакцией `idle in transaction`:
```sql
SELECT
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS current_statement_in_blocking_process
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

### Проверка раздувания таблиц (Bloat) и работы Autovacuum
```sql
SELECT relname, n_live_tup, n_dead_tup,
       round(n_dead_tup::numeric / nullif(n_live_tup + n_dead_tup, 0) * 100, 2) AS dead_pct,
       last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC LIMIT 15;
```

---

## 2. Архитектура отказоустойчивого PostgreSQL в K8s и на VM

### CloudNativePG (CNPG) — стандарт оператора для Kubernetes
Вместо ручной настройки StatefulSet используется оператор **CloudNativePG**:
- Управляет Primary и Standby репликами напрямую через Kubernetes API (без внешнего Consul/etcd для лидера).
- Из коробки поднимает пулер **PgBouncer** (`Pooler` CRD), экспортирует метрики для Prometheus и стримит WAL-архивы в S3 через Barman Cloud.

### Золотые правила настройки PgBouncer:
- **`pool_mode = transaction`** — соединение с реальным Postgres выдается клиенту только на время выполнения одной транзакции, позволяя держать 5 000 подключений от микросервисов на 50 реальных процессах Postgres (`default_pool_size = 50`).
- **Важный нюанс:** в режиме `transaction` приложению нужно явно включить поддержку протокола подготовленных выражений в самом PgBouncer (`max_prepared_statements = 200` в современных версиях PgBouncer 1.21+).

---

## 3. Redis / Valkey в продакшене
- **Почему `KEYS *` убивает продакшн:** Redis однопоточен для выполнения команд. Вызов `KEYS *` на базе с миллионами ключей блокирует основной поток на несколько секунд, вызывая таймауты у всех клиентов. Всегда используй итератор `SCAN 0 MATCH prefix:* COUNT 100`.
- **Политика вытеснения памяти (`maxmemory-policy`):**
  - Если Redis используется как **кэш**: ставь `allkeys-lru` или `volatile-lfu`.
  - Если Redis используется как **брокер очередей (Celery/BullMQ)**: ставь `noeviction` (чтобы задачи не удалялись тихо при нехватке RAM).

---

## 4. Apache Kafka: На что смотреть при деградации
1. **`UnderReplicatedPartitions > 0`** — один из брокеров отстает или упал, риск потери данных при отказе лидера.
2. **`Consumer Lag` растет** — воркеры-консьюмеры не успевают разгребать сообщения.
   - **Решение:** увеличить число подов-консьюмеров (но помни: число активных консьюмеров в одной Consumer Group **не может превышать число партиций** в топике — лишние поды будут просто простаивать!).
