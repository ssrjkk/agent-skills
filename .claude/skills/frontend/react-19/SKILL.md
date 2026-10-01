---
name: react-19
description: "Build modern user interfaces with React 19, including Server Components, Actions, hooks, and the new compiler. Use for any interactive UI work."
category: frontend
tags: [react, ui, javascript, typescript, frontend, components]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
author: ssrjkk
created: 2026-09-20
updated: 2026-09-28
---
# React 19

> Building fast, interactive user interfaces with React 19.

## Quick Start
```bash
npx create-react-app@latest my-app
# or with a build tool you control:
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev
```

## When to Use
- Any interactive web UI, from small widgets to full applications
- Teams already invested in the React ecosystem
- Projects needing rich client-side state and rendering
- Server Components when you want to reduce client JS

## Best Practices

### Component Design
- Split UI into small, focused components with clear props
- Keep components pure: derive state instead of mutating during render
- Use composition over prop drilling
- Prefer `useMemo`/`useCallback` only when profiling shows a need

### Server Components (App Router)
- Default to Server Components; add `"use client"` only where needed
- Keep data fetching in Server Components
- Pass serializable props across the boundary
- Move event handlers and interactive state into Client Components

### State Management
- Prefer local state and derived values first
- Add a store (Zustand/Redux) only when state is genuinely shared
- Colocate state with the components that use it

## Dependencies
```bash
npm create vite@latest app -- --template react-ts
cd app
npm i react@19 react-dom@19
npm i -D typescript @types/react @types/react-dom
```

## Examples
```tsx
// A Server Component that fetches and renders
export default async function PostsPage() {
  const posts = await getPosts();
  return (
    <main>
      <h1>Posts</h1>
      {posts.map((p) => <PostCard key={p.id} post={p} />)}
    </main>
  );
}
```
```tsx
// A Client Component with Actions and optimistic updates
"use client";
import { useActionState, useOptimistic } from "react";

async function addTodo(prev: string[], formData: FormData) {
  const title = String(formData.get("title"));
  return [...prev, title];
}

export function TodoList() {
  const [items, setItems] = useActionState(addTodo, []);
  return (
    <form action={addTodo}>
      <input name="title" />
      <button>Add</button>
      <ul>{items.map((t) => <li key={t}>{t}</li>)}</ul>
    </form>
  );
}
```
```tsx
// Custom hook pattern with cleanup
import { useEffect, useState } from "react";

export function useWindowSize() {
  const [size, setSize] = useState({ w: window.innerWidth, h: window.innerHeight });
  useEffect(() => {
    const onResize = () => setSize({ w: window.innerWidth, h: window.innerHeight });
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);
  return size;
}
```
```tsx
// Suspense with lazy loading
import { lazy, Suspense } from "react";
const Chart = lazy(() => import("./Chart"));

export default function Dashboard() {
  return (
    <Suspense fallback={<div>Loading chart...</div>}>
      <Chart />
    </Suspense>
  );
}
```

## Step-by-Step
1. Scaffold with Vite (`react-ts` template) — it is faster and more configurable than CRA.
2. Set up TypeScript strict mode and ESLint + Prettier before writing features.
3. Model the UI as a tree of small components; sketch props at each level.
4. Default to Server Components; add `"use client"` for interactive parts.
5. Use Actions for mutations (form actions, optimistic updates) instead of manual fetch chains.
6. Add Suspense boundaries around async sections; avoid blocking the whole page.
7. Profile with React DevTools; memoize only what the profiler shows as hot.
8. Write tests with Vitest + React Testing Library, preferring user-centric queries.

## Validation
1. App builds with `npm run build` and passes `tsc --noEmit`
2. All interactive elements reachable by keyboard
3. No layout shift after async data loads
4. React DevTools shows no unnecessary re-renders
5. Lighthouse performance score >= 90 for key routes

## Troubleshooting
- "Too many re-renders": setState called during render — move it into an event or effect.
- Hydration mismatch: ensure Server and Client render identical markup; avoid `Date.now()` in render.
- State reset unexpectedly: key props determine identity — keep keys stable.