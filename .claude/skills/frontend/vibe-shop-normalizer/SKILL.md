---
name: vibe-shop-normalizer
description: "Normalizes messy vibe-coded e-commerce HTML/CSS/JS storefronts into clean, light-themed, responsive Zero-CLS production sites with verified catalog imagery and passing DOM tests. Use when cleaning up multi-iteration storefront code and fixing layout shifts."
category: frontend
tags: [frontend, ecommerce, css, responsive, performance, testing, tailwind]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# Vibe-Coded Storefront & Zero-CLS Normalizer

> Turning tangled multi-pass HTML/CSS/JS shop files into crisp, light-themed, Zero-CLS storefronts that pass every test.

## Quick Start
```bash
# Synchronize storefront HTML/assets and execute the full Node.js test suite
npm run vibe:clean
node --test
```

```css
/* Strict Zero-CLS light storefront geometry */
html { scrollbar-gutter: stable; overflow-x: hidden; }
body { background-color: #F4F5F7; color: #141619; overflow-x: hidden; }
.watch-stage { aspect-ratio: 1 / 1; background: #F8FAFC; }
.card-title { min-height: 38px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
```

## When to Use
- A single-file or static HTML/CSS/JS storefront has accumulated duplicate navbars, conflicting dark/light overrides, or leaked ${...} literals
- Product cards jump or shift horizontally/vertically across mobile (320px), tablet (768px), and desktop (1024px+) viewports
- Converting an inconsistent dark/neon draft into a clean commercial light theme (#F4F5F7 canvas, #FFFFFF surfaces, #141619 primary actions)
- Synchronizing static storefront files (index.html, public/index.html) while keeping 100% of existing DOM unit tests green

## Best Practices
- Audit existing unit tests (tests/*.test.js) before touching markup so required IDs, hash routes (#/catalog, #/p/:id), and price classes stay intact.
- Strip leaked JavaScript template expressions (${...}) outside <script> tags and remove duplicate <nav> or modal containers.
- Lock card aspect ratios (aspect-ratio: 1 / 1), title heights (min-height: 38px), spec heights (min-height: 32px), and button heights (h-10).
- Use font-variant-numeric: tabular-nums on all price, discount, and cart badge counters so digit updates never shift layout.
- Always call .unref() on recurring setInterval timers in storefront scripts so Node.js test runners exit cleanly without hanging.
- Keep index.html and public/index.html synchronized via a deterministic build script (vibe-clean.js).

## Dependencies
```bash
# Run Node.js built-in test runner and storefront normalizer
node --version
node --test
```

## Examples
```python
# Scan static HTML outside <script> blocks for leaked JS template literals (${...}) and duplicate IDs
import re
from collections import Counter

def audit_storefront_dom(html: str) -> dict:
    no_scripts = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S | re.I)
    leaked_tpl = re.findall(r"\$\{[^}]+\}", no_scripts)
    ids = re.findall(r'\bid=["\']([^"\']+)["\']', no_scripts)
    dupe_ids = [k for k, v in Counter(ids).items() if v > 1]
    return {"leaked_templates": leaked_tpl, "duplicate_ids": dupe_ids}
```

```javascript
// Safe background stock ticker that never hangs Node.js test runners
const ticker = setInterval(() => {
  updateLiveOrderToast();
}, 15000);
if (typeof ticker.unref === 'function') {
  ticker.unref();
}
```

## Step-by-Step
1. Read all test files in tests/ and record every asserted DOM selector, meta tag, route pattern, and global helper function.
2. Run audit_storefront_dom() to locate leaked ${...} strings, duplicate element IDs, and redundant <nav> blocks.
3. Remove destructive !important dark-mode overrides on .bg-white, .bg-gray-50, and .text-gray-900.
4. Apply the normalized light palette (#F4F5F7 background, #FFFFFF cards/modals, #141619 primary CTA, #0E9F6E accent, #2AABEE Telegram).
5. Enforce Zero-CLS card rules: aspect-ratio: 1 / 1 photo stage, explicit width/height on <img>, 2-line clamped titles, and tabular-nums prices.
6. Sync index.html to public/index.html and update byte/Brotli metrics in README.md if required by repository tests.
7. Execute node --test and verify zero layout shifts across 320px, 768px, and 1280px viewports.

## Validation
1. audit_storefront_dom() returns zero leaked ${...} literals and zero duplicate IDs in static HTML
2. node --test passes 100% of unit, DOM contract, and SEO assertions without hanging
3. document.documentElement.scrollWidth <= document.documentElement.clientWidth holds at 320px, 768px, and 1280px
4. Toggling filter pills, favorites, or cart state causes zero pixel shift in adjacent product cards

## Troubleshooting
- node --test passes all assertions but never exits — a setInterval timer was started without calling timer.unref().
- README byte-size test fails after editing index.html — run the project sync script (vibe-clean.js) to update recorded raw/Brotli byte counts.
- Product cards have uneven heights in the grid — apply min-height: 38px on the 2-line title and min-height: 32px on the subtitle.
- Page jumps horizontally when opening a modal — add html { scrollbar-gutter: stable; } so hiding the scrollbar does not shift the viewport.
