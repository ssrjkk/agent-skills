---
name: embeddings
description: "Work with text embeddings: model selection, vectorization, similarity, clustering, and caching for search and retrieval. Use for semantic representation of text."
category: ai
tags: [embeddings, ai, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: embeddings
author: ssrjkk
---
# Embeddings (Эмбеддинги)

> Представление текста векторами для семантической похожести и поиска.

## Быстрый старт
```bash
pip install sentence-transformers numpy scikit-learn
python -c "from sentence_transformers import SentenceTransformer; m=SentenceTransformer('all-MiniLM-L6-v2'); print(m.encode('hello').shape)"
```

## Когда использовать
- Семантический поиск и retrieval для RAG
- Кластеризация и дедупликация текстов
- Рекомендации по похожести контента
- Аномалии в текстовых корпусах

## Лучшие практики

### Выбор модели
- Размер модели — под объём данных и бюджет задержки
- Для поиска — retrieval-ориентированные (e5, bge, embedding-3)
- Нормализуйте векторы для cosine similarity
- Фиксируйте и версионируйте модель

### Векторизация
- Кодируйте батчами для пропускной способности
- Кэшируйте эмбеддинги, чтобы не считать повторно
- Длинные документы чанкуйте до кодирования
- Храните map метаданных: id -> исходный текст

### Похожесть и поиск
- Cosine similarity для нормализованных векторов
- Для масштаба — ANN-индекс (HNSW)
- Комбинируйте с keyword-поиском для гибрида
- Пороговые скоре для уверенности

### Оценка
- Тестируйте recall на размеченном наборе
- Сравнивайте модели-кандидаты на вашем домене
- Следите за дрейфом словаря домена
- Меряйте trade-off задержка/качество

## Зависимости
```bash
pip install sentence-transformers numpy scikit-learn
# API-базируемые: pip install openai
```

## Примеры
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
docs = ["Alpha release notes", "Beta API reference", "Gamma user guide"]
emb = model.encode(docs, normalize_embeddings=True)
print(emb.shape)  # (3, 384)
```
```python
# Матрица cosine similarity
import numpy as np

def cosine(a, b):
    return float(np.dot(a, b))

query = model.encode(["how to deploy?"], normalize_embeddings=True)[0]
scores = [cosine(query, e) for e in emb]
best = int(np.argmax(scores))
print(f"best: {docs[best]} score={scores[best]:.3f}")
```
```python
# Батч-кодирование с кэшем
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
# Кластеризация через k-means
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3, n_init=10, random_state=0)
labels = kmeans.fit_predict(emb)
for i, label in enumerate(labels):
    print(docs[i], "-> cluster", label)
```

## Пошаговое руководство
1. Выберите модель эмбеддингов под объём и задержку.
2. Закодируйте корпус батчами; кэшируйте результаты.
3. Нормализуйте векторы для cosine similarity.
4. Индексируйте через ANN-хранилище (или numpy для малых наборов).
5. Стройте запросы похожести с порогами.
6. Где важен recall — добавьте гибридный keyword-поиск.
7. Оцените recall@k на размеченном наборе.
8. Версионируйте модель и перекодируйте при апгрейдах.

## Валидация
1. Похожие документы скорится выше несхожих
2. recall@k соответствует цели на eval-наборе
3. Задержка кодирования в рамках бюджета
4. Кэш исключает повторную работу
5. Результаты воспроизводимы с фиксированным seed

## Устранение неполадок
- Плохая похожесть: смените модель или нормализуйте векторы.
- Медленное кодирование: батчи больше или модель меньше.
- Дрейф домена: дообучите эмбеддинги или добавьте keyword-буст.