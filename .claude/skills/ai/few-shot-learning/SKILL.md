---
name: few-shot-learning
description: "Designs and curates few-shot examples to guide LLM behavior, including example selection, formatting, and ordering. Use for task specification without fine-tuning."
category: ai
tags: [prompt, few-shot, examples, in-context-learning, llm]
models: [sonnet, opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# Few-Shot Learning

> Guiding LLM behavior through carefully curated examples.

## Quick Start
```
Classify the sentiment of each review:

Review: "This product is amazing!"
Sentiment: Positive

Review: "Terrible experience, would not recommend."
Sentiment: Negative

Review: "It's okay, nothing special."
Sentiment: Neutral

Review: "Best purchase I've made all year!"
Sentiment:
```

## When to Use
- Teaching new tasks without fine-tuning
- Specifying output format by example
- Handling edge cases
- Setting response tone and style

## Best Practices

### Example Selection
- Cover edge cases and boundary conditions
- Include 3-5 diverse examples
- Show both positive and negative cases
- Order from simple to complex

### Formatting
- Use consistent separator between examples
- Clearly mark input vs output boundaries
- Keep format identical to expected real use

### Dynamic Selection
- For large datasets: retrieve most similar examples
- Use embedding similarity for example selection
- Limit to context window constraints

## Dependencies
```bash
pip install openai
# For dynamic selection: pip install sentence-transformers
```

## Examples
```
Translate English to French:

English: "Hello"
French: "Bonjour"

English: "Good morning"
French: "Bonjour"

English: "Thank you"
French: "Merci"

English: "How are you?"
French:
```

## Resources
- [OpenAI Few-Shot Guide](https://platform.openai.com/docs/guides/prompt-engineering)

## Step-by-Step
1. Decompose the task: identify input/output shape and the boundary cases that must be taught.
2. Curate 3-5 examples: pick diverse pairs, ordering simple to complex, including edge cases and counterexamples.
3. Format consistently: use an identical separator between examples and mark input vs output boundaries explicitly.
4. Size to the context: keep examples compact; for larger corpora, retrieve the top-k similar examples via embeddings.
5. Prompt the model with the examples inline (few-shot) or in a system message; keep the target format in the final turn.
6. Evaluate: run on a held-out set, compare formats, then iterate — adding failing cases to the example pool.

```python
# Dynamic few-shot selection using embedding similarity
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def select_examples(query: str, pool: list[tuple[str, str]], k: int = 3) -> list[tuple[str, str]]:
    # pool: list of (prompt_example, answer_example) with prompts embedded offline
    emb_q = model.encode(query)
    emb_pool = model.encode([p for p, _ in pool])
    idx = np.argsort([np.dot(emb_q, e) for e in emb_pool])[-k:][::-1]
    return [pool[i] for i in idx]
```
```txt
# Consistent formatting with clear markers
## Example 1
Input: "The movie was brilliant and moving."
Output: Positive

## Example 2
Input: "Waste of money, don't buy."
Output: Negative

## Example 3 (edge case)
Input: "Not bad at all."
Output: Positive
```

## Validation
1. Model follows example patterns consistently
2. Edge cases handled correctly
3. Adding more examples improves accuracy
4. Format matches examples exactly
