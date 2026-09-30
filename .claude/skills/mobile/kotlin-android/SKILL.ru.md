---
name: kotlin-android
description: "Build Android apps with Kotlin: Compose UI, coroutines, architecture components, and Gradle. Use for modern native Android development."
category: mobile
tags: [kotlin-android, mobile, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: kotlin-android
author: ssrjkk
---
# Kotlin Android (Котлин Андроид)

> Современные Android-приложения на Kotlin и Jetpack Compose.

## Быстрый старт
```bash
# Android Studio -> New Project -> Empty Compose Activity
./gradlew assembleDebug
```

## Когда использовать
- Нативные Android-приложения
- Современный UI на Jetpack Compose
- Команды на Kotlin-корутинах
- Приложения для Play Store

## Лучшие практики

### UI на Compose
- Декларативный UI через composables
- State hoisting; composables stateless
- `remember`/`derivedStateOf` для состояния
- Material 3 компоненты

### Архитектура
- MVVM: ViewModel + StateFlow
- Repository pattern для источников данных
- UI без бизнес-логики
- `collectAsStateWithLifecycle`

### Конкурентность
- Корутины для async-работы
- viewModelScope/lifecycleScope
- Flow для потоков
- Без блокировки main thread

### Навигация и DI
- Compose Navigation
- Hilt для DI
- Nav graphs по фичам
- Корректный скоуп зависимостей

## Зависимости
```bash
# build.gradle.kts
implementation("androidx.compose.ui:ui")
implementation("androidx.lifecycle:lifecycle-viewmodel-compose")
implementation("com.google.dagger:hilt-android")
```

## Примеры
```kotlin
// Composable UI
@Composable
fun CounterScreen(viewModel: CounterViewModel = viewModel()) {
    val count by viewModel.count.collectAsStateWithLifecycle()
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.padding(24.dp)
    ) {
        Text(text = "Count: $count", style = MaterialTheme.typography.headlineMedium)
        Button(onClick = { viewModel.increment() }) { Text("Add") }
    }
}
```
```kotlin
// ViewModel со StateFlow
class CounterViewModel : ViewModel() {
    private val _count = MutableStateFlow(0)
    val count: StateFlow<Int> = _count.asStateFlow()
    fun increment() { _count.update { it + 1 } }
}
```
```kotlin
// Корутина + репозиторий
class UserRepository(private val api: Api) {
    suspend fun loadUsers(): List<User> = withContext(Dispatchers.IO) {
        api.fetchUsers()
    }
}
```
```kotlin
// Навигация
@Composable
fun App() {
    val nav = rememberNavController()
    NavHost(navController = nav, startDestination = "home") {
        composable("home") { HomeScreen(onOpen = { nav.navigate("detail") }) }
        composable("detail") { DetailScreen() }
    }
}
```

## Пошаговое руководство
1. Создайте Compose-проект.
2. Настройте Hilt и навигацию.
3. Соберите UI на composables и Material 3.
4. Добавьте ViewModels со StateFlow.
5. Подключите репозитории на корутинах.
6. Обработайте состояния loading/error.
7. Тестируйте Compose UI-тестами.
8. Собирайте и публикуйте.

## Валидация
1. `./gradlew build` проходит
2. UI рендерится и реагирует на состояние
3. Корутины скоуплены и отменяются
4. Навигация работает между экранами
5. Юнит/UI тесты проходят

## Устранение неполадок
- Блокировка main thread: перенесите работу на Dispatchers.IO.
- Состояние не обновляется: StateFlow + collectAsStateWithLifecycle.
- Утечки памяти: скоуп корутин через viewModelScope.