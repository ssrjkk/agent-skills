---
name: jest
description: "Write reliable JavaScript tests with Jest: unit tests, mocking, snapshots, coverage, and CI integration. Use for JS/TS testing."
category: qa
tags: [jest, qa, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: jest
author: ssrjkk
---
# Jest (Джест)

> Тестирование JavaScript и TypeScript через Jest.

## Быстрый старт
```bash
npm i -D jest @types/jest ts-jest
npx jest
```

## Когда использовать
- Юнит-тесты JS/TS кода
- Логика React/Node компонентов
- Тестирование API и утилит
- Покрытие и регрессионные сьюты

## Лучшие практики

### Структура тестов
- Имена по поведению: `test('adds numbers')`
- Arrange, act, assert на тест
- Одно поведение на тест
- Colocate или `__tests__`

### Матчеры и ассерты
- Естественные матчеры (`toBe`, `toEqual`, `toContain`)
- `expect` с описательными сообщениями
- Edge cases и ошибки
- Для объектов — `toEqual`

### Моки
- Мокайте внешние модули и сайд-эффекты
- `jest.fn()` и `jest.spyOn()`
- Сброс моков между тестами (`clearMocks`)
- Не перемокивайте свой код

### Покрытие и CI
- Пороги покрытия
- CI на каждом PR
- `--ci` и `--coverage`
- Быстрые и изолированные тесты

## Зависимости
```bash
npm i -D jest @types/jest ts-jest
# React: @testing-library/react
```

## Примеры
```ts
// Базовый тест
function add(a: number, b: number) {
  return a + b;
}

test("adds two numbers", () => {
  expect(add(2, 3)).toBe(5);
});
```
```ts
// Мок модуля
import { fetchUsers } from "./api";
jest.mock("./api");

test("renders users", async () => {
  fetchUsers.mockResolvedValue([{ id: 1, name: "Alice" }]);
  const users = await loadUsers();
  expect(users).toHaveLength(1);
});
```
```ts
// Параметризованные тесты
test.each([
  [1, 1, 2],
  [2, 3, 5],
  [-1, 1, 0],
])("adds %i + %i = %i", (a, b, expected) => {
  expect(add(a, b)).toBe(expected);
});
```
```ts
// Spy и тест ошибки
const spy = jest.spyOn(console, "error").mockImplementation(() => {});
expect(() => risky()).toThrow();
spy.mockRestore();
```

## Пошаговое руководство
1. Установите Jest и настройте под ваш стек.
2. Добавьте test-скрипт и пороги покрытия.
3. Напишите сфокусированные юнит-тесты.
4. Мокайте внешние зависимости.
5. Добавьте edge case и error тесты.
6. Прогоните с `--coverage` и просмотрите пробелы.
7. Подключите Jest в CI.
8. Держите тесты детерминированными и быстрыми.

## Валидация
1. Все тесты проходят локально и в CI
2. Покрытие соответствует порогу
3. Моки сбрасываются между тестами
4. Нет тестов на сеть или таймеры
5. Фейлы указывают на поведение

## Устранение неполадок
- Флаки: уберите общее состояние и тайминг.
- Пере-моки: мокайте границы, не внутренности.
- Медленный сьют: `--maxWorkers` и изоляция тяжёлых тестов.