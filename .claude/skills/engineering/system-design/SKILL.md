---
name: system-design
description: "Design scalable systems: requirements, architecture, data models, trade-offs, and scaling strategies. Use for architecture and interviews."
category: engineering
tags: [system-design, architecture, scalability, distributed-systems, trade-offs]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# System Design

> Designing scalable, reliable systems.

## Quick Start
```text
1. Clarify requirements
2. Estimate scale
3. Sketch architecture
4. Design data model
5. Discuss trade-offs
```

## When to Use
- Designing new services or features
- Scaling existing systems
- Architecture reviews and interviews
- Choosing between technologies

## Best Practices

### Requirements
- Clarify functional and non-functional needs
- Estimate users, QPS, data size, storage
- Define latency and availability targets
- State assumptions explicitly

### Architecture
- Start simple: services, DB, cache
- Add components only when justified
- Draw data flow end to end
- Identify single points of failure

### Data Model
- Choose storage by access pattern
- Plan for reads vs writes
- Design for consistency needs
- Consider partitioning and replication

### Scaling
- Scale vertically first, then horizontally
- Add caching for hot reads
- Use queues to decouple writes
- Plan for failure domains

## Dependencies
```bash
# whiteboard or diagramming tool
```

## Examples
```text
Requirements:
- 100M users, 10K QPS peak, 1KB avg request
- p99 latency < 200ms, 99.9% availability
- Reads 90% / writes 10%
```
```text
Estimates:
- 10K QPS * 1KB = ~10 MB/s ingress
- 100M users * 100 bytes = ~10 GB user table
- 30 days retention => ~25 TB storage
```
```
Architecture:
[Client] -> [LB] -> [API services] -> [Cache] -> [DB]
                            \-> [Queue] -> [Workers]
```
```text
Scaling options:
- Cache hot reads (Redis) for 90/10 read-heavy
- Shard user data by user_id
- Queue writes for async processing
- Replicate DB with a read replica
```

## Step-by-Step
1. Clarify requirements and constraints.
2. Estimate scale (QPS, storage, retention).
3. Sketch a simple architecture.
4. Design the data model and storage.
5. Add caching, queues, and replication.
6. Identify bottlenecks and single points of failure.
7. Discuss trade-offs and alternatives.
8. Define monitoring and failure handling.

## Validation
1. Architecture meets the QPS and latency targets
2. Storage estimates are covered
3. No single point of failure
4. Data consistency needs are met
5. Scaling path is clear

## Troubleshooting
- Over-engineering: add components only when needed.
- Missed bottlenecks: trace the data flow and hot paths.
- Unclear trade-offs: compare options with explicit criteria.