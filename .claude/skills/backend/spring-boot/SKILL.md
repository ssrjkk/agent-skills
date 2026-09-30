---
name: spring-boot
description: "Build production Java/Kotlin backends with Spring Boot: REST controllers, dependency injection, data access, security, and testing. Use for JVM services."
category: backend
tags: [spring-boot, java, kotlin, rest, dependency-injection, jvm, backend]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Spring Boot

> Building production JVM backends with Spring Boot.

## Quick Start
```bash
# start.spring.io -> Spring Web, Data JPA, Validation
./mvnw spring-boot:run
# http://localhost:8080
```

## When to Use
- Enterprise Java/Kotlin services
- Teams using dependency injection at scale
- CRUD + business logic backends
- Batch, messaging, and data-heavy apps

## Best Practices

### Structure
- Organize by feature: controller, service, repository
- Keep controllers thin; logic in services
- Use constructor injection over field injection
- Package by feature, not by layer

### Data Access
- Use Spring Data repositories for CRUD
- Define entities explicitly; use DTOs at the boundary
- Add indexes and query methods deliberately
- Transactions on services, not controllers

### REST & Validation
- Use `@RestController` with `@Valid` on request bodies
- Return DTOs, never entities, to clients
- Handle errors with `@ControllerAdvice`
- Use proper HTTP status codes

### Testing
- Unit test services with mocks
- Integration test with `@SpringBootTest` and Testcontainers
- Use `MockMvc` for controller tests
- Keep tests isolated and fast

## Dependencies
```bash
# Maven or Gradle from start.spring.io
./mvnw spring-boot:run
```

## Examples
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

## Step-by-Step
1. Scaffold with Spring Initializr (Web, Data JPA, Validation).
2. Model the domain entities and repositories.
3. Build services with transactional business logic.
4. Add controllers returning DTOs with validation.
5. Centralize error handling with @ControllerAdvice.
6. Add security (Spring Security) for authN/authZ.
7. Write unit + integration tests.
8. Containerize and configure for deployment.

## Validation
1. `./mvnw test` passes
2. Endpoints return correct status and DTO shape
3. Validation rejects bad input with 400/422
4. Transactions roll back on failure
5. App starts cleanly in production profile

## Troubleshooting
- Circular dependencies: use constructor injection and refactor.
- LazyInitializationException: use DTOs and fetch eagerly in the service.
- Slow endpoints: add indexes and query methods instead of entity scans.