---
name: nestjs
description: "Creates Node.js server-side applications with NestJS, modules, dependency injection, and decorators. Use for enterprise-grade Node.js APIs."
category: backend
tags: [nestjs, backend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: nestjs
---
# NestJS

> Прогрессивный Node.js фреймворк: TypeScript, декораторы и DI.

## Быстрый старт
```bash
npm i -g @nestjs/cli && nest new my-api
cd my-api && npm run start:dev
```

## Основные концепции
### Модули
```typescript
@Module({ imports: [UsersModule], controllers: [AppController], providers: [AppService] })
export class AppModule {}
```

### Контроллеры
```typescript
@Controller('users')
export class UsersController {
  @Get() findAll() { return this.usersService.findAll() }
  @Post() @Body() create(dto: CreateUserDto) { return this.usersService.create(dto) }
}
```

### Провайдеры (Сервисы)
```typescript
@Injectable()
export class UsersService {
  private users: User[] = []
  findAll() { return this.users }
  create(dto: CreateUserDto) { const user = { id: Date.now(), ...dto }; this.users.push(user); return user }
}
```

## Когда использовать
- Enterprise TypeScript API
- Микросервисы на NATS/RabbitMQ
- Гибрид GraphQL + REST
- Проекты, требующие строгой структуры

## Пошаговое руководство
1. Инициализация: `nest new project`
2. Генерация: `nest g module users`, `nest g controller users`, `nest g service users`
3. Определите сущности и DTO
4. Запуск: `npm run start:dev`

## Примеры
```typescript
// Полный модуль с DI: контроллер + провайдер + репозиторий
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

// Validation DTO с class-validator
import { IsEmail, IsString, MinLength } from 'class-validator';

export class CreateUserDto {
  @IsEmail() email!: string;
  @IsString() @MinLength(2) name!: string;
}
```
```bash
# Генерация модуля с CRUD-скаффолдом, затем запрос к endpoint
nest g resource users --no-spec
curl http://localhost:3000/users
curl -X POST http://localhost:3000/users -H "content-type: application/json" -d '{"email":"a@b.c","name":"Alice"}'
```

## Лучшие практики
- Организуйте по фичам-модулям с ясными providers и controllers.
- DTO и ValidationPipe для типизированных контрактов.
- Сервисы через конструкторный DI; контроллеры тонкие.
- Interceptors для логов, guards для auth, filters для ошибок.
- Async-обработчики и неблокирующий доступ к БД.
- e2e-тесты с supertest против полного Nest-приложения.

## Устранение неполадок
- Ошибки DI: проверьте регистрацию providers в нужном модуле.
- Валидация не срабатывает: глобально примените ValidationPipe.
- Циклические импорты: forwardRef() и разбиение модуля.
- Медленные обработчики: очередь или кэш результатов.

## Валидация
1. Сервер стартует на порту 3000
2. CRUD-эндпоинты отвечают корректно
3. Инъекция зависимостей резолвит провайдеров
