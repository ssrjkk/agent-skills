---
name: prisma-orm
description: "Models databases and writes type-safe queries with Prisma ORM. Use for modern Node.js/TypeScript database access."
category: database
tags: [prisma, orm, database, typescript, postgresql]
models: [sonnet, opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# Prisma ORM

> Type-safe database access with auto-generated queries.

## Quick Start
```prisma
// schema.prisma
model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  name  String?
  posts Post[]
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
}
```

```typescript
import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

// Type-safe query
const user = await prisma.user.create({
  data: {
    email: 'alice@example.com',
    posts: { create: { title: 'Hello Prisma' } }
  },
  include: { posts: true }
});
```

## When to Use
- Type-safe database access
- Rapid schema evolution with migrations
- Not for complex raw SQL queries

## Best Practices
- Define the schema as the single source of truth; generate the client.
- Use migrations for every schema change, committed with the code.
- Select only needed fields (`select`) to avoid over-fetching.
- Use `include`/`relationLoadStrategy` deliberately to prevent N+1.
- Batch writes with `createMany`/`updateMany`.
- Use transactions for multi-step consistency.

## Step-by-Step Instructions
1. Install: `npm install prisma @prisma/client`
2. Init: `npx prisma init`
3. Define models in `schema.prisma`
4. Migrate: `npx prisma migrate dev`
5. Generate client and query with types

## Dependencies
```bash
npm install prisma @prisma/client
npx prisma init
```

## Examples
Input: `prisma.user.findMany({ where: { email: { contains: "@" } } })` → Output: All users with @ in email

```typescript
// Paginated, type-safe query with relations
const page = await prisma.user.findMany({
  where: { role: "member" },
  select: { id: true, email: true, posts: { select: { title: true } } },
  orderBy: { id: "desc" },
  take: 20,
  skip: 40,
});
```
```typescript
// Transaction for consistency
await prisma.$transaction([
  prisma.order.create({ data: { userId, amount } }),
  prisma.user.update({ where: { id: userId }, data: { balance: { decrement: amount } } }),
]);
```

## Resources
- [Prisma Docs](https://www.prisma.io/docs)
- [Examples](./examples/)

## Troubleshooting
- **`PrismaClientInitializationError`** — the schema is out of sync.
  Re-run `npx prisma generate` and check the `DATABASE_URL` is reachable.
- **Introspection overwrites custom types** — treat `prisma db pull` as
  an initial scaffold; re-apply manual types and relations afterwards.
- **Relation queries are slow** — missing index. Add `@@index` on foreign
  keys and use the Prisma Data Platform for query analysis.
- **Migrations drift on team branches** — run `prisma migrate dev` early
  and often; rebase migrations instead of resetting the database.

## Validation
1. Schema validates: `npx prisma validate`
2. Migration applies successfully
3. Generated client is type-safe
