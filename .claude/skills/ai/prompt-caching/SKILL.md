---
name: prompt-caching
description: "Optimize LLM cost and latency with prompt caching: cacheable prefixes, cache-control headers, context layout, and cache-aware prompting. Use for high-volume apps."
category: ai
tags: [prompt-caching, caching, llm, cost, latency, context, optimization]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-25
updated: 2026-09-28
author: ssrjkk
---
# Prompt Caching

> Cutting LLM cost and latency by caching repeated prompt prefixes.

## Quick Start
```python
# Put stable content first, mark it as cacheable
resp = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": LONG_SYSTEM_PROMPT},
        {"role": "user", "content": dynamic_question},
    ],
    extra_headers={"Cache-Control": "ttl=3600, min_tokens=1024"},
)
```

## When to Use
- Chat with long system prompts or tool definitions
- Agents with large context that repeats across turns
- RAG apps where system instructions are stable
- High-volume endpoints where cost matters

## Best Practices

### Layout
- Put stable content first: system prompt, tools, static context
- Put dynamic content last: user turns, retrieved chunks
- Keep a stable prefix across all requests
- Minimum cacheable size varies by provider (e.g., 1024+ tokens)

### Cache-Control
- Mark cacheable segments with cache-control headers
- Set a TTL that matches your access pattern
- Don't cache secrets or per-user data
- Verify cache hits via usage metadata (`cached_tokens`)

### Design for Caching
- Keep the system prompt identical across calls
- Separate static tool definitions from dynamic input
- Reuse the same prefix for the whole conversation
- Batch ephemeral data at the end of the context

### Measurement
- Track cached vs uncached tokens in usage
- Measure latency improvement per request
- Monitor cache hit rate over time
- Compare cost before and after optimization

## Dependencies
```bash
pip install openai anthropic
```

## Examples
```python
import openai

client = openai.OpenAI()

# Stable prefix: system prompt + tools, marked cacheable
STATIC = [
    {"role": "system", "content": "You are a senior support agent."},
    {"role": "user", "content": "Available tools: search, refund, escalate."},
]

def ask(question: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-5",
        messages=STATIC + [{"role": "user", "content": question}],
        extra_headers={"Cache-Control": "ttl=3600, min_tokens=1024"},
    )
    usage = resp.usage
    print("cached:", getattr(usage, "prompt_tokens_details", None))
    return resp.choices[0].message.content
```
```python
# Anthropic-style cache control
import anthropic

client = anthropic.Anthropic()

def ask(question: str) -> str:
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=[
            {"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}},
        ],
        messages=[{"role": "user", "content": question}],
    )
    print("cache:", resp.usage.cache_creation_input_tokens, resp.usage.cache_read_input_tokens)
    return resp.content[0].text
```
```python
# Session-style caching: stable system across a conversation
def chat_session():
    messages = list(STATIC)
    while True:
        q = input("> ")
        resp = client.chat.completions.create(
            model="gpt-5", messages=messages + [{"role": "user", "content": q}],
            extra_headers={"Cache-Control": "ttl=3600, min_tokens=1024"},
        )
        answer = resp.choices[0].message.content
        messages.append({"role": "user", "content": q})
        messages.append({"role": "assistant", "content": answer})
        print(answer)
```
```python
# Verify cache hits from usage metadata
def report_cache(usage) -> dict:
    details = getattr(usage, "prompt_tokens_details", None) or {}
    cached = getattr(details, "cached_tokens", 0)
    total = usage.prompt_tokens
    return {"cached": cached, "total": total, "rate": cached / total if total else 0}
```

## Step-by-Step
1. Identify the stable prefix in your prompts (system, tools, static).
2. Move dynamic content to the end of the context.
3. Mark the prefix cacheable with the provider's mechanism.
4. Verify cache hits in usage metadata.
5. Measure latency and cost before/after.
6. Tune TTL and minimum tokens to your traffic.
7. Avoid caching per-user or secret data.
8. Monitor hit rate and keep the prefix byte-identical.

## Validation
1. Usage shows cached tokens on repeat requests
2. Latency drops for the cached portion
3. Cost per request decreases measurably
4. Responses stay correct after cache hits
5. Secrets are not in the cacheable prefix

## Troubleshooting
- No cache hits: prefix differs between calls — keep it byte-identical.
- Short prompts: raise the prefix above the provider minimum.
- Cache invalidation: changing the prefix invalidates; redesign for stability.