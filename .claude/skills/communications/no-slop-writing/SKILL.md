---
name: no-slop-writing
description: "Eliminates AI slop, corporate buzzwords, filler transitions, and ungrounded claims from technical documents, PRDs, and agent outputs. Use as a strict quality gate for high-density engineering and product writing."
category: communications
tags: [writing, editing, quality-gate, communications, documentation, anti-slop, prd]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# No-Slop High-Density Writing Gate

> Zero filler, zero buzzword salads, and 100% claim-to-evidence grounding for engineering docs and PRDs.

## Quick Start
```python
# Ban-list scanner that flags high-entropy AI slop and corporate filler phrases
SLOP_PHRASES = (
    "delve into", "testament to", "tapestry of", "paradigm shift",
    "synergistic", "holistic approach", "unlock the full potential",
    "инновационные решения", "синергия", "комплексный подход", "вывести на новый уровень",
)

def scan_for_slop(text: str) -> list[str]:
    low = text.lower()
    return [phrase for phrase in SLOP_PHRASES if phrase in low]

assert scan_for_slop("Deploy CloudNativePG with 3 replicas across 3 AZs for RPO=0.") == []
```

```markdown
# High-Density Claim Rule: [Subject] + [Exact Action] + [Quantified Effect] + [Verification]
- Bad (Slop): "Our next-gen platform utilizes holistic caching to dramatically boost performance."
- Good (Dense): "Redis Cache-Aside with a 60s jittered TTL serves 85% of product reads in 1.8ms, reducing PostgreSQL CPU from 78% to 19%."
```

## When to Use
- Auditing technical RFCs, architecture decision records (ADRs), PRDs, or READMEs for fluff and empty corporate slogans
- Enforcing strict token efficiency and factual precision in LLM system prompts and agent outputs
- Removing repetitive meta-announcements ('In this section we will explore...', 'In conclusion, it is clear that...')
- Ensuring every technical recommendation includes trade-offs, failure modes, and verification commands

## Best Practices
- Lead every section with the answer or decision in sentence 1; never bury the conclusion at the bottom of a long preamble.
- Ban meta-roadmaps ('Below is a breakdown of...', 'Let us now turn our attention to...') — let headings do the routing.
- Require every architecture choice to state what it sacrifices (e.g., 'Synchronous replication guarantees RPO=0 at the cost of +1.5ms write latency').
- Replace bullet lists of single abstract nouns ('Scalability', 'Security', 'Reliability') with declarative assertion headers.
- Delete any sentence that remains true if you insert 'not' (e.g., 'We care about quality' -> nobody claims they hate quality).
- Keep word count tight: if a 600-word RFC can state the exact same schema, API contract, and rollback plan in 250 words, cut the 350.

## Dependencies
```bash
# Run automated slop and word-density checks
python3 --version
```

## Examples
```python
# Calculate information density ratio (numbers, code tokens, and concrete identifiers per 100 words)
import re

def info_density_per_100_words(text: str) -> float:
    words = text.split()
    if not words:
        return 0.0
    signals = re.findall(r"(`[^`]+`|\b\d+[a-zA-Z%/.:-]*\b|\b[A-Z]{2,}\b)", text)
    return round(len(signals) / len(words) * 100.0, 1)

assert info_density_per_100_words("Set `max_connections=200` on PostgreSQL 16 and route via PgBouncer on port 6432 for <2ms p99.") >= 25.0
```

```markdown
# Declarative Section Headers (Assertion-Evidence Pattern)
- Weak header: "Database Architecture"
- Strong header: "CloudNativePG 3-Node Quorum Guarantees RPO=0 and <10s Failover"
```

## Step-by-Step
1. Run scan_for_slop() across the draft and delete every flagged phrase and surrounding filler clause.
2. Strip introductory throat-clearing and closing 'In Conclusion / Key Takeaways' recaps that repeat earlier bullets verbatim.
3. Rewrite generic topic headings into declarative assertions containing the core metric or architectural decision.
4. Check info_density_per_100_words() and replace hand-wavy claims with exact configuration keys, numbers, or links.
5. Add an explicit 'Trade-offs & Failure Modes' bullet for every proposed tool or architecture.

## Validation
1. scan_for_slop() returns zero matches across the entire document
2. info_density_per_100_words() is >= 12.0 on technical specification sections
3. Zero sections begin with meta-announcements ('Below is...', 'In this section...')
4. Every architectural recommendation states both its quantified benefit and its operational cost/trade-off

## Troubleshooting
- Document feels too terse for newcomers — add a 2-sentence concrete context example at the top rather than padding every paragraph with adjectives.
- Writer struggles to find exact metrics — state the target threshold or SLA contract ('p99 < 200ms at 5,000 RPS') rather than leaving qualitative fluff.
- AI keeps re-introducing filler words — include the explicit ban-list inside the system prompt or CLAUDE.md.
- Tables repeat the exact same text as bullet lists — delete the duplicate bullet list and let the Markdown table carry the comparison.
