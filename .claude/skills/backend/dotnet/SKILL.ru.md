---
name: dotnet
description: "Build .NET backends with ASP.NET Core: minimal APIs, EF Core, dependency injection, middleware, and testing. Use for C# services."
category: backend
tags: [dotnet, backend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: dotnet
author: ssrjkk
---
# .NET / ASP.NET Core (ДотНет)

> C#-бэкенды на ASP.NET Core.

## Быстрый старт
```bash
dotnet new webapi -n MyApi
cd MyApi && dotnet run
# https://localhost:5001
```

## Когда использовать
- C# сервисы и корпоративные бэкенды
- Команды на строго типизированных языках
- Высокопроизводительные HTTP API
- Интеграция с экосистемой .NET

## Лучшие практики

### Структура
- Минимальные API или контроллеры консистентно
- По фичам: endpoints, services, data
- DI через конструктор
- Сфокусированные обработчики/сервисы

### Данные
- EF Core с миграциями
- Сущности и DTO раздельно
- Индексы для горячих запросов
- Сквозной async/await

### Middleware и ошибки
- Порядок: auth -> endpoints -> error
- Ошибки через ProblemDetails
- Валидация DataAnnotations или FluentValidation
- Корректные статус-коды

### Тестирование
- Юнит-тесты сервисов с моками
- Интеграционные — WebApplicationFactory
- Test containers для БД
- Детерминированные тесты

## Зависимости
```bash
dotnet new webapi -n MyApi
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
```

## Примеры
```csharp
// Minimal API
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/users/{id}", async (int id, UserService svc) =>
{
    var user = await svc.GetAsync(id);
    return user is null ? Results.NotFound() : Results.Ok(user);
});

app.Run();
```
```csharp
// EF Core сущность + контекст
public class User
{
    public int Id { get; set; }
    public string Email { get; set; } = "";
}

public class AppDbContext : DbContext
{
    public DbSet<User> Users => Set<User>();
    public AppDbContext(DbContextOptions<AppDbContext> o) : base(o) { }
}
```
```csharp
// Сервис с DI
public class UserService
{
    private readonly AppDbContext _db;
    public UserService(AppDbContext db) { _db = db; }

    public async Task<User?> GetAsync(int id)
        => await _db.Users.FindAsync(id);
}
```
```csharp
// Обработка ошибок через ProblemDetails
app.UseExceptionHandler(err => err.Run(async ctx =>
{
    ctx.Response.StatusCode = 500;
    await ctx.Response.WriteAsJsonAsync(new ProblemDetails
    {
        Title = "Unexpected error",
        Status = 500,
    });
}));
```

## Пошаговое руководство
1. Скаффолд через `dotnet new webapi`.
2. Настройте EF Core и миграции.
3. Соберите сервисы с DI и async-доступом к данным.
4. Добавьте эндпоинты (Minimal API или контроллеры).
5. Добавьте валидацию и ProblemDetails-ошибки.
6. Зарегистрируйте middleware в правильном порядке.
7. Напишите юнит и интеграционные тесты.
8. Настройте деплой (appsettings, контейнер).

## Валидация
1. `dotnet build` и `dotnet test` проходят
2. Эндпоинты возвращают корректный статус и форму
3. Валидация отклоняет плохой ввод
4. Нет блокирующих async-вызовов
5. Приложение работает в production-конфиге

## Устранение неполадок
- Блокирующий async: консистентно используйте async/await.
- Ошибки DI: регистрируйте сервисы до использования.
- Медленные запросы: индексы и AsNoTracking для чтений.