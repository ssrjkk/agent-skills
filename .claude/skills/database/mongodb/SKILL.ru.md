---
name: mongodb
description: "Design and operate MongoDB: document modeling, queries, indexes, aggregation, replication, and sharding. Use for flexible NoSQL data."
category: database
tags: [mongodb, database, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: mongodb
author: ssrjkk
---
# MongoDB (МонгоДБ)

> Проектирование и эксплуатация гибких документных баз на MongoDB.

## Быстрый старт
```bash
docker run --name mongo -p 27017:27017 -d mongo:8
mongosh
use app
db.users.insertOne({ name: "Alice", role: "admin" })
```

## Когда использовать
- Гибкие или эволюционирующие схемы документов
- Высокая пропускная способность записи и горизонтальное масштабирование
- Денормализованные данные с богатыми запросами
- Прототипирование, где схема меняется быстро

## Лучшие практики

### Моделирование документов
- Встраивайте данные, читаемые вместе; ссылки — на редко меняющиеся
- Избегайте неограниченных массивов (лучше отдельные коллекции)
- Проектируйте под паттерны доступа, а не нормализацию
- `_id` или уникальный индекс — как первичный ключ

### Запросы и индексы
- Индексы под паттерны фильтрации/сортировки
- Составные индексы с корректным порядком полей
- Сначала фильтры равенства, затем диапазоны
- Мониторьте через `explain("executionStats")`

### Агрегация
- Сложные трансформации — через aggregation pipeline
- Match/filter рано, затем group/project
- `$lookup` экономно; предпочитайте встроенные данные
- Лимитируйте стадии и память на пайплайн

### Операции
- Для HA — replica sets; для масштаба — шардинг
- Осознанно задавайте `writeConcern` и `readPreference`
- Включайте auth и TLS; не выставляйте без auth
- Бэкапы через mongodump или Atlas cloud backup

## Зависимости
```bash
docker run --name mongo -p 27017:27017 -d mongo:8
# Python драйвер
pip install pymongo
```

## Примеры
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.app
users = db.users

# Создание с уникальным индексом
users.create_index("email", unique=True)
users.insert_one({"name": "Alice", "email": "alice@example.com", "role": "admin"})
```
```python
# Запрос с фильтром и сортировкой
result = users.find({"role": "admin"}).sort("created_at", -1).limit(10)
for user in result:
    print(user["name"])
```
```python
# Aggregation pipeline
pipeline = [
    {"$match": {"status": "paid"}},
    {"$group": {"_id": "$region", "total": {"$sum": "$amount"}}},
    {"$sort": {"total": -1}},
]
for row in db.orders.aggregate(pipeline):
    print(row)
```
```js
// mongosh: explain для проверки использования индекса
db.users.find({ email: "alice@example.com" }).explain("executionStats");
```

## Пошаговое руководство
1. Смоделируйте документы под паттерны чтения.
2. Решите embed vs reference для каждой связи.
3. Создайте индексы под горячие запросы.
4. Напишите запросы и aggregation pipelines.
5. Проверьте `explain()`, что индексы используются.
6. Для прода — replica set.
7. Включите auth и TLS; ограничьте сетевой доступ.
8. Настройте бэкапы и мониторинг метрик.

## Валидация
1. Горячие запросы используют индексы (explain показывает IXSCAN)
2. Модель документов соответствует паттернам доступа
3. Результаты агрегаций корректны
4. В replica set здоровый primary
5. Бэкап/восстановление протестированы на стейджинге

## Устранение неполадок
- Медленные запросы: добавьте/составьте индексы; проверьте сортировку.
- Неограниченный рост: вынесите встроенные массивы в коллекции.
- Разрывы соединений: используйте пул соединений и retry-записи.