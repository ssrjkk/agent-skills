---
name: dotnet
description: "Build .NET backends with ASP.NET Core: minimal APIs, EF Core, dependency injection, middleware, and testing. Use for C# services."
category: backend
tags: [dotnet, csharp, aspnet-core, ef-core, minimal-api, backend]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# .NET / ASP.NET Core

> Building C# backends with ASP.NET Core.

## Quick Start
```bash
dotnet new webapi -n MyApi
cd MyApi && dotnet run
# https://localhost:5001
```

## When to Use
- C# services and enterprise backends
- Teams using strongly-typed languages
- High-performance HTTP APIs
- Integration with the .NET ecosystem

## Best Practices

### Structure
- Use Minimal APIs or controllers consistently
- Separate by feature: endpoints, services, data
- Register dependencies in DI; constructor injection
- Keep handlers/services focused

### Data Access
- Use EF Core with migrations
- Define entities and DTOs separately
- Add indexes for hot queries
- Use async/await end to end

### Middleware & Errors
- Compose middleware in order (auth -> endpoints -> error)
- Handle errors with ProblemDetails
- Validate inputs with DataAnnotations or FluentValidation
- Return correct status codes

### Testing
- Unit test services with mocks
- Integration test with WebApplicationFactory
- Use test containers for DB
- Keep tests deterministic

## Dependencies
```bash
dotnet new webapi -n MyApi
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
```

## Examples
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
// EF Core entity + context
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
// Service with DI
public class UserService
{
    private readonly AppDbContext _db;
    public UserService(AppDbContext db) { _db = db; }

    public async Task<User?> GetAsync(int id)
        => await _db.Users.FindAsync(id);
}
```
```csharp
// Error handling with ProblemDetails
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

## Step-by-Step
1. Scaffold with `dotnet new webapi`.
2. Set up EF Core and migrations.
3. Build services with DI and async data access.
4. Add endpoints (Minimal API or controllers).
5. Add validation and ProblemDetails errors.
6. Register middleware in the right order.
7. Write unit and integration tests.
8. Configure deployment (appsettings, container).

## Validation
1. `dotnet build` and `dotnet test` pass
2. Endpoints return correct status and shape
3. Validation rejects bad input
4. No async-blocking calls
5. App runs in production config

## Troubleshooting
- Blocking async: use async/await consistently.
- DI errors: register services before use.
- Slow queries: add indexes and AsNoTracking for reads.