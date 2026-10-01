---
name: context-engineering
description: "Curate LLM context windows for quality and cost: system prompts, compaction, just-in-time retrieval, progressive disclosure, and token budgets. Use for effective agent context."
category: ai
tags: [context-engineering, context-window, tokens, agents, compaction, retrieval]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Context Engineering

> Curating the context window for better answers and lower cost.

## Quick Start
```python
# Keep a small stable system prompt, fetch only what the task needs
SYSTEM = "You are a concise senior engineer."
TASK = "Fix the bug in src/auth.py"
```

## When to Use
- Long agent sessions that grow beyond the window
- RAG where too much context hurts quality
- Cost-sensitive high-volume LLM calls
- Multi-turn agents with memory needs

## Best Practices

### Context Budgeting
- Set a token budget per section (system, task, memory, retrieval)
- Keep system prompt small and high-signal
- Trim retrieved chunks to the top-k and relevant spans
- Reserve space for the answer

### Compaction
- Summarize old turns instead of keeping raw history
- Use structured summaries (decisions, actions, open items)
- Keep the last turns verbatim for immediate coherence
- Trigger compaction at a token threshold

### Progressive Disclosure
- Load details only when needed (lazy retrieval)
- Use summaries + pointers to deeper docs
- Ask clarifying questions before pulling big context
- Keep examples cached, not repeated

### Retrieval Quality
- Retrieve on demand, not everything up front
- Rerank and deduplicate before injecting
- Cite sources so the model can verify
- Keep injected context fresh and relevant

## Dependencies
```bash
pip install tiktoken openai
# tokenizer for budgeting
```

## Examples
```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    return len(enc.encode(text))

BUDGET = {"system": 500, "task": 1000, "memory": 1500, "retrieval": 2000}
print(count_tokens("hello world"))
```
```python
# Compaction with structured summary
def compact(history: list[dict], summary: str, keep_last: int = 6) -> list[dict]:
    return [
        {"role": "system", "content": f"Conversation summary so far:\n{summary}"}
    ] + history[-keep_last:]
```
```python
# Lazy retrieval: only fetch when needed
def build_context(question: str, memory: dict) -> str:
    chunks = []
    if "codebase" in question.lower():
        chunks += retrieve("code", question, k=4)
    if "api" in question.lower():
        chunks += retrieve("api_docs", question, k=2)
    return "\n\n".join(chunks)[:BUDGET["retrieval"]]
```
```python
# Token-aware trimming
def trim_to_budget(text: str, budget: int) -> str:
    tokens = enc.encode(text)
    if len(tokens) <= budget:
        return text
    return enc.decode(tokens[:budget]) + "\n...[trimmed]"
```

## Step-by-Step
1. Define a per-section token budget for your task.
2. Write a tight system prompt with role and constraints.
3. Retrieve only what the current turn needs (lazy).
4. Inject top-k, deduplicated, cited chunks.
5. Summarize older turns into structured memory.
6. Trim long content to the budget.
7. Measure token usage and cost per call.
8. Iterate on budgets based on answer quality.

## Validation
1. Answers stay correct as the session grows
2. Token cost per call is within budget
3. Retrieved context is relevant (recall@k)
4. Compaction preserves decisions and facts
5. No budget overflow errors in production

## Troubleshooting
- Context overflow: compact earlier and trim harder.
- Lost facts after compaction: improve the summary format.
- Low quality with much context: reduce injected chunks, keep only relevant.