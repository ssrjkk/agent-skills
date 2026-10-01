---
name: data-visualization
description: "Create clear data visualizations with Matplotlib, Plotly, and Altair: chart selection, design, interactivity, and dashboards. Use for communicating data."
category: data
tags: [data-viz, matplotlib, plotly, altair, charts, dashboards, visualization]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Data Visualization

> Clear, honest charts and dashboards in Python.

## Quick Start
```bash
pip install matplotlib plotly pandas
```

## When to Use
- Exploring data distributions and relationships
- Reporting metrics to stakeholders
- Building interactive dashboards
- Publishing publication-quality figures

## Best Practices

### Chart Selection
- Use bar charts for categories, lines for trends
- Use scatter for relationships, histograms for distributions
- Avoid 3D and pie charts for precision
- Match the chart to the question

### Design
- Label axes and units clearly
- Start y-axis at zero for bars
- Use a consistent color palette
- Remove chart junk and gridlines noise

### Interactivity
- Use Plotly/Altair for hover and zoom
- Link views for brushing and filtering
- Keep dashboards performant
- Provide tooltips with context

### Honesty
- Don't truncate axes misleadingly
- Show uncertainty when it matters
- Use log scales deliberately
- Cite data sources

## Dependencies
```bash
pip install matplotlib plotly pandas
# dashboards: pip install streamlit / dash
```

## Examples
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
# Distribution comparison
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Histogram(x=data_a, name="Control"))
fig.add_trace(go.Histogram(x=data_b, name="Treatment", opacity=0.6))
fig.update_layout(barmode="overlay")
```
```python
# Interactive scatter with hover
fig = px.scatter(df, x="ad_spend", y="revenue", color="channel", hover_data=["region"])
```

## Step-by-Step
1. Clarify the question the chart must answer.
2. Choose the right chart type for the data.
3. Prepare the data (aggregate, clean).
4. Build with Matplotlib (static) or Plotly/Altair (interactive).
5. Label axes, units, and titles.
6. Apply a consistent design system.
7. Add interactivity for exploration.
8. Review for honesty and clarity.

## Validation
1. Chart answers the stated question
2. Axes and units are labeled
3. No misleading truncation or scales
4. Colors are accessible and consistent
5. Interactive views load quickly

## Troubleshooting
- Cluttered charts: aggregate or filter data.
- Misleading: check axis starts and scales.
- Slow dashboards: pre-aggregate and limit data.