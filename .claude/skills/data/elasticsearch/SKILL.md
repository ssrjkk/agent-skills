---
name: elasticsearch
description: "Design and operate Elasticsearch: mappings, indexing, queries, aggregations, and cluster tuning. Use for search and log analytics."
category: data
tags: [elasticsearch, search, full-text, indexing, aggregations, kibana, logs]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-26
updated: 2026-09-28
author: ssrjkk
---
# Elasticsearch

> Building and operating search and analytics with Elasticsearch.

## Quick Start
```bash
docker run -p 9200:9200 -e "discovery.type=single-node" -d docker.elastic.co/elasticsearch/elasticsearch:8.17.0
curl -s localhost:9200  # cluster info
```

## When to Use
- Full-text and fuzzy search over documents
- Log and metric analytics (with Kibana)
- Autocomplete and faceted filtering
- Large-scale read-heavy datasets

## Best Practices

### Mappings
- Define mappings before indexing bulk data
- Choose field types explicitly (keyword vs text)
- Use `text` for search, `keyword` for filter/sort
- Enable dynamic mapping carefully or disable it

### Indexing
- Index in bulk batches for throughput
- Use an alias for zero-downtime reindex
- Manage shard count by size and load
- Set refresh interval and replica counts

### Queries
- Use `match` for search, `term` for exact values
- Combine with `bool` (must, should, filter)
- Use aggregations for analytics
- Paginate with search_after, not deep from

### Operations
- Secure with TLS and auth (xpack)
- Monitor cluster health and shard allocation
- Set disk watermark alerts
- Back up indices and plan disaster recovery

## Dependencies
```bash
docker run -p 9200:9200 -e "discovery.type=single-node" -d docker.elastic.co/elasticsearch/elasticsearch:8.17.0
# Python client
pip install elasticsearch
```

## Examples
```python
from elasticsearch import Elasticsearch

es = Elasticsearch("https://localhost:9200", basic_auth=("elastic", "password"), verify_certs=False)
print(es.info())
```
```json
// Mapping: text for search, keyword for filter
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
# Search with bool query and aggregation
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
# Bulk indexing
from elasticsearch.helpers import bulk

docs = [{"_index": "products", "_id": str(i), "_source": {"title": f"item {i}", "category": "x"}} for i in range(1000)]
success, _ = bulk(es, docs)
```

## Step-by-Step
1. Plan the index structure and field types.
2. Create mappings and an alias.
3. Index data in bulk with error handling.
4. Write search queries with bool and filters.
5. Add aggregations for analytics dashboards.
6. Tune shards, replicas, and refresh.
7. Secure and monitor the cluster.
8. Set up backups and reindex workflows.

## Validation
1. Queries return relevant, correctly ranked results
2. Aggregations match source data
3. Bulk indexing completes without errors
4. Cluster health is green
5. Search latency within budget at load

## Troubleshooting
- Mapping conflicts: fix the type mismatch before reindex.
- Slow queries: add filters, tune shards, or use search templates.
- Disk pressure: monitor watermarks; scale or archive old indices.