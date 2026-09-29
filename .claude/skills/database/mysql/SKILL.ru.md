---
name: mysql
description: "Design and operate MySQL: schema, InnoDB tuning, indexing, transactions, replication, and query optimization. Use for relational workloads."
category: database
tags: [mysql, database, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: mysql
author: ssrjkk
---
# MySQL (МайСэсКьюЭл)

> Проектирование и эксплуатация баз MySQL.

## Быстрый старт
```bash
docker run --name mysql -e MYSQL_ROOT_PASSWORD=secret -p 3306:3306 -d mysql:8
mysql -h 127.0.0.1 -u root -p
```

## Когда использовать
- Реляционные данные с сильной консистентностью
- Веб-бэкенды (read-heavy)
- Транзакции и стандартный SQL
- Проверенный операционный тулинг

## Лучшие практики

### Схема
- InnoDB (дефолт) для транзакций и FK
- Типы колонок осознанно (INT, VARCHAR, DATETIME)
- utf8mb4 для полного Unicode
- Нормализуйте ядро; денормализуйте для горячих чтений

### Индексы
- Индексы под WHERE/JOIN/ORDER BY
- Правило левого префикса для составных
- Покрывающие колонки против lookups
- Без функций на индексированных колонках в WHERE

### Производительность
- `EXPLAIN` для чтения планов
- Батч-вставки; не по строкам в циклах
- `innodb_buffer_pool_size` под кэш
- Пул соединений в приложениях

### Операции
- Binary logging для репликации/бэкапа
- Реплика для чтений при необходимости
- `max_connections` и мониторинг медленных запросов
- Бэкапы через mysqldump или Percona tools

## Зависимости
```bash
docker run --name mysql -e MYSQL_ROOT_PASSWORD=secret -p 3306:3306 -d mysql:8
# клиент: mysql -h 127.0.0.1 -u root -p
```

## Примеры
```sql
-- Схема с типами и индексами
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
-- Транзакция с откатом
START TRANSACTION;
INSERT INTO orders (user_id, amount) VALUES (1, 99.99);
UPDATE users SET balance = balance - 99.99 WHERE id = 1;
COMMIT; -- или ROLLBACK при ошибке
```
```sql
-- EXPLAIN для проверки индексов
EXPLAIN SELECT id, email FROM users
WHERE created_at >= '2026-01-01' ORDER BY created_at LIMIT 50;
```
```sql
-- Батч-вставка
INSERT INTO logs (ts, level, msg) VALUES
  ('2026-09-01', 'info', 'a'),
  ('2026-09-01', 'warn', 'b');
```

## Пошаговое руководство
1. Смоделируйте сущности; выберите типы и charset.
2. Напишите DDL с ключами, индексами и ограничениями.
3. Мигрируйте версионированным инструментом (Flyway/Alembic).
4. Добавьте индексы под реальные паттерны.
5. Прогоните `EXPLAIN` на горячих запросах.
6. Настройте InnoDB и пул соединений.
7. Настройте репликацию и бэкапы.
8. Мониторьте медленные запросы и lock waits.

## Валидация
1. Схема применяется чисто через миграции
2. `EXPLAIN` показывает использование индексов
3. Транзакции откатываются при фейле
4. Реплика синхронизирована (для read scaling)
5. Бэкап/восстановление протестированы

## Устранение неполадок
- Медленный запрос: проверьте EXPLAIN и порядок составного индекса.
- Deadlock: короткие транзакции; консистентный порядок блокировок.
- Высокая нагрузка: buffer pool, пул соединений, read-реплики.