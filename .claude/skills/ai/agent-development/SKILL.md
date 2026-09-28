---
name: agent-development
description: "Build reliable LLM agents and agentic workflows: tool use, memory, loops, guardrails, and evaluation. Use for autonomous AI systems."
category: ai
tags: [agents, agentic, tool-use, orchestration, llm, workflows, autonomy]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-20
updated: 2026-09-28
author: ssrjkk
---
# Agent Development

> Building reliable LLM agents with tools, memory, and guardrails.

## Quick Start
```bash
pip install openai
# define tools, a loop, and safety limits
```

## When to Use
- Automating multi-step tasks that need decisions
- Coding assistants, research agents, customer support
- Workflows that call tools and iterate
- When a single prompt is not enough

## Best Practices

### Tool Design
- Give tools clear names, descriptions, and JSON schemas
- Make tools deterministic and side-effect-aware
- Validate tool inputs; return structured errors
- Keep the tool surface small and focused

### Agent Loop
- Structure: perceive -> decide -> act -> observe
- Cap the number of steps (max_iterations)
- Detect loops and stuck states; add a stop condition
- Log every step (tool, input, output) for debugging

### Memory
- Use short-term context + long-term store (vector DB)
- Summarize conversation to fit context windows
- Persist important state across sessions
- Separate user facts from session facts

### Safety
- Restrict destructive tools (delete, deploy, pay) with approvals
- Sandbox code execution; deny dangerous commands
- Add guardrails: content filters, budget limits, timeouts
- Escape prompt injection in tool outputs and user data

## Dependencies
```bash
pip install openai pydantic
# optional: langgraph, crewai, or your own loop
```

## Examples
```python
from pydantic import BaseModel, Field

class WeatherTool:
    name = "get_weather"
    description = "Get current weather for a city"
    schema = {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
    }

    def run(self, city: str) -> str:
        return f"Weather in {city}: sunny, 22C"
```
```python
# Minimal agent loop with max steps
def run_agent(user_input: str, tools: dict, max_steps: int = 10) -> str:
    messages = [{"role": "user", "content": user_input}]
    for _ in range(max_steps):
        resp = call_llm(messages, tools=list(tools.values()))
        if not resp.tool_calls:
            return resp.content
        for call in resp.tool_calls:
            result = tools[call.function.name].run(**call.function.arguments)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
    return "Reached max steps without final answer."
```
```python
# Approval gate for destructive actions
def run_tool_safe(name: str, args: dict) -> str:
    if name in DANGEROUS_TOOLS:
        if not confirm(f"Approve {name}({args})? "):
            return "Action denied by user."
    return tools[name].run(**args)
```
```python
# Summarize context to fit window
def compress(messages, keep_last=6):
    head = messages[:2]                      # system + original
    tail = messages[-keep_last:]
    summary = summarize(messages[2:-keep_last])
    return head + [{"role": "assistant", "content": f"[Summary] {summary}"}] + tail
```

## Step-by-Step
1. Define the agent's goal, inputs, and stopping criteria.
2. Design a small set of tools with clear schemas.
3. Implement the perceive-decide-act loop with max steps.
4. Add memory: short-term context and persistent store.
5. Gate dangerous actions behind approvals.
6. Add guardrails: budget, timeout, content filters.
7. Evaluate on a benchmark of representative tasks.
8. Log traces for debugging and regressions.

## Validation
1. Agent completes tasks within max steps
2. No infinite loops or repeated identical actions
3. Destructive tools require approval
4. Tool errors are handled gracefully (retry or explain)
5. Cost and latency within budget on the eval set

## Troubleshooting
- Agent loops: tighten max_steps and detect repeated tool calls.
- Wrong tool calls: improve tool descriptions and schemas.
- Context overflow: summarize and trim older turns.