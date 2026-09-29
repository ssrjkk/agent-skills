---
name: graphql
description: "Design and implement GraphQL APIs: schemas, resolvers, queries, mutations, subscriptions, and N+1 avoidance. Use for flexible client-driven APIs."
category: backend
tags: [graphql, backend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: graphql
author: ssrjkk
---
# GraphQL (ГрафКьюЭл)

> Проектирование и реализация гибких GraphQL API.

## Быстрый старт
```bash
npm init -y && npm i graphql @apollo/server
node server.js  # http://localhost:4000/graphql
```

## Когда использовать
- Клиент-ориентированная выборка из нескольких источников
- Мобильные приложения с минимальными пейлоадами
- Агрегация нескольких сервисов за одним API
- Сложные графы объектов с глубокими связями

## Лучшие практики

### Дизайн схемы
- Моделируйте домен как типизированный граф
- Ясные типы, enums и интерфейсы
- Запросы — под нужды клиентов
- Мутации небольшие и явные

### Резолверы
- Резолвите поля по требованию, не заранее
- N+1 избегайте через DataLoader
- Ошибки на поле через массив errors
- Резолверы тонкие; логика — в сервисах

### Мутации и подписки
- Мутации-действия (`createUser`)
- Возвращайте затронутый объект + client mutation ID
- Подписки для real-time событий
- Валидируйте вход до мутации

### Производительность и безопасность
- Лимиты глубины и сложности запроса
- Авторизация на уровне полей
- Кэш резолверов и persisted queries
- Мониторинг времени резолверов

## Зависимости
```bash
npm i graphql @apollo/server graphql-tools dataloader
# Python: pip install strawberry-graphql
```

## Примеры
```graphql
# schema.graphql
type User {
  id: ID!
  name: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  author: User!
}

type Query {
  user(id: ID!): User
  recentPosts(limit: Int = 10): [Post!]!
}

type Mutation {
  createPost(title: String!, authorId: ID!): Post!
}
```
```js
// Резолвер с DataLoader батчингом
import DataLoader from "dataloader";

const userLoader = new DataLoader(ids => fetchUsersByIds(ids));
const resolvers = {
  Post: {
    author: post => userLoader.load(post.authorId),
  },
};
```
```js
// Настройка Apollo Server
import { ApolloServer } from "@apollo/server";
import { startStandaloneServer } from "@apollo/server/standalone";

const server = new ApolloServer({ typeDefs, resolvers });
startStandaloneServer(server, { listen: { port: 4000 } });
```
```js
// Лимиты сложности
const { createComplexityLimitRule } = require("graphql-validation-complexity");
// depthLimit(7), complexityLimit(100) как validationRules
```

## Пошаговое руководство
1. Смоделируйте типы домена и связи.
2. Определите queries, mutations и subscriptions в схеме.
3. Напишите резолверы с DataLoader против N+1.
4. Добавьте валидацию входа и авторизацию полей.
5. Добавьте лимиты глубины/сложности.
6. Реализуйте подписки для real-time.
7. Мониторьте задержку резолверов и ошибки.
8. В проде — persisted queries.

## Валидация
1. Схема компилируется и валидна для интроспекции
2. Запросы возвращают ровно запрошенные поля
3. N+1 исключён (loader батчит)
4. Мутации валидируют и возвращают затронутые объекты
5. Лимиты глубины/сложности отклоняют злоупотребления

## Устранение неполадок
- N+1: батчите через DataLoader, а не per-field запросами.
- Утечки интроспекции: отключите в проде или ограничьте.
- Циркулярные типы: ленивые ссылки в схеме.