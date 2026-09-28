---
name: sql-querying
description: "Write correct and efficient SQL: joins, aggregations, window functions, CTEs, and query optimization. Use for any relational data access."
category: data
tags: [sql-querying, data, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: sql-querying
author: ssrjkk
---
# SQL Querying (СэлКьюЭл запросы)

> Написание корректных и эффективных SQL-запросов для анализа и приложений.

## Быстрый старт
```sql
SELECT status, COUNT(*) AS cnt
FROM orders
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY status
ORDER BY cnt DESC;
```

## Когда использовать
- Отчёты и ad-hoc анализ
- Доступ к данным приложений (под капотом ORM)
- Пайплайны данных и валидация ETL
- Любой раз, когда нужны ответы из реляционных данных

## Лучшие практики

### Читаемость
- Форматируйте запросы с ясными клаузами и алиасами
- Разбивайте сложную логику через CTE (WITH)
- Называйте колонки осмысленно через алиасы
- Комментируйте неочевидную бизнес-логику

### Корректность
- Понимайте семантику join: INNER vs LEFT vs FULL
- Следите за fan-out: join один-ко-многим умножает строки
- Используйте DISTINCT осознанно, а не по привычке
- Явно обрабатывайте NULL в WHERE/агрегациях

### Агрегация
- Агрегируйте через GROUP BY по неагрегированным колонкам
- Для рангов, running totals и дельт — оконные функции
- Фильтруйте: HAVING — по агрегатам, WHERE — по строкам
- Для уникальных подсчётов — COUNT(DISTINCT ...)

### Производительность
- Берите только нужные колонки
- Фильтруйте рано (WHERE до join)
- Убедитесь, что индексы поддерживают фильтры и join
- Избегайте функций на индексированных колонках в WHERE

## Зависимости
```bash
# psql (PostgreSQL), sqlite3 или ваш клиент БД
psql "postgres://localhost/app"
```

## Примеры
```sql
-- CTE + оконная функция: топ-продукт по категории
WITH ranked AS (
  SELECT
    category,
    product,
    revenue,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS rn
  FROM sales
)
SELECT category, product, revenue
FROM ranked
WHERE rn = 1;
```
```sql
-- Running total через оконную функцию
SELECT
  date,
  amount,
  SUM(amount) OVER (ORDER BY date) AS running_total
FROM daily_revenue;
```
```sql
-- Join с агрегацией, ранний фильтр
SELECT c.name, COUNT(o.id) AS orders
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.created_at >= '2026-01-01'
GROUP BY c.name
HAVING COUNT(o.id) > 0
ORDER BY orders DESC;
```
```sql
-- Сравнение текущего и прошлого месяца
SELECT
  product,
  SUM(CASE WHEN date_trunc('month', d) = date_trunc('month', CURRENT_DATE)
           THEN amount ELSE 0 END) AS this_month,
  SUM(CASE WHEN date_trunc('month', d) = date_trunc('month', CURRENT_DATE) - INTERVAL '1 month'
           THEN amount ELSE 0 END) AS last_month
FROM revenue
GROUP BY product;
```

## Пошаговое руководство
1. Сформулируйте вопрос на простом языке.
2. Определите таблицы и ключи join.
3. Сначала WHERE-фильтры, затем join, затем агрегация.
4. Добавьте GROUP BY / оконные функции под нужную форму.
5. Форматируйте через CTE, если запрос сложный.
6. Проверьте корректность на небольшой выборке.
7. Посмотрите план (EXPLAIN) на очевидную неэффективность.
8. Сверьте цифры с известным базлайном.

## Валидация
1. Запрос возвращает ожидаемое число строк (без fan-out сюрпризов)
2. Агрегации совпадают с независимыми итогами
3. NULL и граничные даты обработаны корректно
4. Укладывается в целевое время на продакшн-данных
5. Результаты воспроизводимы

## Устранение неполадок
- Дубликаты строк: проверяйте fan-out join; чините ключи.
- Медленный запрос: фильтруйте раньше, добавляйте индексы, упрощайте.
- Неверные итоги: проверяйте семантику join и обработку NULL.