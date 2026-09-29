---
name: kotlin-android
description: "Build Android apps with Kotlin: Compose UI, coroutines, architecture components, and Gradle. Use for modern native Android development."
category: mobile
tags: [kotlin, android, jetpack-compose, coroutines, gradle, mvvm]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Kotlin Android

> Building modern Android apps with Kotlin and Jetpack Compose.

## Quick Start
```bash
# Android Studio -> New Project -> Empty Compose Activity
./gradlew assembleDebug
```

## When to Use
- Native Android apps
- Modern UI with Jetpack Compose
- Teams using Kotlin coroutines
- Apps targeting Play Store

## Best Practices

### UI with Compose
- Build declarative UI with composables
- Use state hoisting; keep composables stateless
- Prefer `remember`/`derivedStateOf` for state
- Use Material 3 components

### Architecture
- Use MVVM with ViewModel + StateFlow
- Repository pattern for data sources
- Keep UI free of business logic
- Use `collectAsStateWithLifecycle`

### Concurrency
- Use coroutines for async work
- Scope with viewModelScope/lifecycleScope
- Use Flow for streams
- Avoid blocking main thread

### Navigation & DI
- Use Compose Navigation
- Use Hilt for dependency injection
- Define nav graphs per feature
- Scope dependencies correctly

## Dependencies
```bash
# build.gradle.kts
implementation("androidx.compose.ui:ui")
implementation("androidx.lifecycle:lifecycle-viewmodel-compose")
implementation("com.google.dagger:hilt-android")
```

## Examples
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
// ViewModel with StateFlow
class CounterViewModel : ViewModel() {
    private val _count = MutableStateFlow(0)
    val count: StateFlow<Int> = _count.asStateFlow()
    fun increment() { _count.update { it + 1 } }
}
```
```kotlin
// Coroutine + repository
class UserRepository(private val api: Api) {
    suspend fun loadUsers(): List<User> = withContext(Dispatchers.IO) {
        api.fetchUsers()
    }
}
```
```kotlin
// Navigation
@Composable
fun App() {
    val nav = rememberNavController()
    NavHost(navController = nav, startDestination = "home") {
        composable("home") { HomeScreen(onOpen = { nav.navigate("detail") }) }
        composable("detail") { DetailScreen() }
    }
}
```

## Step-by-Step
1. Create a Compose project.
2. Set up Hilt and navigation.
3. Build the UI with composables and Material 3.
4. Add ViewModels with StateFlow.
5. Wire repositories with coroutines.
6. Handle loading/error states.
7. Test with Compose UI tests.
8. Build and publish.

## Validation
1. `./gradlew build` passes
2. UI renders and reacts to state
3. Coroutines are scoped and cancelled
4. Navigation works across screens
5. Unit/UI tests pass

## Troubleshooting
- Main thread block: move work to Dispatchers.IO.
- State not updating: use StateFlow + collectAsStateWithLifecycle.
- Memory leaks: scope coroutines to viewModelScope.