---
name: swift-ios
description: "Build iOS apps with Swift and SwiftUI: views, state, navigation, concurrency, and Combine. Use for native Apple platforms."
category: mobile
tags: [swift-ios, mobile, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: swift-ios
author: ssrjkk
---
# Swift iOS (Свифт АйОЭс)

> Нативные iOS-приложения на Swift и SwiftUI.

## Быстрый старт
```bash
# Xcode -> New Project -> SwiftUI App
# или: swift package init
```

## Когда использовать
- Нативные iOS/macOS/watchOS приложения
- Современные SwiftUI-интерфейсы
- Команды на Swift-конкурентности
- Приложения для App Store

## Лучшие практики

### SwiftUI Views
- Декларативные вьюхи из состояния
- `@State`, `@Binding`, `@Observable`
- Вьюхи маленькие и компонуемые
- SwiftUI navigation и sheets

### Управление состоянием
- Состояние через `@Observable` классы
- Вьюхи из published state
- Environment для общих объектов
- Без хранения производных данных

### Конкурентность
- async/await и actors
- Скоуп задач на жизненный цикл вьюхи
- `Task` и `MainActor` для UI
- Actors против гонок данных

### Сеть и персистентность
- Fetch через async/await
- Декодирование через Codable
- Кэш через SwiftData или Core Data
- Обработка ошибок и retries

## Зависимости
```bash
# Swift Package Manager
swift package init
```

## Примеры
```swift
import SwiftUI

struct CounterView: View {
    @State private var count = 0

    var body: some View {
        VStack(spacing: 12) {
            Text("Count: \(count)")
                .font(.headline)
            Button("Add") { count += 1 }
                .buttonStyle(.borderedProminent)
        }
    }
}
```
```swift
// Observable модель
import Observation

@Observable
final class UserStore {
    var users: [User] = []
    var isLoading = false

    func load() async {
        isLoading = true
        defer { isLoading = false }
        users = try! await api.fetchUsers()
    }
}
```
```swift
// Async networking с Codable
struct User: Codable, Identifiable {
    let id: Int
    let name: String
}

func fetchUsers() async throws -> [User] {
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode([User].self, from: data)
}
```
```swift
// Навигация
NavigationStack {
    List(store.users) { user in
        NavigationLink(user.name) { UserDetailView(user: user) }
    }
}
```

## Пошаговое руководство
1. Создайте SwiftUI-проект.
2. Смоделируйте домен через Codable-типы.
3. Соберите вьюхи из `@Observable` состояния.
4. Добавьте навигацию и sheets.
5. Грузите данные через async/await.
6. Персистентность через SwiftData при необходимости.
7. Обрабатывайте ошибки и loading-состояния.
8. Тесты XCTest/XCUITest.

## Валидация
1. Проект собирается без ошибок
2. Вьюхи реагируют на изменения состояния
3. Async-работа скоуплена и безопасна
4. Навигация работает end to end
5. Юнит/UI тесты проходят

## Устранение неполадок
- Ошибки Main actor: помечайте UI-код @MainActor.
- Гонки данных: actors для общего состояния.
- Сломанный декодинг: согласуйте Codable с формой API.