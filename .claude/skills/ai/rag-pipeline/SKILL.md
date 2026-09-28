---
name: rag-pipeline
description: "Build retrieval-augmented generation pipelines: chunking, embeddings, vector search, hybrid retrieval, and citation. Use for grounded LLM answers over your data."
category: ai
tags: [rag, retrieval, embeddings, vector-db, chunking, llm, search]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-20
updated: 2026-09-28
author: ssrjkk
---
# RAG Pipeline

> Grounding LLM answers with retrieval over your own data.

## Quick Start
```bash
pip install openai chromadb sentence-transformers
# index documents, then query with retrieved context
```

## When to Use
- Answering questions over private or large document sets
- Reducing hallucinations with grounded context
- Product search and recommendation
- Chatbots that cite their sources

## Best Practices

### Chunking
- Split documents into coherent chunks (heading-aware)
- Target 200-800 tokens per chunk with overlap
- Keep chunks self-contained; include metadata (source, heading)
- Preserve structure: code, tables, and lists intact

### Embeddings
- Use models tuned for retrieval (e.g., embedding-3, bge, e5)
- Normalize embeddings for cosine similarity
- Embed chunks once; cache the index
- Consider query expansion or re-ranking for quality

### Retrieval
- Hybrid retrieval: keyword (BM25) + vector, merged by RRF
- Add metadata filters (date, source, category)
- Retrieve more, re-rank top-k with a cross-encoder
- Return top-k with scores for confidence

### Generation
- Inject retrieved chunks into the prompt with clear delimiters
- Ask for citations to chunk IDs
- Set "say I don't know" fallbacks for low scores
- Track which chunks generated the answer

## Dependencies
```bash
pip install openai chromadb sentence-transformers rank_bm25
```

## Examples
```python
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = PersistentClient(path="./db")
col = client.get_or_create_collection("docs")

def index(text: str, meta: dict, cid: str):
    col.add(ids=[cid], embeddings=[model.encode(text).tolist()], metadatas=[meta], documents=[text])

def search(query: str, k: int = 4):
    return col.query(query_embeddings=[model.encode(query).tolist()], n_results=k)
```
```python
# Hybrid retrieval: vector + BM25 merged with RRF
from rank_bm25 import BM25Okapi

def hybrid(query: str, k: int = 5):
    vec = col.query(query_embeddings=[model.encode(query).tolist()], n_results=k)
    bm25 = BM25Okapi([doc.split() for doc in all_docs])
    scores = bm25.get_scores(query.split())
    top_bm25 = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    # merge with reciprocal rank fusion...
```
```python
# Generation with citations
def answer(question: str) -> str:
    chunks = search(question)
    context = "\n\n".join(f"[{i}] {c}" for i, c in enumerate(chunks))
    prompt = f"Answer using only the context. Cite [i].\n\nContext:\n{context}\n\nQuestion: {question}"
    return run_llm(prompt)
```
```python
# Chunking helper
def chunk_doc(text: str, size: int = 600, overlap: int = 100) -> list[str]:
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size - overlap)]
```

## Step-by-Step
1. Collect and normalize source documents with metadata.
2. Chunk into coherent, self-contained units with overlap.
3. Embed chunks and store in a vector DB with filters.
4. Implement hybrid retrieval (vector + keyword) with RRF.
5. Build the prompt that injects context and demands citations.
6. Add a low-confidence fallback ("I don't know").
7. Evaluate on a Q&A set: answer accuracy + citation correctness.
8. Monitor retrieval quality and re-index on document changes.

## Validation
1. Retrieval finds relevant chunks for test questions (recall@k)
2. Generated answers are grounded in retrieved context
3. Citations map to real chunks
4. Low-confidence queries trigger the fallback
5. Latency meets the target at expected load

## Troubleshooting
- Poor recall: tune chunking, switch embedding model, add hybrid search.
- Wrong answers: check retrieval quality before blaming the LLM.
- Slow queries: use ANN indexes and cache frequent queries.