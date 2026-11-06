---
name: explain-anything
description: "Deconstructs complex algorithms, distributed systems, research papers, and unfamiliar codebases using the Feynman method, progressive 3-layer depth, ASCII mental models, and runnable micro-examples. Use for technical teaching, onboarding, and deep comprehension."
category: education
tags: [education, feynman-technique, onboarding, mental-models, architecture, diagrams, learning]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# Explain Anything (Feynman Mental Models & Code Deconstruction)

> From 1-sentence intuition and ASCII packet flows to runnable 20-line micro-implementations and edge-case invariants.

## Quick Start
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

## When to Use
- Explaining a complex distributed systems protocol (Raft, BGP ECMP, eBPF, MVCC, PagedAttention) to a junior or cross-functional engineer
- Summarizing a dense academic paper or RFC into a reproducible mental model and minimal code prototype
- Creating onboarding guides for an unfamiliar repository by tracing a single request from entrypoint to database commit
- Using the build-your-own-x philosophy ('What I cannot create, I do not understand') to master core infrastructure

## Best Practices
- Always explain the problem *before* naming the abstraction: show why naive approaches fail first so the reader feels the necessity of the design.
- Trace one concrete item with real values (e.g., 'Request ID=42 updating balance from $100 to $80') instead of abstract variables X, Y, and Z.
- Draw a compact ASCII state-transition or data-flow diagram showing exact inputs, transformations, and outputs.
- Provide a 15-to-30-line runnable Python or Go micro-implementation that captures the core invariant without framework boilerplate.
- End every explanation with a 'Break It to Understand It' question that tests boundary conditions or failure modes.
- Never hide behind circular jargon ('A monad is a monoid in the category of endofunctors'); ground every term in state and data movement.

## Dependencies
```bash
# Run minimal algorithm prototypes with Python
python3 --version
```

## Examples
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

## Step-by-Step
1. Identify the core friction: state in 2 sentences what breaks if we use a naive approach without this technology.
2. Write the Layer 1 intuition (1-2 sentences using a concrete physical analogy with clear limits).
3. Draw the Layer 2 ASCII data-flow or state diagram tracing a single concrete payload.
4. Write the Layer 3 minimal runnable code (< 30 lines) implementing the core invariant.
5. Document the Layer 4 production edge cases (where the simple mental model breaks under concurrency, network partitions, or scale).
6. Add 2 'Check Your Intuition' failure scenarios with answers.

## Validation
1. Explanation begins with the concrete failure mode of the naive approach before introducing terminology
2. Includes an ASCII state/flow diagram with concrete sample values rather than generic placeholders
3. Minimal code block runs standalone and passes assertions in under 30 lines
4. Explicitly states at least 2 production edge cases or trade-offs

## Troubleshooting
- Analogy misleads advanced readers — explicitly state where the analogy stops working and transition immediately to the exact byte/packet mechanics.
- Codebase onboarding guide becomes a file-by-file directory listing — delete the directory tree and trace one end-to-end HTTP request or CLI command instead.
- Explanation still feels abstract — replace every variable name like `data` or `item` with a concrete domain payload (`order_42`, `jwt_token`).
- Reader gets lost in math notation — map every symbol in an equation to its corresponding variable in a 10-line Python snippet.
