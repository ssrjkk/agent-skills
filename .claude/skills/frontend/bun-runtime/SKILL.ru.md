---
name: bun-runtime
description: "Bun runtime for JavaScript/TypeScript"
category: frontend
tags: [bun-runtime, frontend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: bun-runtime
---
# Bun Runtime

> Создавайте и запускайте JavaScript/TypeScript-приложения на Bun — универсальном тулките.

## Быстрый старт
```bash
# Установка Bun
powershell -c "irm bun.sh/install.ps1 | iex"

# Новый проект
bun init

# Запуск TypeScript напрямую (ts-node не нужен)
bun run server.ts

# Пакетные скрипты (в 3-5 раз быстрее npm)
bun install
bun add express
bun add -d typescript

# Скрипты из package.json
bun run dev
bun run build

# Тест-раннер (совместим с Jest)
bun test

# Встроенный бандлер
bun build ./src/index.ts --outdir=./dist
```

```typescript
// Встроенные возможности Bun

// Fetch API (встроенный, полифилл не нужен)
const response = await fetch("https://api.example.com/data");
const data = await response.json();

// SQLite (встроенный)
import { Database } from "bun:sqlite";
const db = new Database(":memory:");
db.run("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)");
db.run("INSERT INTO users (name) VALUES ($name)", { name: "Alice" });
const users = db.query("SELECT * FROM users").all();

// Файловый I/O (нативный Bun)
const file = Bun.file("data.json");
const contents = await file.json();

// Переменные окружения (встроенные)
const apiKey = Bun.env.API_KEY;

// WebSocket-сервер
Bun.serve({
  port: 3000,
  fetch(req, server) {
    if (server.upgrade(req)) return; // апгрейд до WebSocket
    return new Response("Hello");
  },
  websocket: {
    message(ws, message) {
      ws.send(`Echo: ${message}`);
    }
  }
});
```

## Ключевые концепции
Bun — это runtime, бандлер, тест-раннер и пакетный менеджер в одном. Использует JavaScriptCore (не V8), стартует быстрее Node.js и полностью совместим с Node.js API.

## Когда использовать
- Новые TypeScript/JavaScript проекты
- CI/CD пайплайны со скоростной установкой и сборкой
- Dev-серверы с hot reload
- Проекты, которым нужны встроенные SQLite, fetch и WebSocket

## Пошаговое руководство
1. Установите: однострочный инсталлятор (`irm bun.sh/install.ps1 | iex` на Windows) и проверьте `bun --version`.
2. Скаффолд: `bun init` создаёт `package.json`, `tsconfig.json` и entry `index.ts`.
3. Пишите код нативно: встроенные `fetch`, `Bun.file`, `bun:sqlite` и `Bun.serve` — без полифиллов и фреймворков.
4. Быстрое управление зависимостями: `bun install`; точные версии через `bun add <pkg>@<version>`.
5. Запуск и тесты: `bun run dev` (watch mode), `bun test` (Jest-совместимый API), отладка через `bun --inspect`.
6. Сборка и релиз: `bun build ./src/index.ts --outdir=./dist --minify --target=bun` для деплой-артефакта.

## Примеры
```typescript
// REST API со встроенным SQLite и типизированными маршрутами
import { Database } from "bun:sqlite";

const db = new Database(":memory:");
db.run("CREATE TABLE todos (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, done INTEGER DEFAULT 0)");

Bun.serve({
  port: 3000,
  async fetch(req: Request) {
    const url = new URL(req.url);
    if (req.method === "POST" && url.pathname === "/todos") {
      const { title } = await req.json();
      const res = db.query("INSERT INTO todos (title) VALUES (?) RETURNING *").get(title);
      return Response.json(res, { status: 201 });
    }
    if (url.pathname === "/todos") {
      return Response.json(db.query("SELECT * FROM todos").all());
    }
    return Response.json({ error: "not found" }, { status: 404 });
  },
});
```
```bash
# Запуск собранного артефакта и тесты
bun run --watch src/index.ts
bun test
bun build src/index.ts --outdir=dist --minify --target=bun && bun dist/index.js
```

## Лучшие практики
- Bun для быстрых JS/TS рантаймов, бандлинга и тестов.
- `bun install` для скорости локфайла и совместимости.
- `bun test` — встроенный тест-раннер с покрытием.
- `Bun.serve` для высокопропускного HTTP.
- Минимум зависимостей; у Bun много встроенного.
- Фиксируйте версию Bun в CI для воспроизводимости.

## Устранение неполадок
- Конфликты установки: очистите node_modules и перегенерируйте локфайл.
- Нативные биндинги: сведите версию Bun с пакетом.
- Различия рантайма: версия Bun в CI против локальной.
- Медленный cold start: `--smol` или твик флагов рантайма.

## Валидация
1. `bun --version` показывает установленную версию
2. `bun run` выполняет TypeScript без шага компиляции
3. `bun install` быстрее npm/pnpm на том же проекте
4. `bun test` прогоняет существующие Jest/Vitest наборы
