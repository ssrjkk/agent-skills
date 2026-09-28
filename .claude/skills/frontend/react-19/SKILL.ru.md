---
name: react-19
description: "Build modern user interfaces with React 19, including Server Components, Actions, hooks, and the new compiler. Use for any interactive UI work."
category: frontend
tags: [react-19, frontend, russian]
models: [sonnet, opus]
version: "1.0"
author: ssrjkk
language: ru
original: react-19
---
# React 19 (Реакт 19)

> Создание быстрых интерактивных пользовательских интерфейсов на React 19.

## Быстрый старт
```bash
npx create-react-app@latest my-app
# или с инструментом сборки под ваш контроль:
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev
```

## Когда использовать
- Любой интерактивный веб-интерфейс — от небольших виджетов до полноценных приложений
- Команды, уже работающие в экосистеме React
- Проекты, которым нужно богатое клиентское состояние и рендеринг
- Server Components, когда нужно уменьшить объём клиентского JS

## Лучшие практики

### Дизайн компонентов
- Делите UI на небольшие сфокусированные компоненты с понятными props
- Держите компоненты чистыми: вычисляйте состояние вместо мутаций во время рендера
- Используйте композицию вместо prop drilling
- Применяйте `useMemo`/`useCallback` только если профайлер показывает необходимость

### Server Components (App Router)
- По умолчанию используйте Server Components; добавляйте `"use client"` только там, где нужно
- Держите загрузку данных в Server Components
- Передавайте сериализуемые props через границу
- Обработчики событий и интерактивное состояние — в Client Components

### Управление состоянием
- Сначала локальное состояние и производные значения
- Стор (Zustand/Redux) — только когда состояние действительно общее
- Размещайте состояние рядом с компонентами, которые его используют

## Зависимости
```bash
npm create vite@latest app -- --template react-ts
cd app
npm i react@19 react-dom@19
npm i -D typescript @types/react @types/react-dom
```

## Примеры
```tsx
// Server Component, который загружает и рендерит данные
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
// Client Component с Actions и оптимистичными обновлениями
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
// Паттерн кастомного хука с очисткой
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
// Suspense с ленивой загрузкой
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

## Пошаговое руководство
1. Создайте проект через Vite (шаблон `react-ts`) — он быстрее и гибче, чем CRA.
2. Настройте TypeScript strict mode и ESLint + Prettier до написания фич.
3. Смоделируйте UI как дерево небольших компонентов; наметьте props на каждом уровне.
4. По умолчанию Server Components; `"use client"` — только для интерактивных частей.
5. Используйте Actions для мутаций (form actions, оптимистичные обновления) вместо цепочек fetch.
6. Добавьте Suspense-границы вокруг асинхронных секций; не блокируйте всю страницу.
7. Профилируйте React DevTools; мемоизируйте только то, что профайлер показывает горячим.
8. Пишите тесты на Vitest + React Testing Library, предпочитая user-centric запросы.

## Валидация
1. Приложение собирается: `npm run build` и проходит `tsc --noEmit`
2. Все интерактивные элементы доступны с клавиатуры
3. Нет layout shift после асинхронной загрузки данных
4. React DevTools не показывает лишних ре-рендеров
5. Lighthouse производительность >= 90 для ключевых маршрутов

## Устранение неполадок
- "Too many re-renders": setState вызывается во время рендера — перенесите в событие или эффект.
- Hydration mismatch: Server и Client должны рендерить одинаковую разметку; избегайте `Date.now()` в рендере.
- Состояние неожиданно сбрасывается: ключи props определяют идентичность — держите keys стабильными.