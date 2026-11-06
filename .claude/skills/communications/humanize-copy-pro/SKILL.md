---
name: humanize-copy-pro
description: "Rewrites stiff, robotic AI-generated text into natural, rhythmic, concrete human copywriting in English and Russian. Use for technical articles, product pages, documentation, release notes, and developer communications."
category: communications
tags: [copywriting, writing, communications, editing, bilingual, documentation, content]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# Humanize Copy Pro (Natural Technical & Product Writing)

> Replacing robotic cadence, puffery, and passive bureaucratic nouns with varied sentence rhythm and concrete specifics.

## Quick Start
```python
# Measure sentence-length variance (burstiness) to detect monotonous robotic cadence
import re
import statistics

def sentence_burstiness(text: str) -> float:
    sents = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    lengths = [len(s.split()) for s in sents if len(s.split()) > 1]
    return round(statistics.stdev(lengths), 2) if len(lengths) >= 2 else 0.0

assert sentence_burstiness("Ship the fix now. If the canary error rate stays under 0.5% for ten minutes, promote the rollout to all three availability zones.") > 5.0
```

```markdown
# Before (Robotic AI Cadence) -> After (Human Engineering Voice)
- Before: "In today's fast-paced digital landscape, organizations must leverage robust observability solutions to ensure seamless reliability."
- After: "When a deploy spikes 502 errors at 3 AM, you need one trace_id that links the nginx log to the slow Postgres lock."
```

## When to Use
- Rewriting AI-drafted blog posts, READMEs, landing pages, or release notes that sound monotonous, preachy, or generic
- Translating technical copy into Russian without clumsy calques ('в сегодняшнем быстро меняющемся мире', 'давайте погрузимся')
- Turning abstract feature lists into concrete before/after scenarios with real numbers and tool names
- Adapting tone for developer audiences who distrust marketing hype and value direct, falsifiable claims

## Best Practices
- Vary sentence length deliberately: pair a punchy 5-word declarative sentence with a detailed 22-word explanation.
- Replace abstract nouns (utilization, optimization, facilitation) with concrete active verbs (cut, pin, cache, isolate, roll back).
- Cut throat-clearing openings ('In the realm of modern software...', 'It is important to note that...') and start with the problem or outcome.
- In Russian copy, apply Ilyakhov's informational style: replace verbal nouns ('осуществление настройки') with finite verbs ('настройте').
- Anchor every claim in a specific artifact: a command flag, a latency number in milliseconds, an HTTP status code, or a file path.
- Read the final paragraph aloud; if you run out of breath or hit three 'which/that/которая' clauses in a row, split the sentence.

## Dependencies
```bash
# Run burstiness and passive-voice checks with Python
python3 --version
```

## Examples
```markdown
# Russian Calque Cleanup (Канцелярит -> Живой инженерный язык)
- Calque: "Данный инструмент обеспечивает осуществление мониторинга состояния подов в реальном времени."
- Clean: "Утилита следит за подами в реальном времени и шлет алерт, если контейнер уходит в OOMKilled."
```

```python
# Flag common Russian bureaucratic and AI-calque phrases
BAD_RU_PHRASES = (
    "в современном мире",
    "давайте погрузимся",
    "является ключевым",
    "осуществление",
    "в рамках данного",
)

def find_ru_calques(text: str) -> list[str]:
    low = text.lower()
    return [p for p in BAD_RU_PHRASES if p in low]
```

## Step-by-Step
1. Delete the first paragraph if it restates general background instead of naming the specific problem or result.
2. Run sentence_burstiness() and rewrite flat 15-word-every-sentence paragraphs to alternate short and long sentences.
3. Replace every vague adjective ('fast', 'scalable', 'seamless') with a verifiable metric ('12ms p99', '10k RPS', 'zero-downtime rollout').
4. In Russian text, run find_ru_calques() and replace nominalizations (-ение/-ание) with active verbs.
5. Replace generic hypothetical examples ('imagine a company X') with concrete engineering artifacts (a real CLI command or config diff).
6. Verify that headings use natural sentence case and state a clear takeaway.

## Validation
1. sentence_burstiness() exceeds 4.5 words standard deviation across multi-sentence paragraphs
2. find_ru_calques() returns an empty list on all Russian paragraphs
3. Zero sentences open with 'In today's...', 'It is worth noting...', or 'В современном мире...'
4. Every product or technical claim is paired with a concrete number, command, or mechanism

## Troubleshooting
- Text sounds choppy after shortening sentences — connect related thoughts with concrete causal links ('because', 'so that') instead of staccato fragments.
- Russian translation feels stiff despite correct grammar — rewrite from scratch asking 'how would a senior engineer explain this in Telegram or a PR comment?'.
- Marketing copy loses persuasion when adjectives are stripped — use specific customer/benchmark proof ('cut CI from 24m to 5m across 15 services').
- Overuse of em-dashes in every sentence — replace half of the em-dashes with colons, parentheses, or active verbs.
