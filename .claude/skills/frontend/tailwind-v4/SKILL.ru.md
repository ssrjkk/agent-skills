---
name: tailwind-v4
description: "Tailwind CSS v4 features"
category: frontend
tags: [tailwind-v4, frontend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: tailwind-v4
---
# Tailwind CSS v4

> Используйте CSS-first конфигурацию Tailwind v4, новые утилиты и рост производительности.

## Быстрый старт
```css
/* app.css — CSS-first конфигурация Tailwind v4 */
@import "tailwindcss";

/* Нативные CSS custom properties для темы */
@theme {
  --color-brand: #6c5ce7;
  --color-brand-light: #a29bfe;
  --font-display: "Inter", sans-serif;
  --breakpoint-3xl: 120rem;
  --animate-fade-in: fade-in 0.5s ease-in-out;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* @apply с современными CSS-возможностями */
.btn-primary {
  @apply bg-brand text-white px-4 py-2 rounded-lg
         hover:bg-brand-light transition-colors
         focus-visible:outline-2 focus-visible:outline-brand;
}

/* Container queries с @cq-* */
.card-grid {
  @apply grid grid-cols-1 gap-4;
  @container (min-width: 30rem) {
    @apply grid-cols-2;
  }
  @container (min-width: 50rem) {
    @apply grid-cols-3;
  }
}
```

```html
<!-- новые фичи v4 -->
<div class="
  /* 3D трансформации */
  perspective-1000 rotate-x-45 rotate-y-30

  /* scroll-driven анимации */
  scroll-mt-20 scroll-snap-align-start

  /* новые цветовые функции */
  bg-linear-to-r from-red-500 to-blue-500

  /* field sizing */
  field-sizing-content

  /* балансировка текста */
  text-balance

  /* внутренние тени */
  shadow-inner-sm

  /* container queries */
  @max-md:flex-col @min-lg:flex-row
">
```

## Ключевые концепции
Tailwind v4 — CSS-first (без tailwind.config.js). Новые фичи: директива `@theme`, container queries, 3D-трансформации, scroll-driven анимации, поддержка CSS `@layer`, `text-balance` и `field-sizing`.

## Когда использовать
- Новые проекты на Tailwind v4
- Апгрейд с v3: меньше конфига, новые фичи
- Проекты, которым нужны container queries или 3D-трансформации

## Пошаговое руководство
1. Установите v4: `npm install tailwindcss @tailwindcss/vite` и добавьте Vite-плагин (или PostCSS-аналог).
2. Создайте CSS-вход: `@import "tailwindcss";` в главном CSS — `tailwind.config.js` не нужен.
3. Тема через `@theme`: определите дизайн-токены (цвета, шрифты, брейкпоинты, анимации) как CSS custom properties.
4. Утилиты v4: container queries (`@container`, `@min-*`/`@max-*`), 3D-трансформации, `text-balance`, `field-sizing`.
5. Компонуйте через `@apply` внутри современного CSS (`@layer`, nesting) с токенами `@theme`.
6. Сборка и проверка: dev-сервер, затем сравнение размера продакшн-CSS с v3; без миграционных warning'ов.

## Примеры
```css
/* app.css — кастомный вариант + стилизация по data-атрибуту */
@import "tailwindcss";

@theme {
  --color-brand: #6c5ce7;
  --font-display: "Inter", sans-serif;
}

@custom-variant data-active (&[data-active="true"]);

.card[data-active="true"] {
  @apply border-brand text-brand bg-brand/10;
}
```
```html
<!-- комбинация responsive + container query -->
<div class="@container">
  <div class="
    grid grid-cols-1
    @min-lg:grid-cols-3
    max-md:flex-col
    space-y-4
  ">
    <section class="text-balance shadow-inner-sm">Card A</section>
    <section class="bg-linear-to-r from-violet-500 to-fuchsia-500">Card B</section>
  </div>
</div>
```

## Лучшие практики
- Тема через CSS `@theme` токены, не конфиг-файлы.
- Utility-first классы; компоненты только при повторах.
- Адаптивные и state-варианты (`hover:`, `md:`).
- `@apply` экономно; предпочитайте утилиты в разметке.
- Кастомные утилиты через `@utility` для повторяющихся паттернов.
- Включите content-сканирование путей шаблонов.

## Устранение неполадок
- Классы не генерируются: проверьте content globs.
- Медленная сборка: сузьте пути контента.
- Проблемы переопределений: порядок вариантов или `!` для important.
- v4 vs v3 конфиг: мигрируйте `tailwind.config` в CSS `@theme`.

## Валидация
1. Custom properties из `@theme` доступны во всех утилитах
2. Container queries реагируют на правильных брейкпоинтах
3. Собранный CSS меньше эквивалентной конфигурации v3
4. При сборке нет v3 миграционных предупреждений
