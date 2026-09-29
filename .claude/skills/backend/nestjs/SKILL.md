---
name: nestjs
description: "Creates Node.js server-side applications with NestJS, modules, dependency injection, and decorators. Use for enterprise-grade Node.js APIs."
category: backend
tags: [nestjs, nodejs, typescript, api, decorators]
models: [sonnet, opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# NestJS

> Progressive Node.js framework with TypeScript, decorators, and DI.

## Quick Start
```bash
npm i -g @nestjs/cli && nest new my-api
cd my-api && npm run start:dev
```

## Core Concepts
### Modules
```typescript
@Module({ imports: [UsersModule], controllers: [AppController], providers: [AppService] })
export class AppModule {}
```

### Controllers
```typescript
@Controller('users')
export class UsersController {
  @Get() findAll() { return this.usersService.findAll() }
  @Post() @Body() create(dto: CreateUserDto) { return this.usersService.create(dto) }
}
```

### Providers (Services)
```typescript
@Injectable()
export class UsersService {
  private users: User[] = []
  findAll() { return this.users }
  create(dto: CreateUserDto) { const user = { id: Date.now(), ...dto }; this.users.push(user); return user }
}
```

## When to Use
- Enterprise TypeScript APIs
- Microservices with NATS/RabbitMQ
- GraphQL + REST hybrid APIs
- Projects needing strong structure

## Step-by-Step
1. Init: `nest new project`
2. Generate: `nest g module users`, `nest g controller users`, `nest g service users`
3. Define entities and DTOs
4. Run: `npm run start:dev`

## Examples
```typescript
// Full module wired with DI: controller + provider + repository
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';
import { User } from './user.entity';

@Module({
  imports: [TypeOrmModule.forFeature([User])],
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}

// Validation DTO with class-validator
import { IsEmail, IsString, MinLength } from 'class-validator';

export class CreateUserDto {
  @IsEmail() email!: string;
  @IsString() @MinLength(2) name!: string;
}
```
```bash
# Generate a module with CRUD scaffold, then hit the endpoint
nest g resource users --no-spec
curl http://localhost:3000/users
curl -X POST http://localhost:3000/users -H "content-type: application/json" -d '{"email":"a@b.c","name":"Alice"}'
```

## Validation
1. Server starts on port 3000
2. CRUD endpoints respond correctly
3. Dependency injection resolves providers
