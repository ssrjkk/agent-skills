---
name: dbt
description: "Build analytics engineering workflows with dbt: models, tests, sources, macros, and documentation. Use for transform-layer data pipelines."
category: data
tags: [dbt, data, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: dbt
author: ssrjkk
---
# dbt (ДиБиТи)

> Analytics engineering на transform-слое через dbt.

## Быстрый старт
```bash
pip install dbt-postgres
dbt init my_project
dbt run
```

## Когда использовать
- SQL-трансформационные пайплайны
- Моделирование в warehouse (staging, marts)
- Тестирование и документирование моделей
- Версионируемый analytics-код

## Лучшие практики

### Структура проекта
- Слои: staging, intermediate, marts
- Модель на grain; ясный нейминг
- `ref()` для зависимостей
- Модели небольшие и сфокусированные

### Моделирование
- Инкрементальные модели через `incremental_strategy`
- Materialized views для базовых слоёв
- Дедупликация и каст типов в staging
- Суррогатные ключи для dims

### Тесты и качество
- Singular и generic тесты
- Тесты PK, nulls и связей
- Freshness тесты на источниках
- Гейт мержей на прохождение тестов

### Документация
- Документируйте модели, колонки и источники
- `dbt docs generate` для сайта доков
- `description` на каждую модель
- Чистая lineage

## Зависимости
```bash
pip install dbt-postgres dbt-bigquery
dbt init my_project
```

## Примеры
```yaml
# dbt_project.yml
name: analytics
profile: default
model-paths: ["models"]
tests:
  +store_failures: true
```
```sql
-- models/staging/stg_orders.sql
SELECT
  id AS order_id,
  customer_id,
  amount,
  status,
  created_at
FROM {{ source('raw', 'orders') }}
WHERE status IS NOT NULL
```
```sql
-- models/marts/fct_orders.sql
SELECT
  customer_id,
  SUM(amount) AS lifetime_value,
  COUNT(*) AS order_count
FROM {{ ref('stg_orders') }}
GROUP BY 1
```
```yaml
# models/marts/schema.yml
version: 2
models:
  - name: fct_orders
    columns:
      - name: customer_id
        tests: [not_null]
```

## Пошаговое руководство
1. Инициализируйте проект и настройте профиль.
2. Определите sources для raw-таблиц.
3. Соберите staging-модели (чистка, типы).
4. Промежуточные и mart-модели через `ref()`.
5. Тесты на ключи, nulls и freshness.
6. Инкрементальные стратегии для больших таблиц.
7. Документируйте модели и колонки.
8. `dbt run && dbt test` в CI.

## Валидация
1. `dbt run` проходит
2. `dbt test` без фейлов
3. Модели строятся в порядке зависимостей
4. Инкрементальные модели обрабатывают только новые данные
5. Docs генерируются с lineage

## Устранение неполадок
- Фейлы тестов: исправьте данные или логику модели.
- Медленные прогоны: добавьте incremental и сузьте модели.
- Циклы зависимостей: рефакторите ссылки моделей.