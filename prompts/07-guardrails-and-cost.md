# Guardrails, Refusal Enforcement, Cost Budget

Assume users will attack the agent and finance will audit its bill. Produce the safety-and-cost plan.

## When to use
- Stage 4 of the AI conveyor, when the agent MVP is public

## Prompt
```text
You are an AI platform engineer. Harden this agent:
1. Prompt-injection suite: >= 8 attack cases (indirect via tools, role-play, encoded payloads)
2. Refusal enforcement IN CODE: output schema with refusal field, post-check, retry policy
3. Cost/latency: per-request accounting, monthly budget, alert at 60% and 90%
4. Caching: what to cache (prefixes, RAG chunks), expected savings, eval pass-rate guard
5. Drift: same-input probe set, alarm on quality regression after model/provider updates
Output: ordered checklist with effort per item, plus the injection suite.
Agent: <PASTE THE LOOP AND STACK>
```

## Gate this satisfies
Stage 4 · gates 1-4: injection suite passes, code-enforced refusals, cost/latency alerting, measured caching.
