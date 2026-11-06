---
name: ui-polish-audit
description: "Audits and refines existing UI layouts for optical alignment, baseline consistency, visual hierarchy, tabular numbers, and micro-interaction polish. Use when upgrading rough prototypes into production-grade interfaces."
category: design
tags: [ui-polish, design, frontend, css, visual-hierarchy, alignment, ux]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# Impeccable UI Polish & Optical Alignment Audit

> Hunting down visual jitter, misaligned baselines, cramped padding, and missing empty/loading states in existing UIs.

## Quick Start
```css
/* Optical polish: tabular numbers, balanced headings, and smooth border transitions */
.metric, .price, .counter { font-variant-numeric: tabular-nums; }
h1, h2, h3 { text-wrap: balance; }
p { text-wrap: pretty; max-width: 65ch; }
.card { display: flex; flex-direction: column; justify-content: space-between; }
```

```python
# Check CSS file for common anti-patterns: transition: all, missing box-sizing, or raw z-index > 1000
import re
from pathlib import Path

def audit_css_polish(css_text: str) -> list[str]:
    warnings: list[str] = []
    if re.search(r"transition\s*:\s*all\b", css_text):
        warnings.append("Avoid 'transition: all'; animate only transform, opacity, or color")
    if "box-sizing: border-box" not in css_text and "box-sizing:border-box" not in css_text:
        warnings.append("Missing global box-sizing: border-box reset")
    return warnings
```

## When to Use
- An interface works functionally but looks amateurish due to uneven card heights, jagged text wrapping, or inconsistent padding
- Numbers in tables, timers, or dashboards jitter horizontally when values update
- Sibling elements in a navbar, toolbar, or card footer fail to share a single horizontal baseline
- Eliminating layout shifts (CLS), awkward scrollbars, and abrupt state transitions before a launch

## Best Practices
- Ensure macro-whitespace (gaps between sections: 48-64px) is visibly larger than micro-whitespace (padding inside cards: 16-24px).
- Align sibling cards in CSS Grid by making each card a flex column and pushing footer actions down with margin-top: auto.
- Apply text-wrap: balance on headings so multi-line titles never leave a single orphan word on the last line.
- Never use transition: all; explicitly animate only transform, opacity, background-color, or border-color.
- Right-align numeric columns in tables with font-variant-numeric: tabular-nums while left-aligning text labels.
- Replace jarring spinner-only screens with dimensionally matched skeleton placeholders to preserve scroll position.

## Dependencies
```bash
# Run CSS polish checks and verify DOM alignment
python3 --version
```

## Examples
```css
/* Equal-height grid cards with pinned footer actions */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  align-items: stretch;
}
.card-item {
  display: flex;
  flex-direction: column;
  padding: 1.25rem;
}
.card-item-footer {
  margin-top: auto;
  padding-top: 1rem;
}
```

```css
/* Optical icon-to-text alignment inside badges and buttons */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  line-height: 1;
  padding: 0.25rem 0.625rem;
}
.badge svg {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}
```

## Step-by-Step
1. Scan every page for alignment axes: verify left edges of headings, cards, and tables share a single vertical guide.
2. Check vertical rhythm: set section padding to 48-64px, card padding to 20-24px, and internal item gaps to 8-12px.
3. Pin card footers to the bottom of equal-height grid rows using flex-direction: column and margin-top: auto.
4. Add font-variant-numeric: tabular-nums to all counters, metrics, prices, and table columns.
5. Add text-wrap: balance to headings and cap body paragraph width at 65ch.
6. Run audit_css_polish() and test hover, focus-visible, empty, and error states across dark and light modes.

## Validation
1. All cards in the same horizontal grid row share identical top and bottom borders and aligned footer buttons
2. audit_css_polish() reports zero transition: all usages and confirms box-sizing: border-box
3. Updating live numbers or filter counts produces zero horizontal jitter
4. Icons inside buttons and nav links sit centered on the cap-height axis with flex-shrink: 0

## Troubleshooting
- SVG icon squashes when button text wraps on mobile — add flex-shrink: 0 to all inline SVGs.
- 1px border shifts button size on hover — keep border: 1px solid transparent in the default state and change only border-color on hover.
- Text touches table borders — enforce minimum 10px vertical and 14px horizontal cell padding.
- Scrollbar appearance shifts centered container — set html { scrollbar-gutter: stable; }.
