---
name: apache-spark
description: "Process large-scale data with Apache Spark: DataFrames, SQL, joins, partitioning, and optimization. Use for big data and ETL."
category: data
tags: [apache-spark, data, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: apache-spark
author: ssrjkk
---
# Apache Spark (Апач Спарк)

> Распределённая обработка данных большого масштаба на Spark.

## Быстрый старт
```bash
pip install pyspark
pyspark  # интерактивный шелл
```

## Когда использовать
- Датaсеты, слишком большие для одной машины
- Распределённый ETL и аналитика
- Стриминг (Structured Streaming)
- ML в масштабе (MLlib)

## Лучшие практики

### DataFrames и SQL
- Предпочитайте DataFrames вместо RDD
- Spark SQL для привычных декларативных запросов
- Кэшируйте переиспользуемые DataFrames
- `broadcast` для маленьких join-таблиц

### Оптимизация
- Избегайте shuffle; партиционирование и bucketing
- Фильтруйте и берите колонки рано
- `repartition`/`coalesce` осознанно
- Мониторинг стадий и shuffle в UI

### Join и агрегации
- Маленькие таблицы — `broadcast()`
- Join по bucket/partition ключам
- `groupBy` с агрегатными функциями
- Оконные функции аккуратно

### Настройка ресурсов
- `spark.executor.memory` и ядра
- `spark.sql.shuffle.partitions`
- Динамическая аллокация
- Баланс партиций против skew

## Зависимости
```bash
pip install pyspark
```

## Примеры
```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("etl").getOrCreate()

df = spark.read.parquet("s3://bucket/events")
print(df.printSchema())
```
```python
# ETL с фильтрами и агрегациями
result = (
    df.filter(F.col("status") == "paid")
      .groupBy("region")
      .agg(F.sum("amount").alias("total"), F.count("*").alias("orders"))
      .orderBy(F.desc("total"))
)
result.show()
```
```python
# Broadcast join
from pyspark.sql.functions import broadcast

users = spark.read.parquet("users.parquet").cache()
joined = df.join(broadcast(users), "user_id")
```
```sql
-- Spark SQL
SELECT region, sum(amount) AS total
FROM events
WHERE status = 'paid'
GROUP BY region
ORDER BY total DESC
```

## Пошаговое руководство
1. Запустите SparkSession с настроенным конфигом.
2. Загрузите данные (parquet/json/table).
3. Трансформируйте через DataFrames/SQL.
4. Оптимизируйте: broadcast, партиции, кэш.
5. Пишите результаты в колоночный формат.
6. Мониторьте Spark UI на skew и shuffle.
7. Настройте исполнители и партиции.
8. Планируйте задачи (Airflow/spark-submit).

## Валидация
1. Результаты совпадают с малым референсным расчётом
2. Shuffle минимизирован
3. Нет skew задач (сбалансированные партиции)
4. Кэш ускоряет переиспользуемые данные
5. Job завершается в рамках бюджета

## Устранение неполадок
- OOM: уменьшите память исполнителя или партиционируйте.
- Skew: солите ключи или репартиционируйте.
- Медленные shuffle: настройте shuffle.partitions и bucketing.