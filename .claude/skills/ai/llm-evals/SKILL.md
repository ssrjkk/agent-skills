---
name: llm-evals
description: "Build evaluation suites for LLM applications: golden datasets, metrics, LLM-as-judge, regression gates, and CI integration. Use for trustworthy model behavior."
category: ai
tags: [llm-evals, evaluation, metrics, judge, testing, llm, regression]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-25
updated: 2026-09-28
author: ssrjkk
---
# LLM Evals

> Measuring and guarding LLM application quality with evaluation suites.

## Quick Start
```bash
pip install pytest openai
# collect a golden set, score answers, gate releases in CI
```

## When to Use
- Tracking prompt and model quality over time
- Comparing prompt variants and model versions
- Catching regressions before release
- Building confidence in production agents and RAG

## Best Practices

### Golden Datasets
- Cover happy paths, edge cases, and adversarial inputs
- Use real user queries plus synthetic variations
- Include expected answers or rubrics per case
- Keep the set small (20-100) and maintainable

### Metrics
- Use exact-match for structured outputs (JSON, codes)
- Use similarity for free text (semantic or lexical)
- Prefer LLM-as-judge with a rubric for subjective quality
- Track per-metric scores and aggregate over the set

### LLM-as-Judge
- Give the judge an explicit scoring rubric
- Provide reference answers where possible
- Use a different model than the one evaluated
- Calibrate: spot-check judge vs human labels

### CI Gating
- Run evals on every PR for changed prompts/models
- Set pass thresholds; fail on regressions
- Keep flaky checks out of the blocking path
- Report diffs against the baseline

## Dependencies
```bash
pip install pytest openai numpy
# optional: ragas, promptfoo, deepeval
```

## Examples
```python
import json
import openai

client = openai.OpenAI()

def run_case(prompt: str, user_input: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-6",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input},
        ],
    )
    return resp.choices[0].message.content
```
```python
# Golden set with expected structured output
GOLDEN = [
    {
        "input": "Alice works at Acme.",
        "expected": {"name": "Alice", "org": "Acme"},
    },
    {
        "input": "No company mentioned here.",
        "expected": {"name": None, "org": None},
    },
]

def exact_match(out: str, expected: dict) -> bool:
    try:
        return json.loads(out) == expected
    except json.JSONDecodeError:
        return False
```
```python
# LLM-as-judge with rubric
JUDGE_PROMPT = """Rate the answer 1-5 using this rubric:
5 = correct, complete, well-grounded. 1 = wrong or off-topic.
Return only the number."""

def judge(answer: str) -> int:
    resp = client.chat.completions.create(
        model="gpt-6",
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user", "content": answer},
        ],
    )
    return int(resp.choices[0].message.content)
```
```python
# Regression gate
def run_suite() -> float:
    scores = []
    for case in GOLDEN:
        out = run_case(PROMPT, case["input"])
        scores.append(1.0 if exact_match(out, case["expected"]) else 0.0)
    return sum(scores) / len(scores)

def test_no_regression():
    assert run_suite() >= 0.9, "Eval score dropped below threshold"
```

## Step-by-Step
1. Define what "good" means: correct format, factuality, helpfulness.
2. Build a golden dataset with rubrics or expected answers.
3. Choose metrics: exact-match, similarity, or LLM-as-judge.
4. Implement the scoring harness and aggregate results.
5. Establish a baseline score on the current prompt/model.
6. Add a regression gate in CI with a threshold.
7. Review judge quality against human labels.
8. Extend the set as you find failure modes in production.

## Validation
1. Evals run deterministically on the same inputs
2. Threshold gate blocks clear regressions
3. Judge scores correlate with human judgment
4. Golden set covers the main failure modes
5. Run time is practical for every PR

## Troubleshooting
- Judge drift: recalibrate rubric and spot-check labels.
- Flaky scores: fix nondeterminism (temperature, model, seed).
- Too many cases: prioritize high-signal inputs and trim duplicates.