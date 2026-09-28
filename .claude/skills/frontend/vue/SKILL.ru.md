---
name: vue
description: "Build reactive user interfaces with Vue 3: Composition API, reactivity, components, state, and tooling. Use for any Vue-based UI work."
category: frontend
tags: [vue, frontend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: vue
author: ssrjkk
---
# Vue (Вью)

> Создание реактивных пользовательских интерфейсов на Vue 3 и Composition API.

## Быстрый старт
```bash
npm create vue@latest my-app
cd my-app
npm install
npm run dev
```

## Когда использовать
- Прогрессивное улучшение существующих страниц
- SPA из single-file компонентов
- Команды, которым нужна плавная кривая обучения
- Переиспользуемые библиотеки компонентов

## Лучшие практики

### Composition API
- Используйте `<script setup>` для лаконичных компонентов
- Выносите логику в переиспользуемые composables
- Держите реактивное состояние минимальным и явным
- `ref` — для примитивов, `reactive` — для объектов

### Компоненты
- Делите UI на небольшие сфокусированные компоненты
- Определяйте props с типами и дефолтами
- Emit типизированных событий вместо мутаций props
- Для гибкой композиции используйте slots

### Производительность
- Для производного состояния — `computed`
- Виртуализируйте длинные списки
- Лениво грузите маршруты и тяжёлые компоненты
- Где уместно — `v-memo` и `shallowRef`

### Состояние
- Сначала локальное состояние (`ref`/`reactive`)
- Для общего состояния приложения — Pinia
- Держите сторы сфокусированными и типизированными
- Не переусложняйте глобальное состояние

## Зависимости
```bash
npm create vue@latest my-app -- --typescript --router --pinia
npm i vue
```

## Примеры
```vue
<script setup lang="ts">
import { ref, computed } from "vue";

const count = ref(0);
const doubled = computed(() => count.value * 2);

function increment() {
  count.value += 1;
}
</script>

<template>
  <button @click="increment">Count: {{ count }}</button>
  <p>Doubled: {{ doubled }}</p>
</template>
```
```ts
// Переиспользуемый composable
import { ref } from "vue";

export function useCounter(start = 0) {
  const count = ref(start);
  const increment = () => count.value++;
  const decrement = () => count.value--;
  return { count, increment, decrement };
}
```
```vue
<script setup lang="ts">
// Props с типами и событиями
interface Props {
  title: string;
  done?: boolean;
}
const props = withDefaults(defineProps<Props>(), { done: false });
const emit = defineEmits<{ (e: "toggle", id: number): void }>();
</script>
```
```ts
// Pinia store
import { defineStore } from "pinia";
import { ref } from "vue";

export const useCartStore = defineStore("cart", () => {
  const items = ref<string[]>([]);
  const total = ref(0);
  const add = (item: string, price: number) => {
    items.value.push(item);
    total.value += price;
  };
  return { items, total, add };
});
```

## Пошаговое руководство
1. Создайте проект через `create-vue` (TypeScript, Router, Pinia).
2. Настройте глобальный layout с навигацией.
3. Соберите страницы как route-компоненты.
4. Вынесите общую логику в composables.
5. Добавьте Pinia-сторы для общего состояния.
6. Создайте переиспользуемые компоненты с типизированными props.
7. Оптимизируйте: ленивые маршруты, computed, виртуализация.
8. Пишите тесты на Vitest + Vue Test Utils.

## Валидация
1. `npm run build` проходит с проверкой типов
2. `npm run lint` чисто
3. Компоненты рендерятся и обновляются реактивно
4. Нет лишних ре-рендеров (Vue DevTools)
5. Тесты проходят для ядра логики и компонентов

## Устранение неполадок
- Потеря реактивности: разворачивайте ref в шаблонах; для объектов — `reactive`.
- "Cannot find module": проверьте path aliases и `tsconfig`.
- Нет состояния в Devtools: проверьте установку Pinia и порядок плагинов.