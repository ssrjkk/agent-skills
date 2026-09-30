---
name: structured-output
description: "Force LLMs to emit valid, schema-constrained structured output: JSON modes, function calling, JSON Schema validation, and error recovery. Use for reliable data extraction."
category: ai
tags: [structured-output, json, json-schema, llm, extraction, validation]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Structured Output

> Getting LLMs to reliably emit valid, schema-constrained output.

## Quick Start
```bash
pip install openai pydantic jsonschema
# combine response_format with a JSON Schema for guaranteed shape
```

## When to Use
- Data extraction into typed records
- API responses that must match a contract
- Tool/function arguments generation
- Reducing malformed-output handling

## Best Practices

### Schema Design
- Define a strict JSON Schema per output shape
- Use `additionalProperties: false` to reject surprises
- Keep schemas flat and primitive where possible
- Version schemas alongside your code

### Mode Selection
- Prefer the provider's `response_format` (json_object / json_schema)
- Use function/tool calling when the output feeds a tool
- Fall back to few-shot + validation for models without structured mode
- Never trust unvalidated text

### Validation & Recovery
- Validate every response against the schema
- Re-prompt with the validation error on failure
- Cap retries; fall back to a default record
- Log malformed responses for prompt tuning

## Dependencies
```bash
pip install openai pydantic jsonschema
```

## Examples
```python
import json
import openai
from jsonschema import validate, ValidationError

client = openai.OpenAI()

SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0},
        "emails": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["name", "age"],
    "additionalProperties": False,
}

def extract(text: str) -> dict:
    resp = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": f"Extract from: {text}"}],
        response_format={"type": "json_schema", "json_schema": {"name": "person", "schema": SCHEMA}},
    )
    return json.loads(resp.choices[0].message.content)
```
```python
# Validate and recover on failure
def safe_extract(text: str, retries: int = 2) -> dict:
    for attempt in range(retries):
        raw = extract(text)
        try:
            validate(instance=raw, schema=SCHEMA)
            return raw
        except ValidationError as e:
            print(f"retry {attempt}: {e.message}")
    return {"name": "unknown", "age": 0}
```
```python
# Pydantic-based extraction
from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str
    age: int = Field(ge=0)
    emails: list[str] = []

resp = client.beta.chat.completions.parse(
    model="gpt-5",
    messages=[{"role": "user", "content": "Alice is 30, email a@b.com"}],
    response_format=Person,
)
print(resp.choices[0].message.parsed.model_dump())
```
```python
# JSON mode fallback for providers without json_schema
def extract_json_mode(text: str) -> dict:
    resp = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "Respond only with valid JSON matching the schema."},
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content)
```

## Step-by-Step
1. Define the exact output shape as a JSON Schema.
2. Pick the strictest mode the provider supports (schema > json_object > few-shot).
3. Implement extraction with the schema attached.
4. Validate every response; re-prompt with errors on mismatch.
5. Add retry limits and safe defaults.
6. Log failures to improve the prompt or schema.
7. Add tests with realistic inputs including edge cases.
8. Version schemas and monitor drift.

## Validation
1. All outputs parse as valid JSON
2. Every output satisfies the schema (validated programmatically)
3. Invalid inputs still yield schema-conforming records
4. Retry recovery works without infinite loops
5. Contract changes are versioned

## Troubleshooting
- Output fails schema: tighten the prompt, add examples, or narrow the schema.
- `additionalProperties` errors: expected extra fields — adjust the schema.
- Model ignores format: switch to function calling or guided generation.