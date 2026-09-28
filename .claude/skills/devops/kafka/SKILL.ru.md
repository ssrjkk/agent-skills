---
name: kafka
description: "Design and operate Kafka event streaming: topics, producers, consumers, consumer groups, partitioning, and exactly-once. Use for event-driven systems."
category: devops
tags: [kafka, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: kafka
author: ssrjkk
---
# Kafka (Кафка)

> Построение надёжного event streaming на Apache Kafka.

## Быстрый старт
```bash
docker compose up -d  # однонодовый kafka
kafka-topics --bootstrap-server localhost:9092 --create --topic events --partitions 3
kafka-console-producer --bootstrap-server localhost:9092 --topic events
```

## Когда использовать
- Event-driven архитектура и развязка
- Высокопропускная обработка логов и аналитика
- Stream processing (join, aggregate, window)
- Надёжный replay событий для консьюмеров

## Лучшие практики

### Топики и партиции
- Моделируйте топики по типу события, а не по консьюмеру
- Партиционируйте по ключу для порядка внутри ключа
- Число партиций — под пропускную способность
- Задавайте retention на топик (по времени и размеру)

### Продюсеры
- Ключ — для порядка и co-partitioning
- acks (all) для надёжности; настройте batching
- Обрабатывайте retries и идемпотентность
- Мониторьте `record-error-rate` и задержку

### Консьюмеры
- Для масштаба — consumer groups
- Корректно обрабатывайте rebalance
- Коммитьте offsets после обработки (at-least-once)
- Идемпотентная обработка для exactly-once семантики

### Операции
- Минимум 3 брокера с replication factor 3
- Мониторьте lag, under-replicated partitions и диск
- Для эволюции схем — Schema Registry
- Алерты на consumer lag

## Зависимости
```bash
# Python клиент
pip install confluent-kafka
# или Java:
# org.apache.kafka:kafka-clients
```

## Примеры
```python
from confluent_kafka import Producer

p = Producer({"bootstrap.servers": "localhost:9092"})

def acked(err, msg):
    if err is not None:
        print(f"failed: {err}")

p.produce("events", key="user-42", value=b'{"action":"login"}', callback=acked)
p.flush()
```
```python
from confluent_kafka import Consumer, KafkaError

c = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "analytics",
    "auto.offset.reset": "earliest",
})
c.subscribe(["events"])

while True:
    msg = c.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        break
    process(msg.value())        # идемпотентная обработка
    c.commit(asynchronous=False)  # коммит после обработки
```
```java
// Java producer с acks и идемпотентностью
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("acks", "all");
props.put("enable.idempotence", "true");
KafkaProducer<String, String> producer = new KafkaProducer<>(props);
producer.send(new ProducerRecord<>("events", "user-42", "login"));
```
```bash
# Мониторинг consumer lag
kafka-consumer-groups --bootstrap-server localhost:9092 \
  --describe --group analytics
```

## Пошаговое руководство
1. Определите типы событий и имена топиков заранее.
2. Выберите стратегию партиционирования по ключу.
3. Задайте replication factor и retention.
4. Реализуйте продюсеров с acks и идемпотентностью.
5. Реализуйте консьюмеров с аккуратным rebalance и offsets.
6. Сделайте обработку идемпотентной для безопасных реплеев.
7. Для эволюции контракта — Schema Registry.
8. Мониторьте lag, диск и error rates.

## Валидация
1. Продюсеры шлют без ошибок под нагрузкой
2. Консьюмеры обрабатывают по порядку внутри ключа
3. Consumer lag около нуля в стабильном состоянии
4. Rebalance не теряет и не дублирует события
5. Реплей с offset даёт идентичные результаты

## Устранение неполадок
- Высокий lag: масштабируйте консьюмеров или оптимизируйте обработку.
- Нарушен порядок: партиционируйте по ключу, один консьюмер на партицию.
- Дубликаты: сделайте обработку идемпотентной или используйте exactly-once.