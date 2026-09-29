---
name: swift-ios
description: "Build iOS apps with Swift and SwiftUI: views, state, navigation, concurrency, and Combine. Use for native Apple platforms."
category: mobile
tags: [swift, ios, swiftui, combine, concurrency, xcode, mobile]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Swift iOS

> Building native iOS apps with Swift and SwiftUI.

## Quick Start
```bash
# Xcode -> New Project -> SwiftUI App
# or: swift package init
```

## When to Use
- Native iOS/macOS/watchOS apps
- Modern SwiftUI interfaces
- Teams using Swift concurrency
- Apps for the App Store

## Best Practices

### SwiftUI Views
- Build declarative views from state
- Use `@State`, `@Binding`, `@Observable`
- Keep views small and composable
- Use SwiftUI navigation and sheets

### State Management
- Model state with `@Observable` classes
- Derive views from published state
- Use environment for shared objects
- Avoid storing derived data

### Concurrency
- Use async/await and actors
- Scope tasks to view lifecycle
- Use `Task` and `MainActor` for UI
- Avoid data races with actors

### Networking & Persistence
- Fetch with async/await
- Decode with Codable
- Cache with SwiftData or Core Data
- Handle errors and retries

## Dependencies
```bash
# Swift Package Manager
swift package init
```

## Examples
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
// Observable model
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
// Async networking with Codable
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
// Navigation
NavigationStack {
    List(store.users) { user in
        NavigationLink(user.name) { UserDetailView(user: user) }
    }
}
```

## Step-by-Step
1. Create a SwiftUI project.
2. Model the domain with Codable types.
3. Build views from `@Observable` state.
4. Add navigation and sheets.
5. Fetch data with async/await.
6. Persist with SwiftData when needed.
7. Handle errors and loading states.
8. Test with XCTest/XCUITest.

## Validation
1. Project builds without errors
2. Views react to state changes
3. Async work is scoped and safe
4. Navigation works end to end
5. Unit/UI tests pass

## Troubleshooting
- Main actor errors: mark UI code @MainActor.
- Data races: use actors for shared state.
- Broken decoding: align Codable with the API shape.