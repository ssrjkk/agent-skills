---
name: pandas
description: "Analyze and transform tabular data with pandas: dataframes, cleaning, aggregation, joins, and time series. Use for any data analysis or ETL task."
category: data
tags: [pandas, data, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: pandas
author: ssrjkk
---
# Pandas (Пандас)

> Анализ и трансформация табличных данных через pandas.

## Быстрый старт
```bash
pip install pandas
python -c "import pandas as pd; print(pd.read_csv('data.csv').head())"
```

## Когда использовать
- Очистка и изменение формы табличных датасетов
- Агрегации, joins и pivot
- Анализ временных рядов и ресемплинг
- ETL-шаги перед машинным обучением

## Лучшие практики

### Загрузка данных
- Указывайте `dtype`, `parse_dates` и `usecols`, чтобы избежать сюрпризов
- Используйте `read_parquet`/`read_csv` с явной схемой
- Большие файлы читайте по частям (`chunksize`) или используйте Dask/Polars
- Сразу после загрузки проверяйте форму и nulls

### Очистка
- Используйте векторизованные операции; избегайте циклов по строкам
- Работайте с пропусками осознанно (`fillna` против `dropna`)
- Нормализуйте типы: datetime, categorical, numeric
- Держите трейс трансформаций

### Производительность
- Предпочитайте векторизацию вместо `.apply`/`.iterrows`
- Агрегируйте через `groupby`, а не циклы
- Конвертируйте object-колонки в categorical для скорости
- Ставьте индексы для joins; избегайте merge по object-колонкам

## Зависимости
```bash
pip install pandas numpy
# масштаб: polars, dask, pyarrow
```

## Примеры
```python
import pandas as pd

df = pd.read_csv("sales.csv", parse_dates=["date"], dtype={"qty": "int32"})
df.info()
print(df.isna().sum())
```
```python
# Очистка
df["price"] = df["price"].str.replace("$", "").astype(float)
df = df.dropna(subset=["order_id"])
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df[df["qty"] > 0]
```
```python
# Агрегация
by_region = (
    df.groupby("region", as_index=False)
      .agg(total=("amount", "sum"), orders=("order_id", "nunique"))
      .sort_values("total", ascending=False)
)
print(by_region.head())
```
```python
# Ресемплинг временных рядов
daily = df.set_index("date")["amount"].resample("D").sum()
monthly = daily.resample("ME").mean()
print(monthly.head())
```

## Пошаговое руководство
1. Загрузите данные с явными dtypes и парсингом дат.
2. Профилируйте: форма, колонки, nulls, уникальные значения.
3. Очистите типы и пропуски осознанно.
4. Фильтруйте и трансформируйте векторизованно.
5. Агрегируйте через `groupby`; изменяйте форму через pivot/merge.
6. Для временных рядов корректно ресемплируйте и сдвигайте окна.
7. Экспортируйте с явной схемой (лучше parquet).
8. Сверяйте выводы с инвариантами источника.

## Валидация
1. Нет неожиданных nulls или ошибок типов после очистки
2. Агрегации совпадают с ручным подсчётом
3. Joins не умножают строки неожиданно
4. Диапазоны дат и ресемплинг корректны
5. Результаты воспроизводимы с фиксированным seed (при сэмплинге)

## Устранение неполадок
- MemoryError: используйте dtypes, чанки или Polars.
- Неверные joins: проверяйте типы ключей и дубликаты до merge.
- Медленные циклы: переводите в векторизованные или `groupby` операции.