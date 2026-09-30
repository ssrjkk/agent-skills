---
name: spring-boot
description: "Build production Java/Kotlin backends with Spring Boot: REST controllers, dependency injection, data access, security, and testing. Use for JVM services."
category: backend
tags: [spring-boot, backend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: spring-boot
author: ssrjkk
---
# Spring Boot (Спринг Бут)

> Продакшн-бэкенды на JVM с Spring Boot.

## Быстрый старт
```bash
# start.spring.io -> Spring Web, Data JPA, Validation
./mvnw spring-boot:run
# http://localhost:8080
```

## Когда использовать
- Корпоративные Java/Kotlin сервисы
- Команды, масштабно использующие dependency injection
- CRUD + бизнес-логика бэкенды
- Батчи, messaging и data-heavy приложения

## Лучшие практики

### Структура
- По фичам: controller, service, repository
- Контроллеры тонкие; логика — в сервисах
- Конструкторная инъекция вместо field
- Пакеты по фичам, а не по слоям

### Доступ к данным
- Spring Data repositories для CRUD
- Явные сущности; на границе — DTO
- Индексы и query-методы осознанно
- Транзакции на сервисах, не на контроллерах

### REST и валидация
- `@RestController` + `@Valid` на телах запросов
- Клиентам возвращайте DTO, никогда сущности
- Ошибки через `@ControllerAdvice`
- Корректные HTTP статус-коды

### Тестирование
- Юнит-тесты сервисов с моками
- Интеграционные — `@SpringBootTest` + Testcontainers
- Контроллеры — `MockMvc`
- Тесты изолированы и быстры

## Зависимости
```bash
# Maven или Gradle из start.spring.io
./mvnw spring-boot:run
```

## Примеры
```java
@RestController
@RequestMapping("/api/users")
class UserController {
    private final UserService service;

    UserController(UserService service) { this.service = service; }

    @GetMapping("/{id}")
    UserDto get(@PathVariable Long id) {
        return service.get(id);
    }
}
```
```java
@Service
@Transactional
class UserService {
    private final UserRepository repo;

    UserService(UserRepository repo) { this.repo = repo; }

    public UserDto get(Long id) {
        return repo.findById(id).map(UserDto::from)
            .orElseThrow(() -> new NotFoundException("user"));
    }
}
```
```java
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByEmail(String email);
}
```
```java
@ControllerAdvice
class ApiExceptionHandler {
    @ExceptionHandler(NotFoundException.class)
    ResponseEntity<ErrorBody> notFound(NotFoundException e) {
        return ResponseEntity.status(404).body(new ErrorBody(e.getMessage()));
    }
}
```

## Пошаговое руководство
1. Скаффолд через Spring Initializr (Web, Data JPA, Validation).
2. Смоделируйте доменные сущности и repositories.
3. Соберите сервисы с транзакционной бизнес-логикой.
4. Добавьте контроллеры, возвращающие DTO с валидацией.
5. Централизуйте обработку ошибок через @ControllerAdvice.
6. Добавьте Spring Security для authN/authZ.
7. Напишите юнит + интеграционные тесты.
8. Контейнеризуйте и настройте деплой.

## Валидация
1. `./mvnw test` проходит
2. Эндпоинты возвращают корректный статус и форму DTO
3. Валидация отклоняет плохой ввод с 400/422
4. Транзакции откатываются при фейле
5. Приложение стартует чисто в production-профиле

## Устранение неполадок
- Циклические зависимости: конструкторная инъекция и рефакторинг.
- LazyInitializationException: используйте DTO и fetch в сервисе.
- Медленные эндпоинты: индексы и query-методы вместо сканов сущностей.