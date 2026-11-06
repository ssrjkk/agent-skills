package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log/slog"
	"math/rand"
	"net"
	"net/http"
	"os"
	"os/signal"
	"sync/atomic"
	"syscall"
	"time"
)

var (
	reqTotal   uint64
	errTotal   uint64
	isReady    atomic.Bool
	logger     *slog.Logger
	pgAddr     string
	redisAddr  string
)

func main() {
	// Структурированный JSON-логгер для Loki / Vector
	logger = slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))
	slog.SetDefault(logger)

	pgAddr = getEnv("POSTGRES_ADDR", "postgres:5432")
	redisAddr = getEnv("REDIS_ADDR", "redis:6379")
	port := getEnv("PORT", "8080")

	isReady.Store(true)

	mux := http.NewServeMux()
	mux.HandleFunc("/healthz", healthzHandler)
	mux.HandleFunc("/readyz", readyzHandler)
	mux.HandleFunc("/metrics", metricsHandler)
	mux.HandleFunc("/api/orders", ordersHandler)

	srv := &http.Server{
		Addr:         ":" + port,
		Handler:      mux,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	// Запуск HTTP-сервера в отдельной горутине
	go func() {
		logger.Info("starting production microservice", "port", port, "postgres", pgAddr, "redis", redisAddr)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.Error("server failed", "error", err)
			os.Exit(1)
		}
	}()

	// Graceful Shutdown по сигналам SIGTERM / SIGINT
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGTERM, syscall.SIGINT)
	sig := <-stop

	logger.Info("received shutdown signal, draining connections", "signal", sig.String())
	isReady.Store(false)

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		logger.Error("graceful shutdown failed", "error", err)
	}
	logger.Info("server gracefully stopped")
}

func healthzHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"status":"alive"}`))
}

func readyzHandler(w http.ResponseWriter, r *http.Request) {
	if !isReady.Load() {
		http.Error(w, `{"status":"draining"}`, http.StatusServiceUnavailable)
		return
	}
	// Проверка TCP-доступности зависимостей
	if err := checkTCP(pgAddr); err != nil {
		logger.Warn("readiness check failed: postgres unreachable", "error", err)
		http.Error(w, `{"status":"postgres_unreachable"}`, http.StatusServiceUnavailable)
		return
	}
	if err := checkTCP(redisAddr); err != nil {
		logger.Warn("readiness check failed: redis unreachable", "error", err)
		http.Error(w, `{"status":"redis_unreachable"}`, http.StatusServiceUnavailable)
		return
	}
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"status":"ready"}`))
}

func ordersHandler(w http.ResponseWriter, r *http.Request) {
	start := time.Now()
	atomic.AddUint64(&reqTotal, 1)

	traceID := fmt.Sprintf("tr-%d", rand.Int63())
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("X-Trace-Id", traceID)

	// Имитация работы сервиса
	time.Sleep(time.Duration(15+rand.Intn(40)) * time.Millisecond)

	durationMs := time.Since(start).Milliseconds()
	logger.Info("order processed",
		"method", r.Method,
		"path", r.URL.Path,
		"status", http.StatusOK,
		"duration_ms", durationMs,
		"trace_id", traceID,
	)

	resp := map[string]any{
		"order_id":    rand.Intn(100000),
		"status":      "created",
		"duration_ms": durationMs,
		"trace_id":    traceID,
	}
	json.NewEncoder(w).Encode(resp)
}

func metricsHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain; version=0.0.4")
	fmt.Fprintf(w, "# HELP http_requests_total Total number of HTTP requests.
")
	fmt.Fprintf(w, "# TYPE http_requests_total counter
")
	fmt.Fprintf(w, "http_requests_total{service="backend-api",status_code="200"} %d
", atomic.LoadUint64(&reqTotal))
	fmt.Fprintf(w, "http_requests_total{service="backend-api",status_code="500"} %d
", atomic.LoadUint64(&errTotal))
}

func checkTCP(addr string) error {
	conn, err := net.DialTimeout("tcp", addr, 1*time.Second)
	if err != nil {
		return err
	}
	return conn.Close()
}

func getEnv(key, fallback string) string {
	if val := os.Getenv(key); val != "" {
		return val
	}
	return fallback
}
