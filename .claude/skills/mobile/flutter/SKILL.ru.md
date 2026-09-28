---
name: flutter
description: "Build cross-platform mobile apps with Flutter: widgets, state management, navigation, platform channels, and release builds. Use for iOS/Android/desktop."
category: mobile
tags: [flutter, mobile, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: flutter
author: ssrjkk
---
# Flutter (Флаттер)

> Красивые кросс-платформенные приложения на Flutter и Dart.

## Быстрый старт
```bash
flutter create my_app
cd my_app
flutter run
# сборка для подключённого устройства или эмулятора
```

## Когда использовать
- Кросс-платформенные мобильные приложения (iOS + Android)
- Desktop и web из одной кодовой базы
- Богатый кастомный UI без платформенных вьюх
- Быстрая итерация с hot reload

## Лучшие практики

### Виджеты
- Компонуйте мелкие виджеты, а не большие
- `StatelessWidget` — если состояние не нужно
- Переиспользуемые виджеты выносите в дерево
- Следуйте Material/Cupertino design-токенам

### Управление состоянием
- `setState` — только для локального состояния
- Для общего состояния — Provider/Riverpod
- Логику состояния держите вне виджетов (контроллеры)
- Иммутабельное состояние и явные пересборки

### Навигация и жизненный цикл
- Named routes или go_router
- Dispose контроллеров и подписок
- Обрабатывайте lifecycle (background/foreground)
- Не используйте context через async-промежутки (используйте mounted)

### Производительность
- `const`-конструкторы где можно
- Не пересобирайте большие поддеревья
- Для длинных списков — `ListView.builder`
- Профилируйте через Flutter DevTools

## Зависимости
```bash
flutter create my_app --platforms=android,ios
# состояние: flutter pub add provider
# навигация: flutter pub add go_router
```

## Примеры
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
// Состояние через Provider
class CounterController extends ChangeNotifier {
  int _value = 0;
  int get value => _value;
  void increment() { _value++; notifyListeners(); }
}
```
```dart
// Навигация go_router
final router = GoRouter(
  routes: [
    GoRoute(path: "/", builder: (_, __) => const HomeScreen()),
    GoRoute(path: "/detail/:id", builder: (_, s) => DetailScreen(id: s.pathParameters["id"]!)),
  ],
);
```
```dart
// Platform channel (вызов нативного кода)
import 'package:flutter/services.dart';

final channel = const MethodChannel("app/battery");
Future<int> getBattery() async {
  return await channel.invokeMethod("getBatteryLevel") as int;
}
```

## Пошаговое руководство
1. Создайте проект через `flutter create`.
2. Настройте структуру (features, theme, routes).
3. Соберите UI из мелких компонуемых виджетов.
4. Добавьте управление состоянием для общих данных.
5. Подключите навигацию через go_router или named routes.
6. Добавьте platform channels для нативных фич.
7. Тестируйте: widget tests и integration tests.
8. Соберите release-артефакты для публикации в сторы.

## Валидация
1. `flutter analyze` чисто
2. `flutter test` проходит
3. Приложение работает на эмуляторе и устройстве
4. Нет утечек провайдеров или ошибок жизненного цикла
5. Release-сборка проходит для целевых платформ

## Устранение неполадок
- "use_build_context_synchronously": проверяйте `mounted` перед async-использованием контекста.
- Медленный первый кадр: уменьшайте работу в build; лениво грузите тяжёлые данные.
- Ошибки platform channel: сверяйте имена методов и типы с обеих сторон.