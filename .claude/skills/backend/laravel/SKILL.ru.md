---
name: laravel
description: "Build PHP web applications with Laravel: routing, Eloquent ORM, Blade, migrations, validation, and deployment. Use for PHP backends."
category: backend
tags: [laravel, backend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: laravel
author: ssrjkk
---
# Laravel (Ларавел)

> Создание надёжных PHP-веб-приложений на Laravel.

## Быстрый старт
```bash
composer create-project laravel/laravel my-app
cd my-app && php artisan serve
# http://localhost:8000
```

## Когда использовать
- PHP-монолиты с чистой MVC-структурой
- CRUD-приложения с быстрой разработкой
- Команды, которым нужен полный тулинг
- Проекты с Blade-шаблонами или JSON API

## Лучшие практики

### Структура
- Следуйте структуре приложения: controllers, models, services
- Контроллеры тонкие; логика — в сервисах/actions
- Route-model binding для resourceful маршрутов
- По фичам, когда проект растёт

### Eloquent и миграции
- Миграции на каждое изменение схемы
- Eloquent relationships и eager loading
- Индексы; избегайте N+1
- Валидация через Form Requests

### Валидация и ошибки
- Валидируйте через Form Requests
- Консистентные JSON-ошибки для API
- Централизованная обработка исключений
- Корректные HTTP статус-коды

### Безопасность и производительность
- Blade escaping против XSS
- Mass assignment: whitelist fillable
- Кэш горячих запросов и вьюх
- Тяжёлые задачи — в очередь

## Зависимости
```bash
composer create-project laravel/laravel my-app
php artisan serve
```

## Примеры
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
// Миграция
Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('email')->unique();
    $table->timestamp('created_at')->nullable();
});
```
```php
// Модель со связью и fillable
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
// Валидация через Form Request
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

## Пошаговое руководство
1. Скаффолд через `composer create-project`.
2. Настройте БД и окружение.
3. Создайте миграции и Eloquent-модели.
4. Соберите маршруты и контроллеры.
5. Добавьте Form Requests для валидации.
6. Напишите Blade-шаблоны или JSON API.
7. Добавьте auth, кэш и очереди.
8. Тестируйте Pest/PHPUnit и деплойте.

## Валидация
1. `php artisan test` проходит
2. Миграции применяются чисто
3. Валидация отклоняет плохой ввод
4. Нет явных N+1 в ключевых маршрутах
5. Приложение работает в production-режиме

## Устранение неполадок
- N+1: используйте `with()` eager loading.
- Mass assignment: корректно задавайте `$fillable`.
- Медленные ответы: кэшируйте запросы и вьюхи, ставьте задачи в очередь.