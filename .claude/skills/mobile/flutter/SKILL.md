---
name: flutter
description: "Build cross-platform mobile apps with Flutter: widgets, state management, navigation, platform channels, and release builds. Use for iOS/Android/desktop."
category: mobile
tags: [flutter, dart, mobile, cross-platform, widgets, state, ios, android]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-26
updated: 2026-09-28
author: ssrjkk
---
# Flutter

> Building beautiful cross-platform apps with Flutter and Dart.

## Quick Start
```bash
flutter create my_app
cd my_app
flutter run
# builds for your connected device or emulator
```

## When to Use
- Cross-platform mobile apps (iOS + Android)
- Desktop and web from one codebase
- Rich custom UI without platform views
- Fast iteration with hot reload

## Best Practices

### Widgets
- Compose small widgets over large ones
- Use `StatelessWidget` unless state is needed
- Extract reusable widgets into the widget tree
- Follow Material/Cupertino design tokens

### State Management
- Use `setState` for local state only
- Adopt Provider/Riverpod for shared state
- Keep state logic out of widgets (controllers)
- Use immutable state and explicit rebuilds

### Navigation & Lifecycle
- Use named routes or go_router
- Dispose controllers and subscriptions
- Handle app lifecycle (background/foreground)
- Avoid context across async gaps (use mounted)

### Performance
- Use `const` constructors where possible
- Avoid rebuilding large subtrees
- Use `ListView.builder` for long lists
- Profile with the Flutter DevTools

## Dependencies
```bash
flutter create my_app --platforms=android,ios
# state: flutter pub add provider
# navigation: flutter pub add go_router
```

## Examples
```dart
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(home: const CounterPage());
  }
}

class CounterPage extends StatefulWidget {
  const CounterPage({super.key});
  @override
  State<CounterPage> createState() => _CounterPageState();
}

class _CounterPageState extends State<CounterPage> {
  int _count = 0;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(child: Text('Count: $_count', style: const TextStyle(fontSize: 32))),
      floatingActionButton: FloatingActionButton(
        onPressed: () => setState(() => _count++),
        child: const Icon(Icons.add),
      ),
    );
  }
}
```
```dart
// State management with Provider
class CounterController extends ChangeNotifier {
  int _value = 0;
  int get value => _value;
  void increment() { _value++; notifyListeners(); }
}
```
```dart
// go_router navigation
final router = GoRouter(
  routes: [
    GoRoute(path: "/", builder: (_, __) => const HomeScreen()),
    GoRoute(path: "/detail/:id", builder: (_, s) => DetailScreen(id: s.pathParameters["id"]!)),
  ],
);
```
```dart
// Platform channel (calling native code)
import 'package:flutter/services.dart';

final channel = const MethodChannel("app/battery");
Future<int> getBattery() async {
  return await channel.invokeMethod("getBatteryLevel") as int;
}
```

## Step-by-Step
1. Create the project with `flutter create`.
2. Set up app structure (features, theme, routes).
3. Build the UI with small composable widgets.
4. Add state management for shared data.
5. Wire navigation with go_router or named routes.
6. Add platform channels for native features.
7. Test with widget tests and integration tests.
8. Build release artifacts for store submission.

## Validation
1. `flutter analyze` is clean
2. `flutter test` passes
3. App runs on emulator and device
4. No provider leaks or lifecycle errors
5. Release build succeeds for target platforms

## Troubleshooting
- "use_build_context_synchronously": check `mounted` before async context use.
- Slow first frame: reduce work in build; lazy-load heavy data.
- Platform channel errors: match method names and types across sides.