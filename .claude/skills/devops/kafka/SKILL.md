---
name: kafka
description: "Design and operate Kafka event streaming: topics, producers, consumers, consumer groups, partitioning, and exactly-once. Use for event-driven systems."
category: devops
tags: [kafka, event-streaming, message-queue, topics, consumers, partitioning, streaming]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-26
updated: 2026-09-28
author: ssrjkk
---
# Kafka

> Building reliable event streaming with Apache Kafka.

## Quick Start
```bash
docker compose up -d  # single-node kafka
kafka-topics --bootstrap-server localhost:9092 --create --topic events --partitions 3
kafka-console-producer --bootstrap-server localhost:9092 --topic events
```

## When to Use
- Event-driven architecture and decoupling
- High-throughput log ingestion and analytics
- Stream processing (join, aggregate, window)
- Durable message replay for consumers

## Best Practices

### Topics & Partitioning
- Model topics by event type, not by consumer
- Partition by key for ordering within a key
- Choose partition count based on throughput
- Set retention per topic (time and size)

### Producers
- Use a key for order/co-partitioning needs
- Set acks (all) for durability; tune batching
- Handle retries and idempotence (enable idempotent producer)
- Monitor `record-error-rate` and latency

### Consumers
- Use consumer groups for scale
- Handle rebalance gracefully
- Commit offsets after processing (at-least-once)
- Make consumption idempotent for exactly-once semantics

### Operations
- Run at least 3 brokers with replication factor 3
- Monitor lag, under-replicated partitions, and disk
- Use Schema Registry for schema evolution
- Set alerts on consumer lag

## Dependencies
```bash
# Python client
pip install confluent-kafka
# or Java:
# org.apache.kafka:kafka-clients
```

## Examples
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
    process(msg.value())        # idempotent processing
    c.commit(asynchronous=False)  # commit after processing
```
```java
// Java producer with acks and idempotence
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
# Monitor consumer lag
kafka-consumer-groups --bootstrap-server localhost:9092 \
  --describe --group analytics
```

## Step-by-Step
1. Define event types and topic names up front.
2. Choose partitioning strategy per key.
3. Set replication factor and retention.
4. Implement producers with acks and idempotence.
5. Implement consumers with graceful rebalance and offsets.
6. Make processing idempotent for safe replays.
7. Use Schema Registry for contract evolution.
8. Monitor lag, disk, and error rates.

## Validation
1. Producers send without errors under load
2. Consumers process in order within a key
3. Consumer lag stays near zero at steady state
4. Rebalances don't lose or duplicate processed events
5. Replaying from an offset produces identical results

## Troubleshooting
- High lag: scale consumers or optimize processing.
- Out-of-order: partition by key and check single-consumer-per-partition.
- Duplicates: make processing idempotent or use exactly-once.