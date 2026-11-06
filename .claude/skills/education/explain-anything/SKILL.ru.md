---
name: explain-anything
description: "Deconstructs complex algorithms, distributed systems, research papers, and unfamiliar codebases using the Feynman method, progressive 3-layer depth, ASCII mental models, and runnable micro-examples. Use for technical teaching, onboarding, and deep comprehension."
category: education
tags: [education, feynman-technique, onboarding, mental-models, architecture, diagrams, learning]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
language: ru
original: explain-anything
author: ssrjkk
---
# Explain Anything (Объяснение сложных систем по методу Фейнмана)

> Разбор сложных алгоритмов, протоколов, научных статей и чужих кодовых баз через интуицию, ASCII-схемы и минимальный код.

## Быстрый старт
```markdown
# 4-Layer Feynman Deconstruction Template
1. Why It Exists (The Pain): What broke before this concept was invented?
2. 1-Sentence Intuition: Explain the mechanism using a physical or everyday system without jargon.
3. ASCII Packet/Data Flow: Trace 1 concrete input from entry to exit with exact state changes.
4. 20-Line Runnable Core: Strip away 95% of boilerplate and show the core loop in code.
```

```python
# Layer 4 Example: Token Bucket rate limiter core mechanics in 15 lines of Python
import time

class TokenBucket:
    def __init__(self, rate_per_sec: float, capacity: float) -> None:
        self.rate, self.capacity, self.tokens = rate_per_sec, capacity, capacity
        self.updated_at = time.monotonic()

    def allow(self, cost: float = 1.0) -> bool:
        now = time.monotonic()
        self.tokens = min(self.capacity, self.tokens + (now - self.updated_at) * self.rate)
        self.updated_at = now
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False
```

## Когда использовать
- Объяснение сложной технологии (консенсус Raft, BGP ECMP, eBPF, MVCC в Postgres, PagedAttention в vLLM) простым и точным языком
- Разбор научной статьи, RFC или спецификации с выделением главной математической/инженерной идеи и рабочего прототипа
- Быстрый онбординг в незнакомый репозиторий через трассировку одного конкретного запроса от HTTP-входа до записи в БД
- Изучение фундаментальных технологий по принципу Ричарда Фейнмана (build-your-own-x): напиши минимальное ядро сам, чтобы понять до конца

## Лучшие практики
- Сначала покажите боль и поломку наивного решения, и только потом вводите новый термин или алгоритм как спасение от этой проблемы.
- Трассируйте один конкретный объект с реальными числами («Запрос #42 списывает 200 ₽ со счета #7»), а не абстрактные сущности Foo и Bar.
- Рисуйте наглядную ASCII-схему движения пакета или смены состояний в памяти на каждом шаге алгоритма.
- Приводите минимальную рабочую реализацию ядра алгоритма на 15–30 строк кода без лишних фреймворков и оберток.
- Завершайте разбор проверочным вопросом «А что сломается, если...?», проверяющим понимание граничных условий.
- Не объясняйте непонятное через непонятное: за каждым термином всегда показывайте конкретный байт, указатель, таблицу или сетевой пакет.

## Зависимости
```bash
# Run minimal algorithm prototypes with Python
python3 --version
```

## Примеры
```markdown
# ASCII Mental Model: Why Deleted Files Still Fill Disk (`df -h` 100% vs `du -sh` 20%)
Directory Entry (`/var/log/app.log`) --[rm app.log]--> Unlinked from directory tree (`du` cannot see it)
                                                             |
Kernel Inode #88412 (40 GB data blocks) <---[fd #4 open]--- Running Process PID 1942 (`df` still counts blocks!)
Fix: `: > /proc/1942/fd/4` zeroes the inode blocks immediately without killing PID 1942.
```

```python
# Minimal Consistent Hashing Ring in 22 lines of Python
import bisect
import hashlib

class HashRing:
    def __init__(self, nodes: list[str], vnodes: int = 32) -> None:
        self.ring: list[tuple[int, str]] = []
        for n in nodes:
            for i in range(vnodes):
                h = int(hashlib.md5(f"{n}:{i}".encode()).hexdigest(), 16)
                bisect.insort(self.ring, (h, n))

    def get_node(self, key: str) -> str:
        h = int(hashlib.md5(key.encode()).hexdigest(), 16)
        idx = bisect.bisect_right(self.ring, (h, "")) % len(self.ring)
        return self.ring[idx][1]

ring = HashRing(["node-a", "node-b", "node-c"])
assert ring.get_node("user:42") in {"node-a", "node-b", "node-c"}
```

## Пошаговое руководство
1. Сформулируйте исходную боль в 2 предложениях: что именно падает или тормозит, если решить задачу «в лоб» без этой технологии.
2. Дайте интуитивную аналогию первого уровня (1–2 предложения на понятной жизненной или физической модели).
3. Нарисуйте ASCII-схему второго уровня, проводя один конкретный пакет данных через все узлы или структуры памяти.
4. Напишите минимальный рабочий код третьего уровня (до 30 строк), реализующий главную идею алгоритма с нуля.
5. Разберите четвертый уровень — продакшн-нюансы и граничные случаи (гонки потоков, сетевой split-brain, переполнение памяти).
6. Добавьте 2 контрольных вопроса «Что произойдет при сбое X?» с кратким разбором ответа.

## Валидация
1. Разбор начинается с демонстрации проблемы наивного решения до введения сложной терминологии
2. Присутствует наглядная ASCII-схема с конкретными числами и состояниями вместо абстрактных квадратиков
3. Минимальный пример кода запускается автономно, укладывается в 30 строк и проходит проверку assert
4. Явно разобраны минимум 2 граничных случая или компромисса при работе под высокой нагрузкой

## Устранение неполадок
- Бытовая аналогия уводит в сторону от сути — четко укажите границу аналогии и сразу перейдите к реальному устройству памяти или протокола.
- Онбординг по репозиторию превратился в скучный список папок — удалите оглавление директорий и проведите читателя по пути одного живого запроса.
- Объяснение все еще кажется абстрактным — замените переменные `data` и `item` на предметные данные (`order_42`, `wal_segment`).
- Формула из статьи пугает нагромождением индексов — сопоставьте каждый символ формулы с переменной в 10-строчном коде на Python.
