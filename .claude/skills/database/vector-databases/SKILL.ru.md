---
name: vector-databases
description: "Design and operate vector databases for semantic search and RAG: embeddings, indexes (HNSW), filtering, hybrid search, and scaling. Use for AI retrieval."
category: database
tags: [vector-databases, database, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: vector-databases
author: ssrjkk
---
# Vector Databases (Векторные БД)

> Хранение и поиск эмбеддингов для семантического поиска и RAG.

## Быстрый старт
```bash
# pgvector на Postgres
docker run -e POSTGRES_PASSWORD=secret -p 5432:5432 -d pgvector/pgvector:pg17
# или Chroma:
pip install chromadb
```

## Когда использовать
- Семантический поиск по неструктурированным данным
- Retrieval-бэкенд для RAG
- Рекомендации по похожести
- Дедупликация и кластеризация текстов

## Лучшие практики

### Эмбеддинги
- Используйте retrieval-ориентированные модели
- Нормализуйте векторы для cosine similarity
- Размерность — баланс между хранением и скоростью
- Индексируйте и запрашивайте согласованно

### Индексы
- Предпочитайте HNSW для баланса скорость/recall
- `m` (connections) и `ef_construction` — для качества построения
- Для очень больших коллекций с дисковым бюджетом — IVF
- Согласуйте индекс с метрикой (cosine/euclidean)

### Фильтрация и гибрид
- Комбинируйте векторный поиск с метаданными-фильтрами
- Гибрид (vector + keyword), когда нужно
- Для качества — реранкинг top-k через cross-encoder
- Возвращайте скоре для порогов уверенности

### Операции
- Репликация и бэкапы для надёжности
- Мониторьте recall, задержку и размер индекса
- Переиндексируйте при смене модели эмбеддингов
- Версионируйте модель эмбеддингов вместе с данными

## Зависимости
```bash
# pgvector
docker run -e POSTGRES_PASSWORD=secret -p 5432:5432 -d pgvector/pgvector:pg17
# или Python-native
pip install chromadb qdrant-client
```

## Примеры
```sql
-- pgvector setup и запрос
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
  id bigserial PRIMARY KEY,
  content text,
  embedding vector(384)
);

CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
```
```sql
-- Поиск по похожести с фильтром
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
# Эмбеддинг + хранение через sentence-transformers
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
vec = model.encode("query text").tolist()
col.add(ids=[id], embeddings=[vec], documents=[text])
```

## Пошаговое руководство
1. Выберите хранилище: pgvector, Chroma, Qdrant или managed.
2. Выберите модель эмбеддингов и размерность вектора.
3. Индексируйте корпус батчами с метаданными.
4. Создайте HNSW-индекс под ваши цели recall/задержки.
5. Запрашивайте с фильтрами и гибридными опциями.
6. Реранките результаты там, где важно качество.
7. Настройте бэкапы, репликацию и мониторинг.
8. Переиндексируйте при апгрейде модели эмбеддингов.

## Валидация
1. recall@k соответствует цели на размеченном наборе
2. Задержка запросов в рамках бюджета в масштабе
3. Фильтры по метаданным возвращают корректные подмножества
4. Скоре осмысленны и допускают пороги
5. Бэкапы восстанавливаются успешно

## Устранение неполадок
- Низкий recall: настройте параметры HNSW или смените тип индекса.
- Медленные запросы: уменьшите размерность, добавьте фильтры или шардируйте.
- Устаревшие результаты: переиндексируйте после смены модели эмбеддингов.