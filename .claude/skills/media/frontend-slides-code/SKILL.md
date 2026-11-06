---
name: frontend-slides-code
description: "Creates interactive, keyboard-navigable HTML/CSS/JS slide decks and technical presentations as code with zero external dependencies, live code blocks, SVG architecture diagrams, and PDF print export. Use for engineering talks, pitch decks, and interactive workshops."
category: media
tags: [slides, presentations, media, frontend, html, css, svg]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# Frontend Slides as Code (Interactive HTML/CSS Decks)

> Zero-dependency 16:9 browser slide decks with keyboard navigation, action headlines, live code copy, and @media print PDF export.

## Quick Start
```html
<!-- Minimal 16:9 Slide Deck Container with Keyboard Navigation -->
<main class="deck" id="deck">
  <section class="slide active" data-slide="0">
    <span class="kicker">01 / Architecture</span>
    <h1>Cilium eBPF Cuts Service Routing Latency by 38% vs iptables</h1>
    <p>Direct socket bypass eliminates per-rule linear chain traversal at 500+ Services.</p>
  </section>
</main>
```

```javascript
// Keyboard navigation (ArrowRight/Space/ArrowLeft) and URL hash sync (#slide-1)
let cur = 0;
const slides = Array.from(document.querySelectorAll('.slide'));
function go(idx) {
  cur = Math.max(0, Math.min(slides.length - 1, idx));
  slides.forEach((s, i) => s.classList.toggle('active', i === cur));
  history.replaceState(null, '', `#slide-${cur + 1}`);
}
window.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === ' ') go(cur + 1);
  if (e.key === 'ArrowLeft') go(cur - 1);
});
```

## When to Use
- Building a technical keynote, architecture review, or startup pitch deck as a single self-contained HTML file
- Embedding live interactive demos, syntax-highlighted code blocks, or animated SVG architecture diagrams directly inside slides
- Version-controlling presentation content in Git alongside code with clean diffs and zero proprietary binary lock-in
- Exporting pixel-accurate 16:9 PDF handouts directly from Chromium via @media print rules

## Best Practices
- Use the Assertion-Evidence model: every slide <h1> must be a complete declarative claim ('Karpenter Cut Compute Spend by 42%'), never a topic label ('Cost Overview').
- Cap slide density strictly: maximum 1 core visual (chart, diagram, or code block) + 3 concise bullet points per slide.
- Lock viewport aspect ratio to 16:9 (aspect-ratio: 16 / 9; max-width: 1280px) with clamp() typography so text never overflows or truncates.
- Include @media print rules (@page { size: 16in 9in; margin: 0; }) that display all slides sequentially with page-break-after: always.
- Provide a progress bar, slide counter (03 / 12), keyboard shortcuts (Arrow keys, Space, F for fullscreen), and touch swipe support.
- Ensure high contrast (>= 7:1 for slide headlines) so projections in bright conference rooms remain clear and legible.

## Dependencies
```bash
# Validate HTML slide deck structure and div balance with Python
python3 --version
```

## Examples
```css
/* 16:9 responsive slide stage and print-to-PDF support */
.slide {
  display: none;
  width: min(94vw, 1280px);
  aspect-ratio: 16 / 9;
  padding: clamp(2rem, 5vw, 4.5rem);
  flex-direction: column;
  justify-content: space-between;
}
.slide.active { display: flex; }
@media print {
  @page { size: 16in 9in; margin: 0; }
  .slide { display: flex !important; width: 100vw; height: 100vh; page-break-after: always; }
}
```

```python
# Audit an HTML slide deck for assertion headlines and balanced tags
import re

def audit_slide_deck(html: str) -> dict:
    slides = re.findall(r'<section[^>]*class="[^"]*slide[^"]*"[^>]*>(.*?)</section>', html, flags=re.S)
    h1s = [re.search(r"<h1[^>]*>(.*?)</h1>", s, flags=re.S) for s in slides]
    titles = [re.sub(r"<[^>]+>", "", m.group(1)).strip() for m in h1s if m]
    return {"slide_count": len(slides), "titles": titles, "balanced_divs": html.count("<div") == html.count("</div>")}
```

## Step-by-Step
1. Write the Action Title outline first: reading only the 8-12 slide headlines in order must tell the complete narrative.
2. Scaffold the single-file HTML deck with semantic <section class="slide"> elements and 16:9 CSS grid/flex layouts.
3. Add keyboard (ArrowLeft/ArrowRight/Space/Home/End), click, and touch navigation synced with location.hash (#slide-N).
4. Embed vector SVG diagrams, metric cards, and syntax-highlighted code snippets with one-click copy buttons.
5. Add @media print CSS rules so printing to PDF produces one crisp 16:9 page per slide.
6. Run audit_slide_deck() to verify slide count, action titles, and balanced HTML containers.

## Validation
1. audit_slide_deck() confirms balanced <div> tags and 100% of slides contain a declarative <h1> headline
2. ArrowLeft, ArrowRight, Space, Home, and End keys navigate smoothly and update the URL hash (#slide-N)
3. Zero horizontal or vertical text overflow occurs inside 16:9 slide containers at 1280x720 and 1920x1080
4. Browser Print-to-PDF (@media print) renders each slide onto its own landscape page with backgrounds intact

## Troubleshooting
- Code block overflows slide bottom — cap code snippets on slides to <= 14 lines and highlight only the 3 critical lines.
- Background colors disappear when printing to PDF — add -webkit-print-color-adjust: exact; print-color-adjust: exact; on body and .slide.
- Spacebar scrolls the page down instead of advancing properly — call e.preventDefault() inside the keydown handler for Space and Arrow keys.
- Fonts flicker on first slide transition — inline critical CSS variables and preconnect to Google Fonts in <head>.
