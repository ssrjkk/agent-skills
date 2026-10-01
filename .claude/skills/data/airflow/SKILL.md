---
name: airflow
description: "Orchestrate data pipelines with Apache Airflow: DAGs, tasks, dependencies, sensors, and retries. Use for scheduled workflows."
category: data
tags: [airflow, orchestration, dag, pipelines, scheduling, etl, workflows]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Apache Airflow

> Scheduling and orchestrating data workflows.

## Quick Start
```bash
pip install apache-airflow
airflow standalone  # dev instance
```

## When to Use
- Scheduled ETL/ELT pipelines
- Multi-step workflows with dependencies
- Retries, backfills, and alerting
- Data platform orchestration

## Best Practices

### DAG Design
- Keep DAGs idempotent and deterministic
- Use TaskFlow API for Python tasks
- Make dependencies explicit with `>>`
- Set `catchup` and `max_active_runs` deliberately

### Tasks & Operators
- Use the right operator (Python, SQL, Kubernetes)
- Keep tasks small and single-purpose
- Set retries and retry_delays per task
- Use sensors for external dependencies

### Scheduling & Backfills
- Set the schedule with cron/interval
- Handle backfills with catchup
- Avoid dependencies on wall-clock time
- Use data-interval aware logic

### Reliability
- Store state in a real backend (Postgres)
- Use Airflow connections/secrets for credentials
- Monitor DAG runs and task duration
- Alert on failures

## Dependencies
```bash
pip install apache-airflow
airflow standalone
```

## Examples
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
# Explicit dependencies with the TaskFlow API
with DAG("multi", ...) as dag:
    t1 = BashOperator(task_id="a", bash_command="echo a")
    t2 = BashOperator(task_id="b", bash_command="echo b")
    t3 = BashOperator(task_id="c", bash_command="echo c")
    t1 >> [t2, t3]
```
```python
# Task with retries
@task(retries=3, retry_delay=timedelta(minutes=5))
def flaky():
    do_work()
```
```python
# Sensor for an external file
from airflow.sensors.filesystem import FileSensor

wait = FileSensor(task_id="wait", filepath="/data/ready", poke_interval=30)
```

## Step-by-Step
1. Install Airflow and set up a backend DB.
2. Define DAGs in the dags folder.
3. Build tasks with the TaskFlow API.
4. Set explicit dependencies and schedules.
5. Add retries, sensors, and alerts.
6. Use connections for credentials.
7. Backfill historical runs with catchup.
8. Monitor runs and tune concurrency.

## Validation
1. DAGs parse without errors
2. Runs complete successfully on schedule
3. Retries recover transient failures
4. Backfills produce consistent results
5. No duplicate/overlapping runs

## Troubleshooting
- Task stuck: check for missing sensors or resources.
- Timing issues: use data-interval aware logic.
- Concurrency saturation: tune max_active_tasks.