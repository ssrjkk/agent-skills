---
name: astro
description: "Build content-focused websites with Astro: islands architecture, content collections, static generation, and integrations. Use for fast content sites."
category: frontend
tags: [astro, static-site, islands, content-collections, ssg, frontend]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Astro

> Building fast content-focused websites with Astro.

## Quick Start
```bash
npm create astro@latest
cd my-site && npm run dev
```

## When to Use
- Blogs, docs, marketing sites
- Content-heavy static sites
- Sites needing minimal JS
- Islands for interactive pieces

## Best Practices

### Islands Architecture
- Ship zero JS by default
- Add interactivity with `client:load`, `client:visible`
- Keep islands small and isolated
- Use framework islands only where needed

### Content Collections
- Use `src/content` collections with schemas
- Define zod schemas for frontmatter
- Query with `getCollection`
- Validate content in CI

### Routing & Rendering
- Prefer static generation (`output: 'static'`)
- Use `getStaticPaths` for dynamic routes
- Add SSR only for dynamic needs
- Optimize images with `astro:assets`

### Performance
- Set image sizes and formats
- Use `preload` for critical assets
- Avoid layout shift
- Keep JS budget per page

## Dependencies
```bash
npm create astro@latest -- --template blog
npm i astro
```

## Examples
```astro
---
// Frontmatter for a page
import Layout from "../layouts/Base.astro";
export const title = "Home";
---
<Layout>
  <h1>Welcome</h1>
</Layout>
```
```astro
---
// Content collection query
import { getCollection } from "astro:content";
const posts = await getCollection("blog");
---
<ul>
  {posts.map(p => <li><a href={`/blog/${p.slug}`}>{p.data.title}</a></li>)}
</ul>
```
```astro
<!-- Interactive island -->
<Counter client:visible />
```
```astro
---
export async function getStaticPaths() {
  const posts = await getCollection("blog");
  return posts.map(p => ({ params: { slug: p.slug }, props: { post: p } }));
}
---
<p>{Astro.props.post.data.body}</p>
```

## Step-by-Step
1. Scaffold with `create astro`.
2. Set up content collections with schemas.
3. Build pages and layouts.
4. Add islands for interactive pieces.
5. Generate static paths for dynamic content.
6. Optimize images and assets.
7. Add SEO meta and RSS.
8. Deploy to a static host.

## Validation
1. `npm run build` produces static output
2. Pages ship minimal JS
3. Content collections validate
4. Images are optimized
5. Lighthouse scores high

## Troubleshooting
- Too much JS: convert components to islands or static.
- Collection errors: fix the zod schema.
- Slow builds: cache and parallelize.