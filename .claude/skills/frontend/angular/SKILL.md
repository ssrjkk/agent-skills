---
name: angular
description: "Build enterprise web apps with Angular: components, signals, services, dependency injection, and testing. Use for scalable structured frontends."
category: frontend
tags: [angular, typescript, components, signals, dependency-injection, rxjs]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Angular

> Building scalable enterprise frontends with Angular.

## Quick Start
```bash
npm install -g @angular/cli
ng new my-app
cd my-app && ng serve
```

## When to Use
- Enterprise single-page applications
- Teams wanting structure and conventions
- Large apps with many developers
- Reactive data flows with RxJS

## Best Practices

### Components & Signals
- Use signals (`signal()`) for reactive state
- Use `computed()` for derived values
- Use `@Input()`/`@Output()` for boundaries
- Keep components focused; use `OnPush` change detection

### Dependency Injection
- Provide services at the right scope
- Use `inject()` over constructor injection
- Prefer `providedIn: 'root'` for shared services
- Abstract external APIs behind services

### Reactive State
- Prefer signals over manual subjects for UI state
- Use RxJS for async streams and events
- Manage server state with `httpClient` + effects
- Unsubscribe or use `takeUntilDestroyed`

### Structure
- Organize by feature modules (standalone components)
- Use lazy-loaded routes
- Keep templates declarative with pipes
- Centralize API calls in services

## Dependencies
```bash
ng new my-app --style scss --routing
npm i @angular/common
```

## Examples
```typescript
// Signal-based component
import { Component, signal, computed } from "@angular/core";

@Component({
  selector: "app-counter",
  template: `
    <button (click)="increment()">Count: {{ count() }}</button>
    <p>Doubled: {{ doubled() }}</p>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CounterComponent {
  count = signal(0);
  doubled = computed(() => this.count() * 2);
  increment() { this.count.update(c => c + 1); }
}
```
```typescript
// Injectable service
import { Injectable, inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";

@Injectable({ providedIn: "root" })
export class UserService {
  private http = inject(HttpClient);
  getUsers() { return this.http.get<User[]>("/api/users"); }
}
```
```typescript
// Standalone component with DI
@Component({
  standalone: true,
  imports: [CommonModule],
  template: `<ul><li *ngFor="let u of users$ | async">{{ u.name }}</li></ul>`,
})
export class UserListComponent {
  private users = inject(UserService);
  users$ = this.users.getUsers();
}
```
```typescript
// Route with lazy loading
const routes: Routes = [
  { path: "users", loadComponent: () => import("./users.component").then(m => m.UsersComponent) },
];
```

## Step-by-Step
1. Scaffold with the Angular CLI.
2. Set up routing and a shell layout.
3. Build feature modules with standalone components.
4. Add services with DI for data access.
5. Use signals for UI state, RxJS for streams.
6. Lazy-load routes.
7. Add forms and validation.
8. Write tests with the Angular testing library.

## Validation
1. `ng build` passes with type checking
2. Components render and react to signals
3. Services are provided and injectable
4. Lazy routes load on demand
5. Tests pass for components/services

## Troubleshooting
- Change detection issues: use OnPush and signals.
- Memory leaks: use takeUntilDestroyed for subscriptions.
- DI errors: check provider scope and `providedIn`.