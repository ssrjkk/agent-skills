---
name: elasticsearch
description: "Design and operate Elasticsearch: mappings, indexing, queries, aggregations, and cluster tuning. Use for search and log analytics."
category: data
tags: [elasticsearch, data, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: elasticsearch
author: ssrjkk
---
# Elasticsearch (ЭластикСёрч)

> Построение и эксплуатация поиска и аналитики на Elasticsearch.

## Быстрый старт
```bash
docker run -p 9200:9200 -e "discovery.type=single-node" -d docker.elastic.co/elasticsearch/elasticsearch:8.17.0
curl -s localhost:9200  # инфо о кластере
```

## Когда использовать
- Полнотекстовый и fuzzy поиск по документам
- Аналитика логов и метрик (с Kibana)
- Автокомплит и фасетные фильтры
- Большие read-heavy датасеты

## Лучшие практики

### Маппинги
- Определяйте маппинги до массовой индексации
- Типы полей явно (keyword vs text)
- `text` — для поиска, `keyword` — для фильтра/сортировки
- Dynamic mapping аккуратно или отключайте

### Индексация
- Батчами для пропускной способности
- Алиас — для reindex без downtime
- Число шардов — под размер и нагрузку
- Настройте refresh interval и реплики

### Запросы
- `match` — для поиска, `term` — для точных значений
- Комбинируйте через `bool` (must, should, filter)
- Для аналитики — aggregations
- Пагинация через search_after, а не глубокий from

### Операции
- Безопасность: TLS и auth (xpack)
- Мониторинг health кластера и аллокации шардов
- Алерты на disk watermark
- Бэкапы индексов и план DR

## Зависимости
```bash
docker run -p 9200:9200 -e "discovery.type=single-node" -d docker.elastic.co/elasticsearch/elasticsearch:8.17.0
# Python клиент
pip install elasticsearch
```

## Примеры
```python
from elasticsearch import Elasticsearch

es = Elasticsearch("https://localhost:9200", basic_auth=("elastic", "password"), verify_certs=False)
print(es.info())
```
```json
// Маппинг: text для поиска, keyword для фильтра
PUT /products
{
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "category": { "type": "keyword" },
      "price": { "type": "float" }
    }
  }
}
```
```python
# Поиск с bool query и агрегацией
resp = es.search(index="products", body={
    "query": {
        "bool": {
            "must": [{"match": {"title": "laptop"}}],
            "filter": [{"term": {"category": "electronics"}}],
        }
    },
    "aggs": {"by_category": {"terms": {"field": "category"}}},
})
```
```python
# Bulk индексация
from elasticsearch.helpers import bulk

docs = [{"_index": "products", "_id": str(i), "_source": {"title": f"item {i}", "category": "x"}} for i in range(1000)]
success, _ = bulk(es, docs)
```

## Пошаговое руководство
1. Спланируйте структуру индекса и типы полей.
2. Создайте маппинги и алиас.
3. Индексируйте данные батчами с обработкой ошибок.
4. Напишите поисковые запросы с bool и фильтрами.
5. Добавьте агрегации для аналитических дашбордов.
6. Настройте шарды, реплики и refresh.
7. Обеспечьте безопасность и мониторинг кластера.
8. Настройте бэкапы и reindex-воркфлоу.

## Валидация
1. Запросы возвращают релевантные, корректно ранжированные результаты
2. Агрегации совпадают с исходными данными
3. Bulk-индексация завершается без ошибок
4. Health кластера зелёный
5. Задержка поиска в рамках бюджета под нагрузкой

## Устранение неполадок
- Конфликты маппингов: исправьте несоответствие типов до reindex.
- Медленные запросы: добавьте фильтры, настройте шарды или используйте шаблоны поиска.
- Диск: мониторьте watermarks; масштабируйте или архивируйте старые индексы.