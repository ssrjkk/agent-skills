---
name: function-calling
description: "Implement robust LLM function/tool calling: schemas, multi-call handling, validation, error recovery, and structured execution. Use for agent tool use."
category: ai
tags: [function-calling, tool-use, llm, structured-output, agents, json-schema]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-25
updated: 2026-09-28
author: ssrjkk
---
# Function Calling

> Wiring LLMs to real functions with robust tool calling.

## Quick Start
```bash
pip install openai
# declare tools, let the model call them, execute, and loop
```

## When to Use
- Letting the model query data, compute, or take actions
- Structured extraction into defined function inputs
- Agentic workflows that alternate reasoning and tool calls
- Reducing hallucination by constraining output to schemas

## Best Practices

### Tool Schemas
- Write clear, complete JSON schemas per function
- Use `description` on every param to guide the model
- Enforce `required` and sensible `enum`/`pattern`
- Keep parameter names self-explanatory

### Calling Loop
- Detect tool_calls; execute them; append results as `tool` messages
- Support multiple tool calls in one response
- Include the `tool_call_id` on every result
- Cap iterations to avoid runaway loops

### Validation & Recovery
- Validate arguments before execution
- Return structured errors that the model can read
- Never auto-execute dangerous tools without approval
- Log the full call trace for debugging

### Prompting
- Give the model context on when to call each tool
- Ask it to use tools instead of guessing answers
- Provide examples of tool usage in the system prompt
- Keep tool descriptions aligned with actual behavior

## Dependencies
```bash
pip install openai pydantic
# optional: instructor for schema-guided calls
```

## Examples
```python
import openai

client = openai.OpenAI()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
        },
    }
]

resp = client.chat.completions.create(
    model="gpt-6",
    messages=[{"role": "user", "content": "Weather in Tokyo?"}],
    tools=TOOLS,
)
call = resp.choices[0].message.tool_calls[0]
print(call.function.name, call.function.arguments)
```
```python
# Execute the call and feed the result back
import json

def dispatch(name: str, args: dict) -> str:
    if name == "get_weather":
        return weather_api(args["city"])
    return json.dumps({"error": f"unknown tool: {name}"})

result = dispatch(call.function.name, json.loads(call.function.arguments))
messages = [
    {"role": "user", "content": "Weather in Tokyo?"},
    resp.choices[0].message,
    {"role": "tool", "tool_call_id": call.id, "content": result},
]
final = client.chat.completions.create(model="gpt-6", messages=messages, tools=TOOLS)
print(final.choices[0].message.content)
```
```python
# Multi-call handling
def run_tools(message) -> list[dict]:
    results = []
    for call in message.tool_calls:
        args = json.loads(call.function.arguments)
        results.append(
            {"role": "tool", "tool_call_id": call.id, "content": dispatch(call.function.name, args)}
        )
    return results
```
```python
# Validation with pydantic before execution
from pydantic import BaseModel, ValidationError

class WeatherArgs(BaseModel):
    city: str
    units: str = "metric"

def safe_dispatch(name: str, args: dict) -> str:
    try:
        if name == "get_weather":
            w = WeatherArgs(**args)
            return weather_api(w.city, w.units)
        return f'{{"error": "unknown tool {name}"}}'
    except ValidationError as e:
        return f'{{"error": "invalid args: {e}"}}'
```

## Step-by-Step
1. Write the tool functions you want the model to call.
2. Define JSON schemas with descriptions and required fields.
3. Send the first request with `tools` and user intent.
4. Execute returned `tool_calls` and append results with IDs.
5. Loop until the model returns a final text answer.
6. Validate args; return structured errors the model can use.
7. Add guardrails for dangerous actions.
8. Log traces; test with edge cases and malformed args.

## Validation
1. Model emits valid, schema-conforming calls for the test set
2. Multi-call responses are executed in order
3. Errors are surfaced back to the model for recovery
4. Loop terminates within the iteration cap
5. Dangerous tools require explicit approval

## Troubleshooting
- Model skips tools: add tool usage examples to the system prompt.
- Invalid JSON args: loosen schemas or use guided generation.
- Loops: cap iterations and detect repeated identical calls.