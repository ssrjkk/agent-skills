---
name: laravel
description: "Build PHP web applications with Laravel: routing, Eloquent ORM, Blade, migrations, validation, and deployment. Use for PHP backends."
category: backend
tags: [laravel, php, eloquent, blade, migrations, artisan, backend]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Laravel

> Building robust PHP web applications with Laravel.

## Quick Start
```bash
composer create-project laravel/laravel my-app
cd my-app && php artisan serve
# http://localhost:8000
```

## When to Use
- PHP monoliths with clean MVC structure
- CRUD apps needing rapid development
- Teams wanting batteries-included tooling
- Projects with Blade templates or JSON APIs

## Best Practices

### Structure
- Follow the app structure: controllers, models, services
- Keep controllers thin; business logic in services/actions
- Use route-model binding for resourceful routes
- Organize by feature when it grows

### Eloquent & Migrations
- Define migrations for every schema change
- Use Eloquent relationships and eager loading
- Add indexes; avoid N+1 queries
- Use form requests for validation

### Validation & Errors
- Validate with Form Requests
- Return consistent JSON error shapes for APIs
- Handle exceptions centrally
- Use proper HTTP status codes

### Security & Performance
- Use Blade escaping to prevent XSS
- Mass assignment: whitelist fillable fields
- Cache hot queries and views
- Queue heavy jobs

## Dependencies
```bash
composer create-project laravel/laravel my-app
php artisan serve
```

## Examples
```php
// routes/web.php
Route::get('/users/{user}', [UserController::class, 'show']);

// app/Http/Controllers/UserController.php
class UserController extends Controller
{
    public function show(User $user)
    {
        return view('users.show', ['user' => $user]);
    }
}
```
```php
// Migration
Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('email')->unique();
    $table->timestamp('created_at')->nullable();
});
```
```php
// Model with relationship and fillable
class User extends Authenticatable
{
    protected $fillable = ['name', 'email'];
    protected $hidden = ['password'];

    public function posts()
    {
        return $this->hasMany(Post::class);
    }
}
```
```php
// Form request validation
class StoreUserRequest extends FormRequest
{
    public function rules()
    {
        return [
            'name' => 'required|string|max:255',
            'email' => 'required|email|unique:users',
        ];
    }
}
```

## Step-by-Step
1. Scaffold with `composer create-project`.
2. Configure DB and set up the environment.
3. Create migrations and Eloquent models.
4. Build routes and controllers.
5. Add Form Requests for validation.
6. Write Blade templates or JSON API responses.
7. Add auth, caching, and queues.
8. Test with Pest/PHPUnit and deploy.

## Validation
1. `php artisan test` passes
2. Migrations apply cleanly
3. Validation rejects bad input
4. No obvious N+1 in key routes
5. App runs in production mode

## Troubleshooting
- N+1: use `with()` eager loading.
- Mass assignment: set `$fillable` correctly.
- Slow responses: cache queries and views, queue jobs.