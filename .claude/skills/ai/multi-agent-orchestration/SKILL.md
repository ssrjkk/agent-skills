---
name: multi-agent-orchestration
description: "Design and run multi-agent systems: orchestrator-worker, routing, handoffs, shared state, and coordination patterns. Use for complex agent teams."
category: ai
tags: [multi-agent, orchestration, agents, coordination, workflows, teams]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Multi-Agent Orchestration

> Coordinating multiple specialized agents into reliable systems.

## Quick Start
```python
# Orchestrator picks a worker per task; workers return results
from dataclasses import dataclass

@dataclass
class AgentResult:
    task: str
    output: str
```

## When to Use
- Tasks needing different specializations (research, code, review)
- Parallelizable independent subtasks
- Long workflows broken into reliable steps
- Complex domains a single agent handles poorly

## Best Practices

### Orchestrator-Worker
- Orchestrator plans, delegates, and collects results
- Workers are single-purpose and stateless
- Define a clear task handoff contract
- Cap concurrent workers and total steps

### Routing & Handoffs
- Route by task type, not by guesswork
- Use explicit handoff messages (intent + context)
- Validate worker outputs before handoff
- Fall back to a default worker on routing failure

### Shared State
- Use a shared store for facts and artifacts
- Avoid duplicated context; reference by ID
- Coordinate writes to avoid races
- Log the full execution trace

### Reliability
- Retry failed workers with backoff
- Set timeouts and budgets per worker
- Detect loops and deadlocks
- Aggregate partial results on failure

## Dependencies
```bash
pip install openai pydantic
# optional: langgraph, autogen, crewai
```

## Examples
```python
# Minimal orchestrator
def orchestrate(task: str, workers: dict) -> dict:
    plan = plan_task(task)          # picks worker names
    results = {}
    for name, sub in plan.items():
        results[name] = workers[name](sub)
    return {"plan": plan, "results": results}
```
```python
# Worker contract
def researcher(query: str) -> str:
    return run_llm(f"Research: {query}")

def reviewer(text: str) -> str:
    return run_llm(f"Review for correctness and style:\n{text}")
```
```python
# Routing by intent
def route(task: str) -> str:
    intent = classify(task)
    if intent == "research":
        return "researcher"
    if intent == "review":
        return "reviewer"
    return "general"
```
```python
# Parallel execution with a thread pool
from concurrent.futures import ThreadPoolExecutor

def run_parallel(workers: dict, tasks: dict) -> dict:
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {name: ex.submit(workers[name], task) for name, task in tasks.items()}
        return {name: f.result() for name, f in futures.items()}
```

## Step-by-Step
1. Split the domain into single-purpose worker roles.
2. Define the handoff contract (task, context, output format).
3. Build an orchestrator that plans and routes.
4. Add a shared state store for artifacts.
5. Run independent subtasks in parallel with limits.
6. Add retries, timeouts, and budgets.
7. Validate outputs at each handoff.
8. Trace and log the full execution.

## Validation
1. Or orchestrator completes within step/time budgets
2. Workers receive well-formed tasks
3. Handoffs carry necessary context
4. Parallel tasks don't corrupt shared state
5. Failures degrade gracefully with partial results

## Troubleshooting
- Deadlock: remove circular handoffs; add timeouts.
- Context loss on handoff: carry intent + summary explicitly.
- Rogue worker: validate outputs and add a review step.