---
name: airflow
description: "Orchestrate data pipelines with Apache Airflow: DAGs, tasks, dependencies, sensors, and retries. Use for scheduled workflows."
category: data
tags: [airflow, data, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: airflow
author: ssrjkk
---
# Apache Airflow (Эйрфлоу)

> Планирование и оркестрация рабочих процессов данных.

## Быстрый старт
```bash
pip install apache-airflow
airflow standalone  # dev instance
```

## Когда использовать
- Планируемые ETL/ELT пайплайны
- Многошаговые workflow с зависимостями
- Retries, backfills и алерты
- Оркестрация платформы данных

## Лучшие практики

### Дизайн DAG
- DAGs идемпотентны и детерминированы
- TaskFlow API для Python-задач
- Явные зависимости через `>>`
- `catchup` и `max_active_runs` осознанно

### Задачи и операторы
- Правильный оператор (Python, SQL, Kubernetes)
- Задачи мелкие и одноцелевые
- retries и retry_delays на задачу
- Sensors для внешних зависимостей

### Планирование и backfill
- Расписание через cron/interval
- Backfill через catchup
- Без зависимости от wall-clock
- Логика с учётом data interval

### Надёжность
- Состояние в реальном backend (Postgres)
- Airflow connections/secrets для кредов
- Мониторинг DAG-ранов и длительности задач
- Алерты на фейлы

## Зависимости
```bash
pip install apache-airflow
airflow standalone
```

## Примеры
```python
from airflow import DAG
from airflow.decorators import task
from datetime import datetime

with DAG("etl", start_date=datetime(2026, 1, 1), schedule="@daily",
         catchup=False) as dag:

    @task
    def extract():
        return {"rows": 100}

    @task
    def transform(data: dict):
        return {**data, "processed": True}

    @task
    def load(data: dict):
        print("loaded", data)

    load(transform(extract()))
```
```python
# Явные зависимости через TaskFlow API
with DAG("multi", ...) as dag:
    t1 = BashOperator(task_id="a", bash_command="echo a")
    t2 = BashOperator(task_id="b", bash_command="echo b")
    t3 = BashOperator(task_id="c", bash_command="echo c")
    t1 >> [t2, t3]
```
```python
# Задача с retries
@task(retries=3, retry_delay=timedelta(minutes=5))
def flaky():
    do_work()
```
```python
# Sensor на внешний файл
from airflow.sensors.filesystem import FileSensor

wait = FileSensor(task_id="wait", filepath="/data/ready", poke_interval=30)
```

## Пошаговое руководство
1. Установите Airflow и настройте backend БД.
2. Определите DAGs в папке dags.
3. Соберите задачи через TaskFlow API.
4. Явные зависимости и расписания.
5. Retries, sensors и алерты.
6. Connections для кредов.
7. Backfill исторических прогонов через catchup.
8. Мониторинг прогонов и настройка конкурентности.

## Валидация
1. DAGs парсятся без ошибок
2. Прогоны завершаются по расписанию
3. Retries восстанавливают транзиентные фейлы
4. Backfills дают консистентные результаты
5. Нет дублей/перекрывающихся прогонов

## Устранение неполадок
- Задача зависла: проверьте sensors или ресурсы.
- Проблемы тайминга: логика с учётом data interval.
- Насыщение конкурентности: настройте max_active_tasks.