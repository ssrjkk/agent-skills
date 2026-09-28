---
name: go-rest-api
description: "Build production REST APIs in Go with the standard library or Gin, including routing, middleware, JSON handling, and testing. Use for performant backends."
category: backend
tags: [go-rest-api, backend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: go-rest-api
author: ssrjkk
---
# Go REST API (Go РЕСТ-АПИ)

> Создание быстрых конкурентных REST API на Go.

## Быстрый старт
```bash
go mod init example.com/myapi
go run .  # http://localhost:8080
```

## Когда использовать
- Сервисы и бэкенды с высокой конкурентностью
- Микросервисы, которым нужны маленькие статичные бинарники
- Команды, которым нужны простые примитивы конкурентности
- CLI и инструменты, которые также являются библиотеками

## Лучшие практики

### Структура
- Организуйте по фичам: `cmd/`, `internal/`, `pkg/`
- Держите обработчики тонкими; логику выносите в сервисы
- Используйте `net/http` с паттернами маршрутов Go 1.22+ или роутер
- Определяйте типы запросов/ответов явно

### Конкурентность
- Используйте goroutine для независимой работы; каналы — для координации
- Применяйте `context.Context` для отмены и дедлайнов
- Ограничивайте конкурентность семафорами или worker pools
- Защищайте общее состояние через `sync.Mutex` или атомики

### Ошибки и логирование
- Оборачивайте ошибки через `fmt.Errorf("%w", err)` и `errors.Is`
- Логируйте структурно через `slog`; включайте request ID
- Возвращайте корректные HTTP статус-коды и JSON-ошибки

## Зависимости
```bash
go mod init example.com/myapi
go get github.com/gin-gonic/gin   # опциональный роутер
```

## Примеры
```go
package main

import (
	"fmt"
	"net/http"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /health", healthHandler)
	mux.HandleFunc("POST /items", createItem)
	http.ListenAndServe(":8080", logMiddleware(mux))
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprint(w, `{"status":"ok"}`)
}
```
```go
// Gin-обработчик с JSON binding
package main

import "github.com/gin-gonic/gin"

type Item struct {
	Name  string `json:"name" binding:"required"`
	Price float64 `json:"price" binding:"required"`
}

func createItem(c *gin.Context) {
	var item Item
	if err := c.ShouldBindJSON(&item); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusCreated, gin.H{"ok": true, "item": item})
}
```
```go
// Обработчик с контекстом и таймаутом
func slowHandler(ctx context.Context) func(http.ResponseWriter, *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		select {
		case <-time.After(2 * time.Second):
			fmt.Fprint(w, "done")
		case <-ctx.Done():
			w.WriteHeader(http.StatusGatewayTimeout)
		}
	}
}
```
```go
// Паттерн middleware
func logMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		slog.Info("request", "method", r.Method, "path", r.URL.Path)
		next.ServeHTTP(w, r)
	})
}
```

## Пошаговое руководство
1. Инициализируйте модуль и выберите подход к маршрутизации (stdlib паттерны или Gin).
2. Набросайте контракт API: маршруты, методы, JSON запросов/ответов.
3. Определите явные structs запросов/ответов с `json` тегами.
4. Реализуйте обработчики; держите их тонкими и делегируйте в сервисы.
5. Добавьте middleware для логирования, recovery, CORS и auth.
6. Используйте `context.Context` везде; задайте таймауты сервера.
7. Пишите table-driven тесты с `httptest`.
8. Добавьте линтеры (golangci-lint), staticcheck и `go vet` в CI.

## Валидация
1. `go build ./...` проходит
2. `go test ./...` проходит
3. `go vet ./...` чисто
4. Эндпоинты возвращают корректные статус-коды и JSON-форму
5. `go test -race ./...` не показывает гонок данных

## Устранение неполадок
- Гонки данных: защищайте общее состояние мьютексами или используйте каналы.
- Context canceled: учитывайте `ctx.Done()` в длинных операциях.
- Высокая задержка: добавляйте таймауты на сервере и исходящих клиентах.