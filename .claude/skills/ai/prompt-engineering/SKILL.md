---
name: prompt-engineering
description: "Design effective prompts for LLMs: role framing, structured output, chain-of-thought, few-shot, and evaluation. Use to get reliable model behavior."
category: ai
tags: [prompt-engineering, llm, prompting, chain-of-thought, structured-output]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-20
updated: 2026-09-28
author: ssrjkk
---
# Prompt Engineering

> Designing prompts that reliably steer LLM behavior.

## Quick Start
```text
You are a senior Python code reviewer.
Review the code below for bugs, security issues, and style.
Output a markdown report with sections: Issues, Severity, Fix.
```

## When to Use
- Getting consistent structured output from LLMs
- Reducing hallucinations in critical workflows
- Making prompts robust across models and versions
- Building prompts for agents and tools

## Best Practices

### Framing
- Give the model a clear role and task
- State constraints explicitly (format, length, tone)
- Provide context before asking the question
- Ask for one thing per prompt when possible

### Structured Output
- Ask for JSON/YAML with a schema
- Use few-shot examples of the desired format
- Request self-checking: "validate your JSON before responding"
- Prefer `response_format`/tools when the API supports them

### Reasoning
- Use chain-of-thought for multi-step problems
- Ask for step-by-step reasoning before the final answer
- Keep reasoning separate from the final deliverable
- Avoid leaking internal reasoning into user-facing output

## Dependencies
```bash
pip install openai   # or anthropic, google-generativeai
```

## Examples
```text
# Structured JSON extraction
Extract entities from the text below as JSON.
Schema: {"name": string, "org": string|null, "confidence": float 0-1}
Return only valid JSON, no commentary.

Text: "Alice works at Acme and handles billing."
```

```text
# Chain-of-thought
Solve the math problem step by step, then give the final answer.
Show each calculation. End with: "Answer: <number>".

Problem: A train travels 240 km in 3 hours. What is the average speed?
```

```python
import openai

client = openai.OpenAI()
resp = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": "You extract entities to JSON."},
        {"role": "user", "content": '{"text": "Alice works at Acme"}'},
    ],
    response_format={"type": "json_object"},
)
print(resp.choices[0].message.content)
```

```python
# Evaluate prompt quality on a test set
def score_prompt(prompt: str, cases: list[tuple[str, str]]) -> float:
    correct = 0
    for inp, expected in cases:
        out = run_model(prompt, inp)
        if normalize(out) == normalize(expected):
            correct += 1
    return correct / len(cases)
```

## Step-by-Step
1. Define the task, expected output, and failure modes.
2. Write a role + constraints prompt; include an output schema.
3. Add 2-3 few-shot examples of the exact format.
4. For reasoning tasks, request step-by-step with separated final answer.
5. Test against a held-out set; measure accuracy and format compliance.
6. Iterate: add failing cases, tighten constraints, trim noise.
7. Version prompts; pin model and temperature.
8. Monitor drift and re-evaluate on schedule.

## Validation
1. Output parses as valid JSON/YAML when structured
2. Accuracy on the eval set meets the target
3. Prompt works across the target models
4. No prompt injection from user content (sandbox untrusted input)
5. Latency and cost within budget

## Troubleshooting
- Output not JSON: tighten schema, add few-shot, use response_format.
- Hallucinations: add grounding context and ask for citations.
- Verbose answers: constrain length and format in the prompt.