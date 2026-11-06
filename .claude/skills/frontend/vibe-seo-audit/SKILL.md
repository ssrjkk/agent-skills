---
name: vibe-seo-audit
description: "Audits and fixes SEO, SSR/prerendering, meta tags, Open Graph preview cards, sitemap.xml, robots.txt, PageSpeed/LCP performance, and curated GitHub/MCP/Cursor integrations for vibe-coded websites and SPAs. Use when fixing empty React/Vite root divs and search visibility."
category: frontend
tags: [seo, ssr, nextjs, astro, pagespeed, open-graph, mcp, frontend]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# Vibe-Coded Website SEO, SSR & Performance Audit

> Eliminating empty SPA root divs with SSR/prerendering, rich Open Graph cards, sitemap/robots, and PageSpeed 90+ (LCP < 2.5s).

## Quick Start
```bash
# Verify that the initial HTTP response ships semantic HTML instead of an empty <div id="root"></div>
curl -s http://localhost:3000 | grep -E "<h1|<title|og:image"
test -f public/sitemap.xml && test -f public/robots.txt && echo "SEO files present"
```

```html
<!-- Complete SEO & Open Graph head block for crawler indexing and Telegram preview cards -->
<head>
  <title>AI Coder Portal — Roadmaps, Skills & Career</title>
  <meta name="description" content="Step-by-step IT roadmaps, 120 bilingual agent skills, and hands-on DevOps/AI labs." />
  <link rel="canonical" href="https://ssrjkk.github.io/agent-skills/" />
  <meta property="og:title" content="AI Coder Portal — Roadmaps, Skills & Career" />
  <meta property="og:description" content="Step-by-step IT roadmaps and 120 bilingual agent skills." />
  <meta property="og:image" content="https://ssrjkk.github.io/agent-skills/og-preview.webp" />
  <meta property="og:type" content="website" />
  <meta name="twitter:card" content="summary_large_image" />
</head>
```

## When to Use
- A vibe-coded React or Vite SPA ships an empty <div id="root"></div> that Yandex, Google, or AI search crawlers fail to index
- Sharing a link in Telegram, Slack, or X displays a bare URL instead of a rich preview card with image and description
- PageSpeed Insights scores below 90 or Largest Contentful Paint (LCP) exceeds 2.5 seconds due to heavy PNGs and bloated JS
- Selecting curated GitHub ecosystems (build-your-own-x, public-apis, awesome-mcp-servers, awesome-cursorrules) for AI-assisted builds

## Best Practices
- Render semantic HTML (<header>, <main>, <h1>, <article>) on the server or at build time using Next.js, Astro, or an HTML prerender script.
- Keep exactly one <h1> tag per page and write unique <title> and <meta name="description"> tags aligned with real search queries.
- Always use an absolute HTTPS URL in <meta property="og:image" content="https://..."> so Telegram and social scrapers fetch the preview reliably.
- Convert multi-megabyte hero PNG/JPEG images to compressed WebP (<= 200 KB) with explicit width, height, and fetchpriority="high".
- Place valid sitemap.xml and robots.txt files in the site root and register the domain in Google Search Console and Yandex Webmaster.
- Replace generic corporate slogans with concrete user search phrases (specific services, locations, or technical queries).

## Dependencies
```bash
# Convert heavy PNG/JPG assets to WebP and run Lighthouse SEO/LCP checks
cwebp -q 82 public/hero.png -o public/hero.webp
```

## Examples
```python
# Audit an HTML file for empty SPA root, single H1, meta description, and absolute og:image
import re
from pathlib import Path

def audit_html_seo(html_text: str) -> list[str]:
    issues: list[str] = []
    if re.search(r'<div\s+id=["\']root["\']>\s*</div>', html_text):
        issues.append("Empty <div id='root'></div> detected: enable SSR or prerendering")
    h1_count = len(re.findall(r"<h1[\s>]", html_text, flags=re.I))
    if h1_count != 1:
        issues.append(f"Expected exactly 1 <h1> tag, found {h1_count}")
    if 'name="description"' not in html_text:
        issues.append("Missing <meta name='description'>")
    og_img = re.search(r'property="og:image"\s+content="([^"]+)"', html_text)
    if not og_img or not og_img.group(1).startswith("https://"):
        issues.append("og:image must be present and use an absolute https:// URL")
    return issues
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://ssrjkk.github.io/agent-skills/</loc>
    <lastmod>2026-10-28</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://ssrjkk.github.io/agent-skills/roadmaps.html</loc>
    <lastmod>2026-10-28</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>
```

## Step-by-Step
1. Inspect the raw page source (curl -s <URL>) to confirm whether crawlers receive semantic HTML or an empty <div id="root"></div>.
2. Enable SSR/SSG (Next.js App Router, Astro) or run a build-time prerender script that injects semantic HTML into index.html.
3. Add unique <title>, <meta name="description">, canonical link, and a single <h1> heading per route.
4. Add Open Graph (og:title, og:description, og:image, og:url) and Twitter Card tags with an absolute HTTPS preview image.
5. Generate sitemap.xml and robots.txt in the public root and submit them in Google Search Console and Yandex Webmaster.
6. Compress hero and catalog images to WebP, preload the LCP asset, and defer non-critical scripts until LCP is under 2.5s.
7. Integrate curated GitHub resources (build-your-own-x, public-apis, awesome-mcp-servers, awesome-cursorrules) into project workflows.

## Validation
1. curl -s <URL> returns populated <h1>, <main>, <title>, and <meta name="description"> without executing JavaScript
2. audit_html_seo() reports zero issues on index.html and all route pages
3. sitemap.xml and robots.txt return HTTP 200 and validate cleanly in Search Console / Webmaster
4. PageSpeed Insights mobile and desktop scores reach 90+ with Largest Contentful Paint (LCP) < 2.5s

## Troubleshooting
- Telegram link preview still shows old or missing image — use an absolute https:// URL in og:image and refresh via @WebpageBot.
- Yandex Webmaster reports pages excluded as low-value or empty — the SPA root div is still rendered only on the client; enable build-time prerendering.
- LCP remains > 3.0s despite WebP compression — remove loading="lazy" from the above-the-fold hero image and add fetchpriority="high".
- Duplicate title warnings in Search Console — give each dynamic route or category page its own distinct title and canonical URL.
