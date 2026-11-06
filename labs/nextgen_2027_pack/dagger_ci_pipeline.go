// Программируемый CI/CD пайплайн 2026-2027 на Go + Dagger SDK (вместо YAML)
// Запускается одинаково локально на ноутбуке и в любом CI: dagger run go run dagger_ci_pipeline.go
package main

import (
	"context"
	"fmt"
	"os"

	"dagger.io/dagger"
)

func main() {
	ctx := context.Background()

	client, err := dagger.Connect(ctx, dagger.WithLogOutput(os.Stderr))
	if err != nil {
		panic(err)
	}
	defer client.Close()

	src := client.Host().Directory("./pet_project_app")

	// 1. Запуск тестов и компиляция статического бинарника в контейнере Go 1.23
	builder := client.Container().
		From("golang:1.23-alpine").
		WithMountedDirectory("/src", src).
		WithWorkdir("/src").
		WithEnvVariable("CGO_ENABLED", "0").
		WithExec([]string{"go", "test", "-v", "./..."}).
		WithExec([]string{"go", "build", "-ldflags=-w -s", "-o", "/bin/app", "main.go"})

	// 2. Упаковка в минимальный distroless:nonroot образ
	prodImage := client.Container().
		From("gcr.io/distroless/static-debian12:nonroot").
		WithFile("/app", builder.File("/bin/app")).
		WithEntrypoint([]string{"/app"})

	// Экспорт собранного тарбола для проверки Trivy
	tarPath := "/tmp/backend-api-image.tar"
	_, err = prodImage.Export(ctx, tarPath)
	if err != nil {
		panic(err)
	}

	fmt.Println("Dagger pipeline succeeded: tests passed and distroless image built!")
}
