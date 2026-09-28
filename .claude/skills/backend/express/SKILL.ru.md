---
name: express
description: "Build Node.js web APIs with Express: routing, middleware, error handling, validation, and production hardening. Use for Node backends."
category: backend
tags: [express, backend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: express
author: ssrjkk
---
# Express (Экспресс)

> Создание Node.js API на Express и middleware.

## Быстрый старт
```bash
npm init -y
npm i express
node server.js  # http://localhost:3000
```

## Когда использовать
- Простые и гибкие HTTP API на Node
- Приложения с большим использованием middleware
- Прототипирование и небольшие сервисы
- Команды, знакомые с JavaScript

## Лучшие практики

### Структура
- Маршруты по ресурсам: `routes/`, `controllers/`
- `express.Router()` на ресурс
- Контроллеры тонкие; логика — в сервисах
- Конфиг отдельно от кода

### Middleware
- Для auth, логирования, CORS, parsing
- Порядок: parse → auth → routes → error
- Маленький и одноцелевой middleware
- Централизованный обработчик ошибок

### Валидация и ошибки
- Валидируйте тела запросов (zod/joi)
- Структурированные ошибки со статус-кодами
- Async error handlers (`express-async-errors`)
- 404 обрабатывайте централизованно

### Продакшн
- Конфиг через `process.env`
- За reverse proxy включите `trust proxy`
- Rate limiting и security headers (helmet)
- Процесс-менеджер (PM2) или serverless

## Зависимости
```bash
npm i express helmet cors zod
npm i -D typescript @types/express ts-node nodemon
```

## Примеры
```js
const express = require("express");
const app = express();

app.use(express.json());
app.get("/health", (req, res) => res.json({ ok: true }));

app.use((err, req, res, next) => {
  res.status(err.status || 500).json({ error: err.message });
});

app.listen(3000);
```
```js
// Router для ресурса
const { Router } = require("express");
const router = Router();

router.get("/:id", async (req, res, next) => {
  try {
    const user = await findUser(req.params.id);
    res.json(user);
  } catch (e) {
    next(e);
  }
});
```
```js
// Валидация через zod
const { z } = require("zod");

const createSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

router.post("/", (req, res, next) => {
  const parsed = createSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(422).json({ error: parsed.error.flatten() });
  }
  res.status(201).json(createUser(parsed.data));
});
```
```js
// Центральный обработчик ошибок + 404
app.use((req, res) => res.status(404).json({ error: "Not found" }));
app.use((err, req, res, next) => {
  console.error(err);
  res.status(err.status || 500).json({ error: "Internal error" });
});
```

## Пошаговое руководство
1. Инициализируйте проект и установите Express.
2. Настройте middleware: json, helmet, cors.
3. Создайте роутеры по ресурсам.
4. Добавьте схемы валидации для входов.
5. Реализуйте сервисы с бизнес-логикой.
6. Добавьте центральный обработчик ошибок и 404.
7. Обеспечьте безопасность: rate limiting и env-конфиг.
8. Добавьте тесты и деплойте за reverse proxy.

## Валидация
1. Эндпоинты возвращают корректные статус-коды и JSON
2. Валидация отклоняет плохой ввод с 422
3. Ошибки обрабатываются централизованно, без падения сервера
4. Security headers и rate limiting активны
5. Тесты проходят в CI

## Устранение неполадок
- CORS-ошибки: настройте cors с правильным origin.
- Unhandled rejection: добавьте process-level обработчики и async error middleware.
- Медленные ответы: профилируйте порядок middleware и запросы к БД.