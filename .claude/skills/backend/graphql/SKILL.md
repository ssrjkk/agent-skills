---
name: graphql
description: "Design and implement GraphQL APIs: schemas, resolvers, queries, mutations, subscriptions, and N+1 avoidance. Use for flexible client-driven APIs."
category: backend
tags: [graphql, api, schema, resolvers, mutations, subscriptions, dataloader]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# GraphQL

> Designing and implementing flexible GraphQL APIs.

## Quick Start
```bash
npm init -y && npm i graphql @apollo/server
node server.js  # http://localhost:4000/graphql
```

## When to Use
- Client-driven data fetching over multiple sources
- Mobile apps needing minimal payloads
- Aggregating several services behind one API
- Complex object graphs with deep relations

## Best Practices

### Schema Design
- Model the domain as a typed graph
- Use clear types, enums, and interfaces
- Design queries around client needs
- Keep mutations small and explicit

### Resolvers
- Resolve fields on demand, not eagerly
- Avoid N+1 with DataLoader batching
- Return errors per field via the errors array
- Keep resolvers thin; delegate to services

### Mutations & Subscriptions
- Name mutations as actions (`createUser`)
- Return the affected object plus a client mutation ID
- Use subscriptions for real-time events
- Validate inputs before mutating

### Performance & Security
- Set query depth and complexity limits
- Add field-level authorization
- Cache resolvers and use persisted queries
- Monitor resolver timing

## Dependencies
```bash
npm i graphql @apollo/server graphql-tools dataloader
# Python: pip install strawberry-graphql
```

## Examples
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
// Resolver with DataLoader batching
import DataLoader from "dataloader";

const userLoader = new DataLoader(ids => fetchUsersByIds(ids));
const resolvers = {
  Post: {
    author: post => userLoader.load(post.authorId),
  },
};
```
```js
// Apollo Server setup
import { ApolloServer } from "@apollo/server";
import { startStandaloneServer } from "@apollo/server/standalone";

const server = new ApolloServer({ typeDefs, resolvers });
startStandaloneServer(server, { listen: { port: 4000 } });
```
```js
// Complexity limits
const { createComplexityLimitRule } = require("graphql-validation-complexity");
// depthLimit(7), complexityLimit(100) as validationRules
```

## Step-by-Step
1. Model the domain types and relationships.
2. Define queries, mutations, and subscriptions in the schema.
3. Write resolvers with DataLoader to avoid N+1.
4. Add input validation and field authorization.
5. Add depth/complexity limits.
6. Implement subscriptions for real-time data.
7. Monitor resolver latency and errors.
8. Use persisted queries for production.

## Validation
1. Schema compiles and is introspection-valid
2. Queries return exactly the requested fields
3. N+1 avoided (loader batches requests)
4. Mutations validate and return affected objects
5. Depth/complexity limits reject abusive queries

## Troubleshooting
- N+1: batch with DataLoader, not per-field queries.
- Introspection leaks: disable in production or restrict.
- Circular types: use lazy references in the schema.