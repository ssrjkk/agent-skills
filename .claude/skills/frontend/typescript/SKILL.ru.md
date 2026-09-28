---
name: typescript
description: "Apply TypeScript for type-safe JavaScript: type design, generics, utility types, strict mode, and integration with modern tooling. Use for any JS codebase."
category: frontend
tags: [typescript, frontend, russian]
models: [sonnet, opus]
version: "1.0"
author: ssrjkk
language: ru
original: typescript
---
# TypeScript (ТайпСкрипт)

> Type-safe JavaScript с сильной типизацией, дженериками и строгим тулингом.

## Быстрый старт
```bash
npm create vite@latest my-app -- --template vanilla-ts
cd my-app
npm i
npm run build
# tsconfig.json включает strict mode
```

## Когда использовать
- Любой JavaScript-проект, который вырастает за пару файлов
- Библиотеки и общие пакеты, где важен контракт API
- Команды, которым нужна безопасность на этапе компиляции
- Рефакторинг больших легаси JS-кодовых баз

## Лучшие практики

### Дизайн типов
- Моделируйте домен через union, discriminated union и литералы
- Выводите типы из данных, а не наоборот
- Предпочитайте `type` вместо `interface` для union и mapped types
- Экспортируйте общие типы из центрального `types.ts`

### Строгость
- Включайте `strict: true` с самого начала
- Избегайте `any`; используйте `unknown` и сужайте через type guards
- Используйте `satisfies` для проверки объектов без расширения типа
- Включайте `noUncheckedIndexedAccess` для безопасности массивов

### Дженерики
- Пишите generic-функции с разумными ограничениями
- Используйте utility types: `Pick`, `Omit`, `Partial`, `Record`, `ReturnType`
- Применяйте `infer` в conditional types для продвинутого извлечения

## Зависимости
```bash
npm i -D typescript @types/node tsx
npx tsc --init
# задайте: strict true, noUncheckedIndexedAccess true
```

## Примеры
```ts
// Discriminated union безопасно моделирует state machine
type Result<T> =
  | { status: "success"; data: T }
  | { status: "error"; message: string };

function handle(r: Result<number>): number {
  if (r.status === "success") return r.data;
  console.error(r.message);
  return 0;
}
```
```ts
// Generic функция с ограничением
function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  return items.map((item) => item[key]);
}

const names = pluck([{ name: "a", id: 1 }], "name"); // string[]
```
```ts
// satisfies сохраняет узкие типы, проверяя форму
const config = {
  port: 3000,
  host: "0.0.0.0",
} satisfies Record<string, string | number>;

config.port; // number, а не string | number
```
```ts
// Type guard сужает unknown
function isError(x: unknown): x is { message: string } {
  return typeof x === "object" && x !== null && "message" in x;
}
```

## Пошаговое руководство
1. Включите `strict: true` и `noUncheckedIndexedAccess` в `tsconfig.json`.
2. Сначала смоделируйте доменные типы (union, сущности) до написания функций.
3. Пишите функции с явными возвращаемыми типами; избегайте неявного `any`.
4. Используйте `unknown` для внешнего ввода; сужайте через guards и валидацию.
5. Предпочитайте `satisfies` для конфигов; используйте `as const` для литералов.
6. Выносите сложную логику в дженерики только при повторном использовании дважды и более.
7. Добавьте `tsc --noEmit` в CI; проверяйте на каждом PR.
8. В разработке запускайте `tsc` в watch mode для быстрой обратной связи.

## Валидация
1. `tsc --noEmit` проходит без ошибок
2. Нет `any` в новом коде (правило `@typescript-eslint/no-explicit-any`)
3. Публичные API общих модулей имеют явные типы
4. Поведение в рантайме совпадает с типами (без опасных кастов)
5. Сборка (`tsup`/`vite build`) проходит чисто

## Устранение неполадок
- "Property does not exist": тип уже, чем кажется — сузьте через guards.
- "Not assignable": несовпадение объявленной и фактической формы — чините контракт данных, а не каст.
- Странные утечки `any`: проверьте `ts-ignore` и типы сторонних библиотек.