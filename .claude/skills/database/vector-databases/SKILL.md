---
name: vector-databases
description: "Design and operate vector databases for semantic search and RAG: embeddings, indexes (HNSW), filtering, hybrid search, and scaling. Use for AI retrieval."
category: database
tags: [vector-db, embeddings, hnsw, similarity-search, rag, retrieval, pgvector]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-25
updated: 2026-09-28
author: ssrjkk
---
# Vector Databases

> Storing and searching embeddings for semantic retrieval and RAG.

## Quick Start
```bash
# pgvector on Postgres
docker run -e POSTGRES_PASSWORD=secret -p 5432:5432 -d pgvector/pgvector:pg17
# or Chroma:
pip install chromadb
```

## When to Use
- Semantic search over unstructured data
- RAG retrieval backends
- Recommendation by similarity
- Deduplication and clustering of texts

## Best Practices

### Embeddings
- Use retrieval-tuned embedding models
- Normalize vectors for cosine similarity
- Choose dimension balanced with storage and speed
- Embed at indexing time and query time consistently

### Indexes
- Prefer HNSW for balanced speed/recall
- Set `m` (connections) and `ef_construction` for build quality
- Use IVF for very large collections with disk budget
- Match the index to the metric (cosine/euclidean)

### Filtering & Hybrid
- Combine vector search with metadata filters
- Support hybrid retrieval (vector + keyword) when needed
- Re-rank top-k with a cross-encoder for quality
- Return scores for confidence thresholds

### Operations
- Set replication and backup for durability
- Monitor recall, latency, and index size
- Re-index when the embedding model changes
- Version the embedding model with the data

## Dependencies
```bash
# pgvector
docker run -e POSTGRES_PASSWORD=secret -p 5432:5432 -d pgvector/pgvector:pg17
# or Python-native
pip install chromadb qdrant-client
```

## Examples
```sql
-- pgvector setup and query
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
  id bigserial PRIMARY KEY,
  content text,
  embedding vector(384)
);

CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
```
```sql
-- Similarity search with filter
SELECT id, content, 1 - (embedding <=> $1) AS similarity
FROM documents
WHERE category = 'docs'
ORDER BY embedding <=> $1
LIMIT 5;
```
```python
import chromadb

client = chromadb.PersistentClient(path="./db")
col = client.get_or_create_collection("docs")

col.add(
    ids=["1", "2"],
    embeddings=[[0.1] * 384, [0.9] * 384],
    documents=["Alpha docs", "Beta docs"],
    metadatas=[{"cat": "guide"}, {"cat": "api"}],
)

res = col.query(query_embeddings=[[0.1] * 384], n_results=2, where={"cat": "guide"})
print(res["documents"])
```
```python
# Embed + store with sentence-transformers
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
vec = model.encode("query text").tolist()
col.add(ids=[id], embeddings=[vec], documents=[text])
```

## Step-by-Step
1. Choose a store: pgvector, Chroma, Qdrant, or managed services.
2. Pick an embedding model and vector dimension.
3. Index your corpus in batches with metadata.
4. Create an HNSW index tuned to your recall/latency goals.
5. Query with filters and hybrid options.
6. Re-rank results for quality where it matters.
7. Set backups, replication, and monitoring.
8. Re-index when you upgrade the embedding model.

## Validation
1. Recall@k meets the target on a labeled set
2. Query latency is within budget at scale
3. Metadata filters return correct subsets
4. Scores are meaningful and thresholdable
5. Backups restore successfully

## Troubleshooting
- Low recall: tune HNSW params or switch index type.
- Slow queries: reduce dimensions, add filters, or scale shards.
- Stale results: re-index after embedding model changes.