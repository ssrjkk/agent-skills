---
name: express
description: "Build Node.js web APIs with Express: routing, middleware, error handling, validation, and production hardening. Use for Node backends."
category: backend
tags: [express, nodejs, javascript, typescript, middleware, api, backend]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-26
updated: 2026-09-28
author: ssrjkk
---
# Express

> Building Node.js APIs with Express and middleware.

## Quick Start
```bash
npm init -y
npm i express
node server.js  # http://localhost:3000
```

## When to Use
- Simple and flexible HTTP APIs in Node
- Middleware-heavy applications
- Prototyping and small services
- Teams familiar with JavaScript

## Best Practices

### Structure
- Organize routes by resource: `routes/`, `controllers/`
- Use `express.Router()` per resource
- Keep controllers thin; logic in services
- Separate config from code

### Middleware
- Use middleware for auth, logging, CORS, parsing
- Order matters: parse → auth → routes → error
- Keep middleware small and single-purpose
- Add a centralized error handler

### Validation & Errors
- Validate request bodies (zod/joi)
- Return structured errors with status codes
- Use async error handlers (`express-async-errors`)
- Handle 404 centrally

### Production
- Use `process.env` for config
- Enable `trust proxy` behind a reverse proxy
- Add rate limiting and security headers (helmet)
- Run with a process manager (PM2) or serverless

## Dependencies
```bash
npm i express helmet cors zod
npm i -D typescript @types/express ts-node nodemon
```

## Examples
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
// Router for a resource
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
// Validation with zod
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
// Central error handler + 404
app.use((req, res) => res.status(404).json({ error: "Not found" }));
app.use((err, req, res, next) => {
  console.error(err);
  res.status(err.status || 500).json({ error: "Internal error" });
});
```

## Step-by-Step
1. Initialize the project and install Express.
2. Set up middleware: json, helmet, cors.
3. Create routers per resource.
4. Add validation schemas for inputs.
5. Implement services for business logic.
6. Add a centralized error handler and 404.
7. Secure with rate limiting and env config.
8. Add tests and deploy behind a reverse proxy.

## Validation
1. Endpoints return correct status codes and JSON
2. Validation rejects bad input with 422
3. Errors are handled centrally, not crashing the server
4. Security headers and rate limiting are active
5. Tests pass in CI

## Troubleshooting
- CORS errors: configure cors with the right origin.
- Unhandled rejection: add process-level handlers and async error middleware.
- Slow responses: profile middleware order and DB queries.