---
name: ai-testing
description: "AI-powered test generation and validation"
category: engineering
tags: [testing, ai, test-generation, quality, automation]
models: [sonnet, opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# AI Testing

> Generate, validate, and maintain test suites using AI-powered test generation.

## Quick Start
```python
# AI test generation with Claude
from anthropic import Anthropic
import ast
import os

client = Anthropic()

def generate_tests(source_file: str) -> str:
    """Generate unit tests for a Python module using AI."""
    with open(source_file) as f:
        source = f.read()

    # Parse to understand structure
    tree = ast.parse(source)
    functions = [node.name for node in ast.walk(tree) 
                 if isinstance(node, ast.FunctionDef) and not node.name.startswith('_')]
    classes = [node.name for node in ast.walk(tree) 
               if isinstance(node, ast.ClassDef)]

    prompt = f"""Generate comprehensive pytest tests for this module.

Module: {os.path.basename(source_file)}
Functions: {', '.join(functions)}
Classes: {', '.join(classes)}

Requirements:
- Cover: happy path, edge cases, error handling
- Use pytest fixtures for setup
- Include property-based tests where appropriate
- Mock external dependencies (I/O, network, DB)
- Achieve > 90% code coverage

Source code:
<source>
{source}
</source>

Generate tests only:"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096
    )

    return response.content[0].text

# AI-powered test validation
def validate_test_quality(test_code: str) -> dict:
    """Evaluate test quality with AI."""
    response = client.messages.create(
        model="claude-sonnet-4-5",
        messages=[{"role": "user", "content": f"""Evaluate this test suite for:

1. Coverage: Are edge cases covered?
2. Isolation: Are tests properly isolated?
3. Maintainability: Are tests readable?
4. Completeness: What's missing?

Test code:
<test_code>
{test_code}
</test_code>

Score each category 1-10 and list gaps."""}],
        max_tokens=1000
    )
    return response.content[0].text
```

```bash
# Run AI-generated tests
pytest tests/ --cov=src --cov-report=term-missing

# Continuous test regeneration on source changes
# Add to CI: if coverage drops > 5%, regenerate tests
```

## Key Concepts
AI generates tests faster but needs validation. Combine AI generation with traditional tools (coverage, mutation testing). Review AI-generated tests for correctness — they may hallucinate APIs or miss context.

## When to Use
- Legacy codebases lacking test coverage
- Rapid prototyping where manual test writing is slow
- Generating test data and fixtures
- CI pipeline to suggest tests for new code

## Step-by-Step
1. Parse the target module: walk the AST to list public functions, classes, and their signatures.
2. Build a prompt: instruct the model to generate pytest with fixtures, edge cases, and mocked external deps.
3. Generate and save: write the AI-produced tests into `tests/` (name like `test_<module>.py`).
4. Run coverage: `pytest tests/ --cov=src --cov-report=term-missing` to see gaps.
5. Validate quality: ask the model to score coverage/isolation/maintainability and list missing cases; fix hallucinations by re-running tests.
6. Automate in CI: regenerate tests when coverage drops > 5%; add adversarial cases (property-based) for numeric/logic functions.

## Examples
```python
# Regenerate tests automatically after a source change
import subprocess, pathlib

def regenerate_for(source: str) -> None:
    tests = generate_tests(source)          # from Quick Start
    out = pathlib.Path("tests") / f"test_{pathlib.Path(source).stem}.py"
    out.write_text(tests)
    subprocess.run(["pytest", str(out), "--cov=src", "--cov-report=term-missing"], check=False)
```
```bash
# Enforce quality gate in CI
pytest tests/ --cov=src --cov-fail-under=80 --cov-report=term-missing
# Mutation testing spot-check
pip install mutmut && mutmut run --paths-to-mutate src/
```

## Best Practices
- Test model outputs with a golden set and deterministic prompts.
- Use LLM-as-judge with a rubric for subjective quality.
- Add regression gates in CI for prompt and model changes.
- Track token cost and latency alongside correctness.
- Test edge cases: empty input, adversarial, and long context.
- Keep tests deterministic (temperature 0, fixed seed).

## Troubleshooting
- Flaky scores: fix nondeterminism in sampling.
- Judge bias: calibrate the rubric with human labels.
- Slow suite: cache model calls and sample the set.
- Drift: re-run evals on schedule and alert on regressions.

## Validation
1. AI-generated tests pass when run against the source
2. Coverage meets the target threshold (> 80%)
3. No hallucinated function calls in generated tests
4. Tests are deterministic (same results on each run)
