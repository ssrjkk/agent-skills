---
name: apache-spark
description: "Process large-scale data with Apache Spark: DataFrames, SQL, joins, partitioning, and optimization. Use for big data and ETL."
category: data
tags: [apache-spark, spark, big-data, dataframe, etl, pyspark, distributed]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Apache Spark

> Large-scale distributed data processing with Spark.

## Quick Start
```bash
pip install pyspark
pyspark  # interactive shell
```

## When to Use
- Processing datasets too big for a single machine
- Distributed ETL and analytics
- Streaming (Structured Streaming)
- Machine learning at scale (MLlib)

## Best Practices

### DataFrames & SQL
- Prefer DataFrames over RDDs for most work
- Use Spark SQL for familiar declarative queries
- Cache intermediate DataFrames when reused
- Use `broadcast` for small join tables

### Optimization
- Avoid shuffles; use partitioning and bucketing
- Filter and select early to reduce data
- Use `repartition`/`coalesce` deliberately
- Monitor stages and shuffle in the UI

### Joins & Aggregations
- Broadcast small tables with `broadcast()`
- Join on bucketed/partitioned keys
- Use `groupBy` with aggregation functions
- Prefer window functions carefully

### Resource Tuning
- Set `spark.executor.memory` and cores
- Tune `spark.sql.shuffle.partitions`
- Use dynamic allocation
- Balance partitions to avoid skew

## Dependencies
```bash
pip install pyspark
```

## Examples
```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("etl").getOrCreate()

df = spark.read.parquet("s3://bucket/events")
print(df.printSchema())
```
```python
# ETL with filters and aggregations
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

## Step-by-Step
1. Start a SparkSession with tuned config.
2. Load data (parquet/json/table).
3. Transform with DataFrames/SQL.
4. Optimize: broadcast, partitioning, caching.
5. Write results in a columnar format.
6. Monitor the Spark UI for skew and shuffles.
7. Tune executors and partitions.
8. Schedule jobs (Airflow/spark-submit).

## Validation
1. Results match a small reference computation
2. Shuffles are minimized
3. No task skew (balanced partitions)
4. Caching speeds up reused data
5. Job completes within the budget

## Troubleshooting
- OOM: reduce executor memory or partition data.
- Skew: salt keys or repartition.
- Slow shuffles: tune shuffle.partitions and bucketing.