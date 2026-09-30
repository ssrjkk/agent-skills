---
name: astro
description: "Build content-focused websites with Astro: islands architecture, content collections, static generation, and integrations. Use for fast content sites."
category: frontend
tags: [astro, frontend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: astro
author: ssrjkk
---
# Astro (АстроДжейЭс)

> Быстрые контентные сайты на Astro.

## Быстрый старт
```bash
npm create astro@latest
cd my-site && npm run dev
```

## Когда использовать
- Блоги, доки, маркетинговые сайты
- Контентные статические сайты
- Сайты с минимумом JS
- Острова (islands) для интерактива

## Лучшие практики

### Islands архитектура
- Ноль JS по умолчанию
- Интерактив через `client:load`, `client:visible`
- Острова маленькие и изолированные
- Framework-острова только где нужно

### Content collections
- `src/content` с схемами
- Zod-схемы для frontmatter
- Запросы через `getCollection`
- Валидация контента в CI

### Маршрутизация и рендер
- Статическая генерация (`output: 'static'`)
- `getStaticPaths` для динамических маршрутов
- SSR только для динамики
- Оптимизация изображений через `astro:assets`

### Производительность
- Размеры и форматы изображений
- `preload` для критичных ассетов
- Без layout shift
- JS-бюджет на страницу

## Зависимости
```bash
npm create astro@latest -- --template blog
npm i astro
```

## Примеры
```astro
---
// Frontmatter страницы
import Layout from "../layouts/Base.astro";
export const title = "Home";
---
<Layout>
  <h1>Welcome</h1>
</Layout>
```
```astro
---
// Запрос content collection
import { getCollection } from "astro:content";
const posts = await getCollection("blog");
---
<ul>
  {posts.map(p => <li><a href={`/blog/${p.slug}`}>{p.data.title}</a></li>)}
</ul>
```
```astro
<!-- Интерактивный остров -->
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

## Пошаговое руководство
1. Скаффолд через `create astro`.
2. Настройте content collections со схемами.
3. Соберите страницы и layout.
4. Добавьте острова для интерактива.
5. Статические пути для динамического контента.
6. Оптимизируйте изображения и ассеты.
7. Добавьте SEO-мету и RSS.
8. Деплой на статический хост.

## Валидация
1. `npm run build` даёт статический вывод
2. Страницы отдают минимум JS
3. Content collections валидны
4. Изображения оптимизированы
5. Lighthouse высокий

## Устранение неполадок
- Слишком много JS: конвертируйте компоненты в острова или статику.
- Ошибки коллекций: исправьте zod-схему.
- Медленные сборки: кэшируйте и распараллеливайте.