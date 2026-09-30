---
name: svelte
description: "Build reactive UIs with Svelte 5: runes, stores, components, and transitions. Use for efficient interactive frontends."
category: frontend
tags: [svelte, frontend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: svelte
author: ssrjkk
---
# Svelte (Свелт)

> Компиляторно-реактивные UI на Svelte.

## Быстрый старт
```bash
npm create svelte@latest my-app
cd my-app && npm install && npm run dev
```

## Когда использовать
- Очень интерактивные фронтенды
- Маленькие бандлы (компиляция, без runtime)
- Команды, которым нужна простая реактивность
- Full-stack приложения SvelteKit

## Лучшие практики

### Runes (Svelte 5)
- `$state` для реактивного состояния
- `$derived` для вычисляемых значений
- `$props` для входов компонентов
- Избегайте прямой мутации `$state` извне

### Компоненты
- Компонуйте мелкие сфокусированные компоненты
- Данные через props; события через callbacks
- Сниппеты для переиспользуемой разметки
- Сторы для общего состояния

### Сторы
- writable/readable для общего состояния
- Производные через `derived`
- Подписки минимальны; отписывайтесь
- Для локального состояния предпочитайте runes

### Производительность
- Компилятор сам убирает неиспользуемый код
- `{#key}` для пересоздания блоков
- Лениво грузите маршруты и тяжёлые компоненты
- Виртуализируйте длинные списки

## Зависимости
```bash
npm create svelte@latest my-app -- --template demo
npm i svelte
```

## Примеры
```svelte
<script lang="ts">
  let count = $state(0);
  const doubled = $derived(count * 2);
</script>

<button onclick={() => count++}>Count: {count}</button>
<p>Doubled: {doubled}</p>
```
```svelte
<script>
  let { title, done = false } = $props();
</script>

<h2>{title}</h2>
{#if done}<span>done</span>{/if}
```
```svelte
<script>
  import { writable } from "svelte/store";

  const cart = writable<string[]>([]);
  function add(item: string) {
    cart.update(items => [...items, item]);
  }
</script>

{#each $cart as item}<p>{item}</p>{/each}
```
```svelte
<!-- Транзишены и keyed blocks -->
<script>
  import { fade } from "svelte/transition";
  let items = $state([1, 2, 3]);
</script>

{#each items as item, i (item)}
  <p transition:fade>{item}</p>
{/each}
```

## Пошаговое руководство
1. Скаффолд через SvelteKit.
2. Настройте роутинг и глобальный layout.
3. Соберите страницы на runes и компонентах.
4. Вынесите общую логику в сторы.
5. Добавьте транзишены и анимации.
6. Грузите данные через load-функции SvelteKit.
7. Оптимизируйте ленивой загрузкой.
8. Тесты на Vitest + Testing Library.

## Валидация
1. `npm run build` проходит
2. Изменения состояния отражаются в DOM
3. Сторы корректно уведомляют подписчиков
4. Нет утечек памяти от подписок
5. Размер бандла небольшой

## Устранение неполадок
- Состояние не реактивно: используйте `$state`, не простые `let`.
- Утечки сторов: отписывайтесь в `onDestroy`.
- SSR-рассогласование: избегайте browser-only API в load.