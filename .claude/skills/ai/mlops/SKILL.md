---
name: mlops
description: "Operate machine learning in production: experiment tracking, pipelines, model registry, serving, monitoring, and CI/CD for ML. Use for ML lifecycle."
category: ai
tags: [mlops, machine-learning, pipelines, model-registry, serving, monitoring, ml]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-26
updated: 2026-09-28
author: ssrjkk
---
# MLOps

> Running machine learning reliably in production.

## Quick Start
```bash
pip install mlflow
mlflow ui  # experiment tracking UI
```

## When to Use
- Models that need reproducible training
- Teams shipping models to production repeatedly
- Data drift and model monitoring
- Collaboration between data science and engineering

## Best Practices

### Experiments
- Track every run: params, metrics, artifacts
- Use MLflow or W&B for tracking
- Version datasets and code with the run
- Compare runs systematically

### Pipelines
- Build reproducible data → train → evaluate pipelines
- Use orchestrators (Airflow, Prefect, TFX)
- Cache intermediate artifacts
- Separate train vs serve code paths

### Model Registry
- Register candidate models with metadata
- Stage models: staging → production
- Store the exact artifact + signature
- Version and rollback models

### Serving & Monitoring
- Serve via REST/gRPC or serverless inference
- Monitor input/output data drift
- Track latency, throughput, and error rates
- Set alerts and define rollback triggers

## Dependencies
```bash
pip install mlflow scikit-learn
# orchestrators: airflow / prefect
# serving: bentoml / triton / fastapi
```

## Examples
```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

mlflow.set_experiment("churn")

with mlflow.start_run():
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)

    model = RandomForestClassifier(n_estimators=100, max_depth=5)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))

    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "model")
```
```python
# Load a registered model for serving
import mlflow.sklearn

model = mlflow.sklearn.load_model("models:/churn/Production")

def predict(features: dict) -> dict:
    pred = model.predict([list(features.values())])[0]
    proba = model.predict_proba([list(features.values())])[0].tolist()
    return {"prediction": int(pred), "probabilities": proba}
```
```yaml
# CI/CD for ML (pseudo)
stages:
  - train:
      script: python train.py
      artifacts: [model.pkl, metrics.json]
  - register:
      when: metrics.accuracy >= 0.85
      command: mlflow register -m run/model
  - deploy:
      when: stage == register
      command: deploy_to_prod model
```
```python
# Drift monitoring
import numpy as np

def drift_score(train_mean: float, live_mean: float, train_std: float) -> float:
    return abs(live_mean - train_mean) / max(train_std, 1e-9)

def alert_if_drift(score: float, threshold: float = 2.0) -> str:
    return "ALERT" if score > threshold else "ok"
```

## Step-by-Step
1. Set up experiment tracking for all training runs.
2. Version code, data, and model together.
3. Build reproducible training pipelines.
4. Evaluate with a fixed holdout and thresholds.
5. Register models with metadata and stage promotion.
6. Serve with a consistent interface and signature.
7. Monitor drift, latency, and errors.
8. Define rollback and retraining triggers.

## Validation
1. Every run is reproducible (seed, data, code versions)
2. Metrics are tracked and comparable
3. Registered models have a clear stage lifecycle
4. Serving matches training preprocessing
5. Drift alerts fire before quality degrades

## Troubleshooting
- Train/serve skew: share preprocessing code between both.
- Model drift: monitor inputs; retrain on schedule or alerts.
- Slow serving: batch requests and scale the endpoint.