---
name: mlops
description: "Operate machine learning in production: experiment tracking, pipelines, model registry, serving, monitoring, and CI/CD for ML. Use for ML lifecycle."
category: ai
tags: [mlops, ai, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: mlops
author: ssrjkk
---
# MLOps (ЭмЭлОпс)

> Надёжный продакшн машинного обучения.

## Быстрый старт
```bash
pip install mlflow
mlflow ui  # UI трекинга экспериментов
```

## Когда использовать
- Модели, которым нужен воспроизводимый тренинг
- Команды, регулярно выкатывающие модели в прод
- Data drift и мониторинг моделей
- Коллаборация data science и инженерии

## Лучшие практики

### Эксперименты
- Трекайте каждый запуск: params, metrics, artifacts
- Трекинг через MLflow или W&B
- Версионируйте датасеты и код вместе с запуском
- Сравнивайте запуски систематически

### Пайплайны
- Воспроизводимые data → train → evaluate пайплайны
- Оркестраторы (Airflow, Prefect, TFX)
- Кэшируйте промежуточные артефакты
- Разделяйте кодовые пути train и serve

### Model Registry
- Регистрируйте модели-кандидаты с метаданными
- Стейджи: staging → production
- Храните точный артефакт + сигнатуру
- Версионируйте и откатывайте модели

### Сервинг и мониторинг
- Сервинг через REST/gRPC или serverless inference
- Мониторинг дрейфа ввода/вывода
- Трекинг задержки, throughput и error rates
- Алерты и триггеры отката

## Зависимости
```bash
pip install mlflow scikit-learn
# оркестраторы: airflow / prefect
# сервинг: bentoml / triton / fastapi
```

## Примеры
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
# Загрузка зарегистрированной модели для сервинга
import mlflow.sklearn

model = mlflow.sklearn.load_model("models:/churn/Production")

def predict(features: dict) -> dict:
    pred = model.predict([list(features.values())])[0]
    proba = model.predict_proba([list(features.values())])[0].tolist()
    return {"prediction": int(pred), "probabilities": proba}
```
```yaml
# CI/CD для ML (псевдо)
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
# Мониторинг дрейфа
import numpy as np

def drift_score(train_mean: float, live_mean: float, train_std: float) -> float:
    return abs(live_mean - train_mean) / max(train_std, 1e-9)

def alert_if_drift(score: float, threshold: float = 2.0) -> str:
    return "ALERT" if score > threshold else "ok"
```

## Пошаговое руководство
1. Настройте трекинг экспериментов для всех запусков.
2. Версионируйте код, данные и модель вместе.
3. Соберите воспроизводимые тренировочные пайплайны.
4. Оценивайте на фиксированном holdout с порогами.
5. Регистрируйте модели с метаданными и продвижением по стейджам.
6. Сервите с единым интерфейсом и сигнатурой.
7. Мониторьте дрейф, задержку и ошибки.
8. Определите триггеры отката и переобучения.

## Валидация
1. Каждый запуск воспроизводим (seed, данные, версии кода)
2. Метрики трекаются и сравнимы
3. Зарегистрированные модели имеют ясный жизненный цикл стейджей
4. Сервинг совпадает с препроцессингом тренинга
5. Дрейф-алерты срабатывают до деградации качества

## Устранение неполадок
- Train/serve skew: делите код препроцессинга между обоими.
- Дрейф модели: мониторьте входы; переобучайте по расписанию или алертам.
- Медленный сервинг: батчите запросы и масштабируйте эндпоинт.