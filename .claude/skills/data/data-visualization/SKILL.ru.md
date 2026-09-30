---
name: data-visualization
description: "Create clear data visualizations with Matplotlib, Plotly, and Altair: chart selection, design, interactivity, and dashboards. Use for communicating data."
category: data
tags: [data-visualization, data, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: data-visualization
author: ssrjkk
---
# Data Visualization (Визуализация данных)

> Ясные, честные графики и дашборды на Python.

## Быстрый старт
```bash
pip install matplotlib plotly pandas
```

## Когда использовать
- Исследование распределений и связей
- Отчёты метрик стейкхолдерам
- Интерактивные дашборды
- Публикационные фигуры

## Лучшие практики

### Выбор графика
- Бар для категорий, линии для трендов
- Scatter для связей, histograms для распределений
- Избегайте 3D и pie для точности
- График под вопрос

### Дизайн
- Подписывайте оси и единицы
- Ось Y с нуля для баров
- Консистентная палитра
- Убирайте chart junk и шум сетки

### Интерактивность
- Plotly/Altair для hover и zoom
- Связывайте вьюхи для brushing/фильтров
- Производительные дашборды
- Tooltips с контекстом

### Честность
- Не урезайте оси вводяще
- Показывайте неопределённость
- Лог-шкалы осознанно
- Цитируйте источники данных

## Зависимости
```bash
pip install matplotlib plotly pandas
# дашборды: pip install streamlit / dash
```

## Примеры
```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({"region": ["A", "B", "C"], "sales": [10, 25, 15]})
df.plot.bar(x="region", y="sales")
plt.title("Sales by region")
plt.ylabel("Sales ($k)")
plt.tight_layout()
plt.savefig("sales.png", dpi=150)
```
```python
import plotly.express as px

fig = px.line(df, x="month", y="revenue", color="region")
fig.update_layout(title="Revenue trend", xaxis_title="Month", yaxis_title="Revenue")
fig.show()
```
```python
# Сравнение распределений
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Histogram(x=data_a, name="Control"))
fig.add_trace(go.Histogram(x=data_b, name="Treatment", opacity=0.6))
fig.update_layout(barmode="overlay")
```
```python
# Интерактивный scatter с hover
fig = px.scatter(df, x="ad_spend", y="revenue", color="channel", hover_data=["region"])
```

## Пошаговое руководство
1. Уточните вопрос, на который должен ответить график.
2. Выберите правильный тип графика.
3. Подготовьте данные (агрегация, чистка).
4. Соберите на Matplotlib (статичный) или Plotly/Altair (интерактивный).
5. Подпишите оси, единицы и заголовки.
6. Примените консистентный дизайн-систем.
7. Добавьте интерактив для исследования.
8. Проверьте честность и ясность.

## Валидация
1. График отвечает на заданный вопрос
2. Оси и единицы подписаны
3. Нет вводящего урезания или шкал
4. Цвета доступны и консистентны
5. Интерактивные вьюхи грузятся быстро

## Устранение неполадок
- Захламлённые графики: агрегируйте или фильтруйте данные.
- Вводящие: проверьте старт осей и шкалы.
- Медленные дашборды: пред-агрегируйте и ограничьте данные.