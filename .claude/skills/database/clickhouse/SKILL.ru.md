---
name: clickhouse
description: "Design and operate ClickHouse for OLAP analytics: columnar tables, engines, aggregations, partitioning, and performance. Use for analytics workloads."
category: database
tags: [clickhouse, database, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: clickhouse
author: ssrjkk
---
# ClickHouse (КликХаус)

> Колоночная OLAP-аналитика на ClickHouse.

## Быстрый старт
```bash
docker run -p 8123:8123 -d clickhouse/clickhouse-server
clickhouse-client
```

## Когда использовать
- Аналитика и отчёты больших объёмов
- Агрегации по большим event-датасетам
- Анализ таймсерий и логов
- Бэкенды дашбордов и BI

## Лучшие практики

### Схема
- Колоночные MergeTree-движки
- Правильный движок (MergeTree, Replacing, Summing)
- LowCardinality для строк с низкой кардинальностью
- Осознанные типы (DateTime, UInt, Float64)

### Партиции и порядок
- Партиции по времени для retention и сканов
- ORDER BY под фильтры/сортировки
- TTL для жизненного цикла данных
- Сбалансированные по размеру партиции

### Запросы
- Агрегация GROUP BY; materialized views
- Фильтруйте рано; без SELECT * на широких таблицах
- Сэмплинг для очень больших результатов
- `argMax`, `uniq`, `quantile` функции

### Операции
- Мониторьте диск, CPU и производительность запросов
- `system.query_log` для диагностики
- Бэкапы партов и метаданных
- Распределение через Distributed tables

## Зависимости
```bash
docker run -p 8123:8123 -d clickhouse/clickhouse-server
# Python: pip install clickhouse-connect
```

## Примеры
```sql
-- Колоночная таблица с TTL и партициями
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
-- Агрегационный запрос
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
-- Квантили и argMax
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

## Пошаговое руководство
1. Выберите MergeTree-движок и layout таблицы.
2. Задайте партиционирование и ORDER BY под паттерны доступа.
3. Добавьте TTL для retention.
4. Пишите агрегации с правильными функциями.
5. Добавьте materialized views для горячих агрегаций.
6. Мониторьте query_log и диск.
7. Настройте max_threads и память.
8. Бэкапы и план масштабирования.

## Валидация
1. Агрегации возвращают корректные результаты
2. Запросы сканируют минимум партиций
3. TTL удаляет устаревшие данные
4. Задержка запросов в рамках бюджета в масштабе
5. Бэкапы восстанавливаются корректно

## Устранение неполадок
- Медленные запросы: проверьте сканируемые партиции и ORDER BY.
- Высокий диск: настройте TTL и размер партиций.
- Ошибки памяти: снизьте max_memory_usage или оптимизируйте запросы.