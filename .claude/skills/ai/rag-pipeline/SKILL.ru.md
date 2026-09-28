---
name: rag-pipeline
description: "Build retrieval-augmented generation pipelines: chunking, embeddings, vector search, hybrid retrieval, and citation. Use for grounded LLM answers over your data."
category: ai
tags: [rag-pipeline, ai, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: rag-pipeline
author: ssrjkk
---
# RAG Pipeline (РЭГ-пайплайн)

> Grounding ответов LLM через поиск по вашим данным.

## Быстрый старт
```bash
pip install openai chromadb sentence-transformers
# индексируйте документы, затем задавайте вопросы с извлечённым контекстом
```

## Когда использовать
- Ответы на вопросы по частным или большим наборам документов
- Снижение галлюцинаций через grounded контекст
- Поиск по продуктам и рекомендации
- Чат-боты, которые цитируют источники

## Лучшие практики

### Чанкинг
- Делите документы на связные чанки (по заголовкам)
- Цель: 200-800 токенов на чанк с перекрытием
- Держите чанки самодостаточными; включайте метаданные (источник, заголовок)
- Сохраняйте структуру: код, таблицы и списки целиком

### Эмбеддинги
- Используйте модели для retrieval (embedding-3, bge, e5)
- Нормализуйте эмбеддинги для cosine similarity
- Эмбеддьте чанки один раз; кэшируйте индекс
- Для качества — query expansion или реранкинг

### Поиск
- Гибрид: keyword (BM25) + vector, слияние через RRF
- Добавляйте фильтры по метаданным (дата, источник, категория)
- Берите больше, реранките top-k cross-encoder'ом
- Возвращайте top-k со скором для уверенности

### Генерация
- Инжектируйте чанки в промпт с явными разделителями
- Просите цитаты к ID чанков
- Задайте фолбэк "не знаю" при низких скорах
- Отслеживайте, какие чанки породили ответ

## Зависимости
```bash
pip install openai chromadb sentence-transformers rank_bm25
```

## Примеры
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
# Гибрид: vector + BM25, слияние через RRF
from rank_bm25 import BM25Okapi

def hybrid(query: str, k: int = 5):
    vec = col.query(query_embeddings=[model.encode(query).tolist()], n_results=k)
    bm25 = BM25Okapi([doc.split() for doc in all_docs])
    scores = bm25.get_scores(query.split())
    top_bm25 = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    # merge через reciprocal rank fusion...
```
```python
# Генерация с цитатами
def answer(question: str) -> str:
    chunks = search(question)
    context = "\n\n".join(f"[{i}] {c}" for i, c in enumerate(chunks))
    prompt = f"Answer using only the context. Cite [i].\n\nContext:\n{context}\n\nQuestion: {question}"
    return run_llm(prompt)
```
```python
# Хелпер чанкинга
def chunk_doc(text: str, size: int = 600, overlap: int = 100) -> list[str]:
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size - overlap)]
```

## Пошаговое руководство
1. Соберите и нормализуйте исходные документы с метаданными.
2. Нарежьте на связные самодостаточные чанки с перекрытием.
3. Эмбеддьте чанки и храните в vector DB с фильтрами.
4. Реализуйте гибридный поиск (vector + keyword) через RRF.
5. Соберите промпт с контекстом и требованием цитат.
6. Добавьте фолбэк при низкой уверенности ("не знаю").
7. Оцените на Q&A-наборе: точность ответов + корректность цитат.
8. Мониторьте качество поиска и переиндексируйте при изменениях.

## Валидация
1. Поиск находит релевантные чанки для тестовых вопросов (recall@k)
2. Ответы grounded в извлечённом контексте
3. Цитаты указывают на реальные чанки
4. Низкоуверенные запросы уходят в фолбэк
5. Задержка в рамках цели при ожидаемой нагрузке

## Устранение неполадок
- Низкий recall: настройте чанкинг, смените модель эмбеддингов, добавьте гибрид.
- Неверные ответы: сначала проверяйте качество поиска, а не вините LLM.
- Медленные запросы: используйте ANN-индексы и кэшируйте частые запросы.