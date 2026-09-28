---
name: postgresql
description: "Design and operate PostgreSQL databases: schema design, indexing, query optimization, transactions, and migrations. Use for any relational data layer."
category: database
tags: [postgresql, database, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: postgresql
author: ssrjkk
---
# PostgreSQL (ПостгреСкуэл)

> Проектирование и эксплуатация надёжных баз данных PostgreSQL.

## Быстрый старт
```bash
docker run --name pg -e POSTGRES_PASSWORD=secret -p 5432:5432 -d postgres:17
psql -h localhost -U postgres
# CREATE DATABASE app;
```

## Когда использовать
- Реляционные данные с высокими требованиями к консистентности
- Транзакции и сложные JOIN
- Полнотекстовый поиск, JSONB и геоданные (PostGIS)
- Аналитика через materialized views и оконные функции

## Лучшие практики

### Дизайн схемы
- Используйте корректные типы (uuid, timestamptz, jsonb) — не только text
- Добавляйте внешние ключи и ограничения для целостности
- Предпочитайте нормализованное ядро; денормализуйте только для горячих чтений
- Именуйте таблицы консистентно; используйте snake_case

### Индексы
- Индексируйте колонки из WHERE, JOIN, ORDER BY
- B-tree — для равенства/диапазонов; GIN — для JSONB/массивов; BRIN — для огромных таблиц
- Составные индексы должны совпадать с порядком колонок запроса
- Удаляйте неиспользуемые индексы; анализируйте через `pg_stat_user_indexes`

### Производительность
- Используйте `EXPLAIN (ANALYZE, BUFFERS)` для чтения планов
- Избегайте `SELECT *`; берите только нужные колонки
- Пакетные вставки через `COPY` или multi-row VALUES
- В проде используйте пул соединений (PgBouncer)

## Зависимости
```bash
docker run --name pg -e POSTGRES_PASSWORD=secret -p 5432:5432 -d postgres:17
# psql клиент:  psql -h localhost -U postgres
```

## Примеры
```sql
-- Схема с типами, ограничениями и индексами
CREATE TABLE users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email text NOT NULL UNIQUE,
  role text NOT NULL DEFAULT 'member',
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_users_created ON users (created_at DESC);
```
```sql
-- Оптимизация запроса через EXPLAIN
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, email FROM users
WHERE created_at > now() - interval '7 days'
ORDER BY created_at DESC
LIMIT 50;
```
```sql
-- Оконная функция для аналитики
SELECT
  category,
  revenue,
  RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rnk
FROM monthly_sales;
```
```sql
-- JSONB-запросы с GIN индексом
CREATE INDEX idx_meta ON orders USING gin (meta);
SELECT id FROM orders WHERE meta @> '{"status": "paid"}';
```

## Пошаговое руководство
1. Смоделируйте сущности и связи; выберите тип для каждой колонки.
2. Напишите DDL с ограничениями (PK, FK, UNIQUE, NOT NULL).
3. Добавьте индексы под реальные паттерны запросов.
4. Пишите миграции (Alembic/Prisma/Flyway) и версионируйте их.
5. Загрузите репрезентативные данные и прогоните `EXPLAIN (ANALYZE)` на горячих запросах.
6. Настройте индексы и запросы; в проде добавьте пул соединений.
7. Настройте бэкапы (pg_dump/WAL archiving) и протестируйте восстановление.
8. Мониторьте медленные запросы через `pg_stat_statements` и ставьте алерты.

## Валидация
1. Схема применяется чисто через миграции
2. Ограничения отклоняют невалидные данные
3. Горячие запросы укладываются в целевые задержки
4. `EXPLAIN` показывает использование индексов на больших таблицах
5. Бэкап и восстановление проверены на стейджинге

## Устранение неполадок
- Медленный запрос несмотря на индекс: проверьте порядок колонок составного индекса и `= NULL`.
- Lock waits: длинные транзакции держат блокировки — держите их короткими.
- Высокая память: аккуратно поднимите `shared_buffers` и `effective_cache_size`.