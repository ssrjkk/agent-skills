---
name: sqlite
description: "Use SQLite for embedded relational storage: schema, WAL mode, transactions, indexing, and performance. Use for local and mobile data layers."
category: database
tags: [sqlite, database, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: sqlite
author: ssrjkk
---
# SQLite (СэсКьюЭлЛайт)

> Встраиваемое реляционное хранилище на SQLite.

## Быстрый старт
```bash
sqlite3 app.db
CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT UNIQUE);
INSERT INTO users (email) VALUES ('a@b.com');
```

## Когда использовать
- Локальное/десктопное/мобильное хранилище
- Одномашинные приложения с небольшими данными
- Прототипы и встраиваемые инструменты
- Офлайн read-heavy датасеты

## Лучшие практики

### Схема
- INTEGER PRIMARY KEY или явный rowid
- TEXT для дат (ISO) или REAL для timestamp
- UNIQUE и CHECK ограничения
- `STRICT` таблицы (SQLite 3.37+) для типизации

### Конкурентность
- WAL режим для конкурентных читателей
- Короткие транзакции записи
- `busy_timeout` против SQLITE_BUSY
- Без длинных read-транзакций

### Производительность
- Индексы под WHERE/JOIN
- PRAGMA-тюнинг (cache_size, mmap)
- Батч-записи в транзакциях
- `VACUUM` периодически

### Надёжность
- Journal mode по потребности (WAL vs DELETE)
- `synchronous=NORMAL` в WAL для скорости
- Бэкап через `.backup` или VACUUM INTO
- Тестируйте на целевой ФС

## Зависимости
```bash
sqlite3  # CLI
# Python: sqlite3 stdlib
```

## Примеры
```sql
-- WAL и busy timeout
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=5000;
```
```sql
-- Схема с ограничениями
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  role TEXT NOT NULL DEFAULT 'member'
  CHECK (role IN ('member','admin'))
);
CREATE INDEX idx_users_role ON users(role);
```
```python
# Python с транзакциями
import sqlite3

conn = sqlite3.connect("app.db")
conn.execute("PRAGMA journal_mode=WAL")
with conn:
    conn.execute("INSERT INTO users (email, role) VALUES (?, ?)", ("a@b.com", "admin"))
for row in conn.execute("SELECT * FROM users"):
    print(row)
```
```python
# Батч-записи в одной транзакции
with conn:
    conn.executemany(
        "INSERT INTO logs (ts, msg) VALUES (?, ?)",
        [(1, "a"), (2, "b"), (3, "c")],
    )
```

## Пошаговое руководство
1. Выберите путь файла и откройте с pragma (WAL).
2. Создайте схему с ограничениями и индексами.
3. Пишите короткими транзакциями и `busy_timeout`.
4. Запросы с параметрами против инъекций.
5. Настройте cache и synchronous под нагрузку.
6. Бэкап через `.backup`/`VACUUM INTO`.
7. Периодически vacuum и re-analyze.
8. Тестируйте конкурентность на целевой платформе.

## Валидация
1. Записи и чтения консистентны
2. Конкурентные чтения работают в WAL
3. Нет SQLITE_BUSY при ожидаемой нагрузке
4. Запросы используют индексы (EXPLAIN QUERY PLAN)
5. Бэкап восстанавливается корректно

## Устранение неполадок
- SQLITE_BUSY: поднимите busy_timeout, укоротите транзакции.
- База заблокирована: проверьте открытые длинные транзакции.
- Медленные запросы: добавьте индексы; проверьте `EXPLAIN QUERY PLAN`.