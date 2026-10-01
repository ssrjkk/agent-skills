---
name: embeddings
description: "Work with text embeddings: model selection, vectorization, similarity, clustering, and caching for search and retrieval. Use for semantic representation of text."
category: ai
tags: [embeddings, vectors, similarity, semantic-search, nlp, representation]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Embeddings

> Representing text as vectors for semantic similarity and retrieval.

## Quick Start
```bash
pip install sentence-transformers numpy scikit-learn
python -c "from sentence_transformers import SentenceTransformer; m=SentenceTransformer('all-MiniLM-L6-v2'); print(m.encode('hello').shape)"
```

## When to Use
- Semantic search and RAG retrieval
- Clustering and deduplication of texts
- Recommender systems by content similarity
- Anomaly detection over text corpora

## Best Practices

### Model Selection
- Match model size to data volume and latency budget
- Use retrieval-tuned models (e5, bge, embedding-3) for search
- Normalize vectors when using cosine similarity
- Freeze and version the embedding model

### Vectorization
- Encode in batches for throughput
- Cache embeddings to avoid recomputation
- Chunk long documents before encoding
- Keep a metadata map: id -> source text

### Similarity & Retrieval
- Use cosine similarity for normalized vectors
- Index with ANN (HNSW) for scale
- Combine with keyword search for hybrid retrieval
- Threshold scores for confidence

### Evaluation
- Test retrieval recall on a labeled set
- Compare candidate models on your domain
- Watch for domain drift in vocabulary
- Measure latency vs quality trade-offs

## Dependencies
```bash
pip install sentence-transformers numpy scikit-learn
# API-based: pip install openai
```

## Examples
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
docs = ["Alpha release notes", "Beta API reference", "Gamma user guide"]
emb = model.encode(docs, normalize_embeddings=True)
print(emb.shape)  # (3, 384)
```
```python
# Cosine similarity matrix
import numpy as np

def cosine(a, b):
    return float(np.dot(a, b))

query = model.encode(["how to deploy?"], normalize_embeddings=True)[0]
scores = [cosine(query, e) for e in emb]
best = int(np.argmax(scores))
print(f"best: {docs[best]} score={scores[best]:.3f}")
```
```python
# Batch encoding with caching
import json, pathlib

cache_path = pathlib.Path("embeddings.json")
cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}

def get_emb(texts: list[str]) -> list[list[float]]:
    missing = [t for t in texts if t not in cache]
    if missing:
        for t, v in zip(missing, model.encode(missing, normalize_embeddings=True)):
            cache[t] = v.tolist()
        cache_path.write_text(json.dumps(cache))
    return [cache[t] for t in texts]
```
```python
# Clustering with k-means
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3, n_init=10, random_state=0)
labels = kmeans.fit_predict(emb)
for i, label in enumerate(labels):
    print(docs[i], "-> cluster", label)
```

## Step-by-Step
1. Choose an embedding model sized to your data and latency.
2. Encode your corpus in batches; cache results.
3. Normalize vectors for cosine similarity.
4. Index with an ANN store (or numpy for small sets).
5. Build similarity queries with thresholds.
6. Add hybrid keyword retrieval where recall matters.
7. Evaluate recall@k on a labeled set.
8. Version the model and re-encode on upgrades.

## Validation
1. Similar documents score higher than dissimilar ones
2. recall@k meets the target on the eval set
3. Encoding latency is within budget
4. Caching avoids duplicate work
5. Results are reproducible with a fixed seed

## Troubleshooting
- Poor similarity: switch model or normalize vectors properly.
- Slow encoding: batch larger or downsize the model.
- Domain drift: fine-tune embeddings or add keyword boost.