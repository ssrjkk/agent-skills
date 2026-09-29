---
name: angular
description: "Build enterprise web apps with Angular: components, signals, services, dependency injection, and testing. Use for scalable structured frontends."
category: frontend
tags: [angular, frontend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: angular
author: ssrjkk
---
# Angular (Ангуляр)

> Масштабируемые корпоративные фронтенды на Angular.

## Быстрый старт
```bash
npm install -g @angular/cli
ng new my-app
cd my-app && ng serve
```

## Когда использовать
- Корпоративные single-page приложения
- Команды, которым нужна структура и конвенции
- Большие приложения со многими разработчиками
- Реактивные потоки данных через RxJS

## Лучшие практики

### Компоненты и сигналы
- Сигналы (`signal()`) для реактивного состояния
- `computed()` для производных значений
- `@Input()`/`@Output()` для границ
- Компоненты сфокусированы; `OnPush` change detection

### Dependency injection
- Сервисы с правильным скоупом
- `inject()` вместо конструкторной инъекции
- `providedIn: 'root'` для общих сервисов
- Внешние API за сервисами

### Реактивное состояние
- Сигналы для UI-состояния
- RxJS для async-потоков и событий
- Серверное состояние через `httpClient` + effects
- Отписка через `takeUntilDestroyed`

### Структура
- По фичам (standalone компоненты)
- Лениво загружаемые маршруты
- Декларативные шаблоны с pipes
- API-вызовы централизованы в сервисах

## Зависимости
```bash
ng new my-app --style scss --routing
npm i @angular/common
```

## Примеры
```typescript
// Компонент на сигналах
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
// Injectable сервис
import { Injectable, inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";

@Injectable({ providedIn: "root" })
export class UserService {
  private http = inject(HttpClient);
  getUsers() { return this.http.get<User[]>("/api/users"); }
}
```
```typescript
// Standalone компонент с DI
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
// Маршрут с ленивой загрузкой
const routes: Routes = [
  { path: "users", loadComponent: () => import("./users.component").then(m => m.UsersComponent) },
];
```

## Пошаговое руководство
1. Скаффолд через Angular CLI.
2. Настройте роутинг и shell-layout.
3. Соберите feature-модули из standalone-компонентов.
4. Сервисы с DI для доступа к данным.
5. Сигналы для UI-состояния, RxJS для потоков.
6. Лениво грузите маршруты.
7. Добавьте формы и валидацию.
8. Тесты через Angular testing library.

## Валидация
1. `ng build` проходит с проверкой типов
2. Компоненты рендерятся и реагируют на сигналы
3. Сервисы провайдятся и инжектируются
4. Ленивые маршруты грузятся по требованию
5. Тесты проходят для компонентов/сервисов

## Устранение неполадок
- Проблемы change detection: OnPush и сигналы.
- Утечки памяти: takeUntilDestroyed для подписок.
- Ошибки DI: проверьте скоуп провайдеров и `providedIn`.