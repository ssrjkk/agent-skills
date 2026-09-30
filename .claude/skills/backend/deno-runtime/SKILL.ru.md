---
name: deno-runtime
description: "Deno runtime and standard library"
category: backend
tags: [deno-runtime, backend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: deno-runtime
---
# Deno Runtime

> Создавайте безопасные TypeScript-first приложения на Deno и его стандартной библиотеке.

## Быстрый старт
```typescript
// Deno.serve — современный HTTP-сервер без внешних зависимостей
import { Hono } from "jsr:@hono/hono";
import { cors } from "jsr:@hono/hono/cors";
import { Database } from "jsr:@db/sqlite";

const db = new Database("app.db");
db.run(`CREATE TABLE IF NOT EXISTS todos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  completed BOOLEAN DEFAULT FALSE
)`);

const app = new Hono();

app.use("/api/*", cors());

app.get("/api/todos", (c) => {
  const todos = db.query("SELECT * FROM todos").map(([id, title, completed]) => ({
    id, title, completed: !!completed
  }));
  return c.json(todos);
});

app.post("/api/todos", async (c) => {
  const { title } = await c.req.json();
  db.run("INSERT INTO todos (title) VALUES (?)", [title]);
  return c.json({ success: true }, 201);
});

app.patch("/api/todos/:id", async (c) => {
  const id = c.req.param("id");
  const { completed } = await c.req.json();
  db.run("UPDATE todos SET completed = ? WHERE id = ?", [completed ? 1 : 0, id]);
  return c.json({ success: true });
});

app.delete("/api/todos/:id", (c) => {
  db.run("DELETE FROM todos WHERE id = ?", [c.req.param("id")]);
  return c.json({ success: true });
});

// Deno.serve встроен — внешний сервер не нужен
Deno.serve({ port: 3000 }, app.fetch);
```

```bash
# Запуск (разрешения задаются явно)
deno run --allow-net --allow-read --allow-write --allow-env server.ts

# Или просто --allow-all для разработки
deno run -A server.ts

# Форматирование
deno fmt

# Линтинг
deno lint

# Компиляция в автономный бинарник
deno compile -A -o app-server server.ts
```

## Ключевые концепции
Deno безопасен по умолчанию — нет доступа к файлам/сети/окружению без явных флагов. Использует web-standard API (fetch, Request, Response). Встроенные форматтер, линтер, раннер тестов и компилятор. Импорт из URL или JSR.

## Когда использовать
- Безопасные приложения с принципом наименьших привилегий
- TypeScript-first проекты без конфигурации
- CLI-инструменты (deno compile создаёт автономные бинарники)
- Приложения, использующие web-standard API

## Пошаговое руководство
1. Скаффолд проекта: `deno init` создаёт стандартную структуру с тестами и конфигом.
2. Выберите HTTP-фреймворк: встроенный `Deno.serve` для простоты или `Hono` из JSR для роутинга и middleware.
3. Добавьте хранение: встроенный SQLite через `jsr:@db/sqlite` (колонки напрямую мапятся на TypeScript-типы).
4. Запустите с явными правами: `deno run --allow-net --allow-read --allow-write --allow-env server.ts`.
5. Итерируйте с watcher: `deno run --watch server.ts`, затем форматируйте и линтите через `deno fmt` / `deno lint`.
6. Отдайте в продакшен: `deno compile -A -o app-server server.ts` собирает автономный бинарник.

## Лучшие практики
- Запускайте с минимальными флагами прав, которые реально нужны (`--allow-net`, если нет доступа к файлам).
- Предпочитайте web-standard API (`fetch`, `Request`, `Response`) для переносимости.
- JSR-пакеты с явными версиями в `deno.json` для воспроизводимости.
- Держите обработчики тонкими: парсите, валидируйте и делегируйте в сервисный слой.
- Используйте `Deno.serve` для серверов без зависимостей; Hono — только при нужде в роутинге/middleware.
- Валидируйте тела запросов до записи в БД.
- Форматируйте и линтите в CI (`deno fmt --check`, `deno lint`).
- `deno task` для определения и документирования общих команд.

## Устранение неполадок
- Ошибки прав: добавьте точные флаги `--allow-*` для вашего кода.
- Порт занят: смените порт или остановите конфликтующий процесс.
- Нет модуля: зафиксируйте версии в `deno.json` и перезапустите `deno install`.
- SQLite заблокирован: используйте одно соединение или оборачивайте записи в транзакции.

## Примеры
```typescript
// Полный CRUD API: сервер, роутинг, SQLite и обработка ошибок
import { Hono } from "jsr:@hono/hono";
import { cors } from "jsr:@hono/hono/cors";
import { Database } from "jsr:@db/sqlite";

const db = new Database("app.db");
db.exec(`CREATE TABLE IF NOT EXISTS todos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  completed BOOLEAN DEFAULT FALSE
)`);

const app = new Hono();
app.use("/api/*", cors());

app.get("/health", (c) => c.json({ status: "ok" }));

app.post("/api/todos", async (c) => {
  const { title } = await c.req.json<{ title: string }>();
  if (!title) return c.json({ error: "title required" }, 400);
  const info = db.query("INSERT INTO todos (title) VALUES (?) RETURNING id, title, completed", [title]);
  return c.json(info[0], 201);
});

app.patch("/api/todos/:id", async (c) => {
  const id = Number(c.req.param("id"));
  const { completed } = await c.req.json<{ completed: boolean }>();
  db.run("UPDATE todos SET completed = ? WHERE id = ?", [completed ? 1 : 0, id]);
  return c.json({ updated: true });
});

app.delete("/api/todos/:id", (c) => {
  db.run("DELETE FROM todos WHERE id = ?", [Number(c.req.param("id"))]);
  return c.json({ deleted: true });
});

Deno.serve({ port: 3000 }, app.fetch);
```

```bash
# Проверка: запуск, запросы к API, контроль строк в SQLite
deno run --allow-net --allow-read --allow-write --allow-env server.ts
curl http://localhost:3000/api/todos
curl -X POST http://localhost:3000/api/todos -H "content-type: application/json" -d '{"title":"demo"}'
```

## Валидация
1. `deno run` работает с явными флагами разрешений
2. Функции стандартной библиотеки Deno работают корректно
3. `deno compile` собирает работающий автономный бинарник
4. HTTP-сервер корректно отвечает с нужными правами
