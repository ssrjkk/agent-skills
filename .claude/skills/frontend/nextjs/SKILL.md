---
name: nextjs
description: "Build full-stack React applications with Next.js App Router, Server Components, API routes, middleware, and deployment. Use for production web apps."
category: frontend
tags: [nextjs, react, fullstack, app-router, ssr, web]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
author: ssrjkk
created: 2026-09-20
updated: 2026-09-28
---
# Next.js

> Full-stack React framework with App Router, SSR, and serverless deployment.

## Quick Start
```bash
npx create-next-app@latest my-app -- --typescript --tailwind --app
cd my-app
npm run dev
# http://localhost:3000
```

## When to Use
- Full-stack React apps that need SSR, SSG, or ISR
- SEO-critical pages and marketing sites
- APIs and backend logic colocated with frontend
- Applications deployed to Vercel, Netlify, or Node servers

## Best Practices

### App Router
- Use Server Components by default; add `"use client"` only for interactivity
- Fetch data in Server Components or Route Handlers
- Use `loading.tsx`, `error.tsx`, and `not-found.tsx` for each route segment
- Stream with `<Suspense>` instead of blocking whole routes

### Routing
- File-based routing in `app/` with `page.tsx`, `layout.tsx`, `route.ts`
- Dynamic segments with `[slug]`; catch-all with `[...slug]`
- `generateStaticParams` for SSG on dynamic routes

### Performance
- Optimize images with `next/image`
- Use `next/font` for self-hosted fonts
- Implement ISR with `revalidate` or `export const dynamic`
- Add metadata via `export const metadata`

## Dependencies
```bash
npx create-next-app@latest my-app -- --typescript --tailwind --app
npm i next react react-dom
npm i -D typescript @types/node @types/react @types/react-dom
```

## Examples
```tsx
// Server Component page with metadata and ISR
export const metadata = { title: "Blog", description: "Posts" };

export const revalidate = 3600; // ISR every hour

export default async function BlogPage() {
  const posts = await fetch("https://api.example.com/posts").then((r) => r.json());
  return (
    <main>
      <h1>Blog</h1>
      {posts.map((p) => <article key={p.id}>{p.title}</article>)}
    </main>
  );
}
```
```tsx
// Route Handler (API) with validation
import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const { email } = await req.json();
  if (!email || !email.includes("@")) {
    return NextResponse.json({ error: "Invalid email" }, { status: 400 });
  }
  return NextResponse.json({ ok: true }, { status: 201 });
}
```
```tsx
// Client component for interactive UI
"use client";
import { useState } from "react";

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>Count: {count}</button>;
}
```
```tsx
// Dynamic route with generateStaticParams (SSG)
export async function generateStaticParams() {
  const posts = await fetch("https://api.example.com/posts").then((r) => r.json());
  return posts.map((p) => ({ slug: p.slug }));
}

export default function PostPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  return <h1>Post: {slug}</h1>;
}
```

## Step-by-Step
1. Scaffold with `create-next-app` using the App Router and TypeScript.
2. Plan routes as folders in `app/`; add `layout.tsx` and `page.tsx` per segment.
3. Default to Server Components; add `"use client"` only for interactive parts.
4. Fetch data in Server Components or Route Handlers; cache with ISR or revalidate.
5. Add `loading.tsx`/`error.tsx` for resilience and Suspense for streaming.
6. Add middleware for auth, redirects, or i18n when needed.
7. Optimize assets with `next/image` and `next/font`.
8. Deploy to Vercel or your Node host; set environment variables in the platform.

## Validation
1. `npm run build` succeeds with no type errors
2. `npm run lint` passes (next/core-web-vitals)
3. Routes render correct metadata and status codes
4. API routes validate input and return proper status codes
5. Lighthouse scores >= 90 on key pages

## Troubleshooting
- Hydration errors: Server and Client markup must match; avoid random values in render.
- 404 on dynamic route: check the route folder name and `generateStaticParams`.
- Build-time fetch fails: mark the route dynamic or provide a fallback.