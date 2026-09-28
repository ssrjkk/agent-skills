---
name: nextjs
description: "Build full-stack React applications with Next.js App Router, Server Components, API routes, middleware, and deployment. Use for production web apps."
category: frontend
tags: [nextjs, frontend, russian]
models: [sonnet, opus]
version: "1.0"
author: ssrjkk
language: ru
original: nextjs
---
# Next.js (НекстДжей-Эс)

> Full-stack React-фреймворк с App Router, SSR и бессерверным деплоем.

## Быстрый старт
```bash
npx create-next-app@latest my-app -- --typescript --tailwind --app
cd my-app
npm run dev
# http://localhost:3000
```

## Когда использовать
- Full-stack React-приложения, которым нужны SSR, SSG или ISR
- SEO-критичные страницы и маркетинговые сайты
- API и серверная логика рядом с фронтендом
- Приложения, деплоящиеся на Vercel, Netlify или Node-серверы

## Лучшие практики

### App Router
- По умолчанию Server Components; добавляйте `"use client"` только для интерактивности
- Загружайте данные в Server Components или Route Handlers
- Используйте `loading.tsx`, `error.tsx` и `not-found.tsx` для каждого сегмента маршрута
- Стримите через `<Suspense>` вместо блокировки целых маршрутов

### Маршрутизация
- Файловая маршрутизация в `app/` через `page.tsx`, `layout.tsx`, `route.ts`
- Динамические сегменты через `[slug]`; catch-all через `[...slug]`
- `generateStaticParams` для SSG на динамических маршрутах

### Производительность
- Оптимизируйте изображения через `next/image`
- Используйте `next/font` для self-hosted шрифтов
- Реализуйте ISR через `revalidate` или `export const dynamic`
- Добавляйте метаданные через `export const metadata`

## Зависимости
```bash
npx create-next-app@latest my-app -- --typescript --tailwind --app
npm i next react react-dom
npm i -D typescript @types/node @types/react @types/react-dom
```

## Примеры
```tsx
// Server Component страница с метаданными и ISR
export const metadata = { title: "Blog", description: "Posts" };

export const revalidate = 3600; // ISR каждый час

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
// Route Handler (API) с валидацией
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
// Клиентский компонент для интерактивного UI
"use client";
import { useState } from "react";

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>Count: {count}</button>;
}
```
```tsx
// Динамический маршрут с generateStaticParams (SSG)
export async function generateStaticParams() {
  const posts = await fetch("https://api.example.com/posts").then((r) => r.json());
  return posts.map((p) => ({ slug: p.slug }));
}

export default function PostPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  return <h1>Post: {slug}</h1>;
}
```

## Пошаговое руководство
1. Создайте проект через `create-next-app` с App Router и TypeScript.
2. Спланируйте маршруты как папки в `app/`; добавьте `layout.tsx` и `page.tsx` на сегмент.
3. По умолчанию Server Components; `"use client"` — только для интерактивных частей.
4. Загружайте данные в Server Components или Route Handlers; кэшируйте через ISR или revalidate.
5. Добавьте `loading.tsx`/`error.tsx` для устойчивости и Suspense для стриминга.
6. Добавьте middleware для auth, редиректов или i18n при необходимости.
7. Оптимизируйте ассеты через `next/image` и `next/font`.
8. Деплойте на Vercel или ваш Node-хост; настройте переменные окружения на платформе.

## Валидация
1. `npm run build` проходит без ошибок типов
2. `npm run lint` проходит (next/core-web-vitals)
3. Маршруты отдают корректные метаданные и статус-коды
4. API-маршруты валидируют вход и возвращают корректные статус-коды
5. Lighthouse >= 90 на ключевых страницах

## Устранение неполадок
- Ошибки гидрации: разметка Server и Client должна совпадать; избегайте случайных значений в рендере.
- 404 на динамическом маршруте: проверьте имя папки маршрута и `generateStaticParams`.
- Сбой fetch на этапе сборки: пометьте маршрут динамическим или дайте fallback.