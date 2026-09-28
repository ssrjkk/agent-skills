---
name: pandas
description: "Analyze and transform tabular data with pandas: dataframes, cleaning, aggregation, joins, and time series. Use for any data analysis or ETL task."
category: data
tags: [pandas, python, data-analysis, dataframe, etl, csv, time-series]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-20
updated: 2026-09-28
author: ssrjkk
---
# Pandas

> Analyzing and transforming tabular data with pandas.

## Quick Start
```bash
pip install pandas
python -c "import pandas as pd; print(pd.read_csv('data.csv').head())"
```

## When to Use
- Cleaning and reshaping tabular datasets
- Aggregations, joins, and pivots
- Time series analysis and resampling
- ETL steps before machine learning

## Best Practices

### Data Loading
- Specify `dtype`, `parse_dates`, and `usecols` to avoid surprises
- Use `read_parquet`/`read_csv` with explicit schema
- Chunk large files with `chunksize` or use Dask/Polars for scale
- Validate shape and nulls right after loading

### Cleaning
- Use vectorized ops; avoid row-wise loops
- Handle missing data deliberately (`fillna` vs `dropna`)
- Normalize types: datetime, categorical, numeric
- Keep an audit trail of transformations

### Performance
- Prefer vectorized operations over `.apply`/`.iterrows`
- Use `groupby` aggregations instead of loops
- Convert object columns to categorical for speed
- Set indexes for joins; avoid merge on object columns

## Dependencies
```bash
pip install pandas numpy
# scale: polars, dask, pyarrow
```

## Examples
```python
import pandas as pd

df = pd.read_csv("sales.csv", parse_dates=["date"], dtype={"qty": "int32"})
df.info()
print(df.isna().sum())
```
```python
# Cleaning
df["price"] = df["price"].str.replace("$", "").astype(float)
df = df.dropna(subset=["order_id"])
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df[df["qty"] > 0]
```
```python
# Aggregation
by_region = (
    df.groupby("region", as_index=False)
      .agg(total=("amount", "sum"), orders=("order_id", "nunique"))
      .sort_values("total", ascending=False)
)
print(by_region.head())
```
```python
# Time series resampling
daily = df.set_index("date")["amount"].resample("D").sum()
monthly = daily.resample("ME").mean()
print(monthly.head())
```

## Step-by-Step
1. Load data with explicit dtypes and date parsing.
2. Profile: shape, columns, nulls, and unique counts.
3. Clean types and missing values deliberately.
4. Filter and transform with vectorized operations.
5. Aggregate with `groupby`; reshape with pivot/merge.
6. For time series, resample and window correctly.
7. Export with explicit schema (parquet preferred).
8. Verify outputs against the source invariants.

## Validation
1. No unexpected nulls or type errors after cleaning
2. Aggregations match manually computed totals
3. Joins don't multiply rows unexpectedly
4. Date ranges and resampling are correct
5. Results reproducible with a fixed seed (if sampling)

## Troubleshooting
- MemoryError: use dtypes, chunking, or Polars.
- Wrong joins: check key types and duplicates before merge.
- Slow loops: convert to vectorized or `groupby` operations.