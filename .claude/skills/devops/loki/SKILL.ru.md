---
name: loki
description: "Operate log aggregation with Grafana Loki: agents, labels, queries (LogQL), retention, and dashboards. Use for log observability."
category: devops
tags: [loki, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: loki
author: ssrjkk
---
# Grafana Loki (Локи)

> Агрегация и запросы логов через Loki.

## Быстрый старт
```bash
# одиночный бинарь или docker compose с promtail + loki
docker run -p 3100:3100 -d grafana/loki:latest -config.file=/etc/loki/local-config.yaml
```

## Когда использовать
- Централизованное хранение и запрос логов
- Корреляция с Prometheus-метриками
- Алерты на основе логов
- Логи подов Kubernetes в масштабе

## Лучшие практики

### Агенты и доставка
- Promtail или Alloy для доставки
- Структурированные labels (app, namespace, level)
- Низкая кардинальность labels
- Парсинг строк логов в поля через pipelines

### Labels и индексация
- Labels по идентификаторам, не по значениям
- High-cardinality поля — в контент лога
- Структурированный парсинг (json, logfmt) в pipelines
- Стримы по наборам labels

### Запросы (LogQL)
- Фильтры `|=`, `|~`, `|json`, `|logfmt`
- Агрегации range-функциями (`rate`, `count_over_time`)
- `{app="api"} |= "error" | json`
- Корреляция с PromQL-метриками

### Операции
- Retention и лимиты
- Мониторинг ingestion и задержки запросов
- Хранилище (filesystem/object store)
- Бэкап конфига и дашбордов

## Зависимости
```bash
docker run -p 3100:3100 -d grafana/loki:latest -config.file=/etc/loki/local-config.yaml
# агент: promtail / alloy
```

## Примеры
```yaml
# Promtail конфиг
scrape_configs:
  - job_name: app
    static_configs:
      - targets: [localhost]
        labels:
          job: app
          __path__: /var/log/app/*.log
```
```logql
# Подсчёт ошибок в минуту
sum(rate({job="app"} |= "error" [1m])) by (level)
```
```logql
# Парсинг JSON и фильтр по полю
{job="api"} | json | level="error" | message=~"timeout.*"
```
```yaml
# Loki лимиты
limits_config:
  retention_period: 720h
  max_query_lookback: 720h
  ingestion_rate_mb: 8
```

## Пошаговое руководство
1. Задеплойте Loki (single binary или HA).
2. Настройте Promtail/Alloy для доставки логов.
3. Задайте low-cardinality labels.
4. Добавьте pipelines структурированного парсинга.
5. Пишите LogQL-запросы для отладки и дашбордов.
6. Добавьте алерты на основе логов.
7. Задайте retention и лимиты.
8. Коррелируйте логи с метриками в Grafana.

## Валидация
1. Логи появляются в Loki с ожидаемой задержкой
2. LogQL возвращает корректные отфильтрованные результаты
3. Кардинальность labels низкая
4. Retention соблюдается
5. Дашборды показывают логи с метриками

## Устранение неполадок
- Нет логов: проверьте targets и пути Promtail.
- Взрыв кардинальности: перенесите high-cardinality значения в контент лога.
- Медленные запросы: сузьте наборы labels и временные диапазоны.