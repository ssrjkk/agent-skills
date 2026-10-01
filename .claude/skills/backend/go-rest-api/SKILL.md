---
name: go-rest-api
description: "Build production REST APIs in Go with the standard library or Gin, including routing, middleware, JSON handling, and testing. Use for performant backends."
category: backend
tags: [go, golang, rest, api, http, backend, server]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-20
updated: 2026-09-28
---
# Go REST API

> Building fast, concurrent REST APIs in Go.

## Quick Start
```bash
go mod init example.com/myapi
go run .  # http://localhost:8080
```

## When to Use
- High-concurrency services and backends
- Microservices needing small, static binaries
- Teams wanting simple concurrency primitives
- CLIs and tools that double as libraries

## Best Practices

### Structure
- Organize by feature: `cmd/`, `internal/`, `pkg/`
- Keep handlers thin; move logic to services
- Use `net/http` with Go 1.22+ route patterns or a router
- Define request/response types explicitly

### Concurrency
- Use goroutines for independent work; channel for coordination
- Use `context.Context` for cancellation and deadlines
- Bound concurrency with semaphores or worker pools
- Protect shared state with `sync.Mutex` or atomics

### Errors & Logging
- Wrap errors with `fmt.Errorf("%w", err)` and `errors.Is`
- Log structured with `slog`; include request ID
- Return proper HTTP status codes and JSON errors

## Dependencies
```bash
go mod init example.com/myapi
go get github.com/gin-gonic/gin   # optional router
```

## Examples
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
// Gin-style handler with JSON binding
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
// Context-aware handler with timeout
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
// Middleware pattern
func logMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		slog.Info("request", "method", r.Method, "path", r.URL.Path)
		next.ServeHTTP(w, r)
	})
}
```

## Step-by-Step
1. Initialize the module and pick a routing approach (stdlib patterns or Gin).
2. Sketch the API contract: routes, methods, request/response JSON.
3. Define explicit request/response structs with `json` tags.
4. Implement handlers; keep them thin and delegate to services.
5. Add middleware for logging, recovery, CORS, and auth.
6. Use `context.Context` everywhere; set server timeouts.
7. Write table-driven tests with `httptest`.
8. Add linters (golangci-lint), staticcheck, and `go vet` to CI.

## Validation
1. `go build ./...` succeeds
2. `go test ./...` passes
3. `go vet ./...` clean
4. Endpoints return correct status codes and JSON shape
5. `go test -race ./...` shows no data races

## Troubleshooting
- Data races: guard shared state with mutexes or use channels.
- Context canceled: honor `ctx.Done()` in long operations.
- High latency: add timeouts on the server and on outbound clients.