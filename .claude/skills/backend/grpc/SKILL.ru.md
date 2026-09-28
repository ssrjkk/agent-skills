---
name: grpc
description: "Build high-performance services with gRPC: protobuf schemas, unary/streaming RPCs, interceptors, and error handling. Use for inter-service communication."
category: backend
tags: [grpc, backend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: grpc
author: ssrjkk
---
# gRPC (Джи-Ар-Пи-Си)

> Высокопроизводительная коммуникация сервисов через gRPC.

## Быстрый старт
```bash
pip install grpcio grpcio-tools
# или Go:
go get google.golang.org/grpc
```

## Когда использовать
- Внутренние вызовы между сервисами
- Низколатентные, типизированные кросс-языковые API
- Стриминг (живые данные, прогресс)
- Микросервисы, разделяющие контракт через proto

## Лучшие практики

### Схемы
- Контракты определяйте в `.proto` сначала
- Семантическая нумерация полей proto3 (стабильная)
- Версионируйте через package и правила совместимости полей
- Держите сообщения небольшими и сфокусированными

### Стили RPC
- Unary — для запрос/ответ
- Server streaming — для пагинации или live-обновлений
- Client streaming — для загрузок и батчей
- Bidi streaming — для интерактивных сессий

### Реализация
- Генерируйте стабы в общий модуль
- Ставьте deadlines/timeouts на каждый вызов
- Interceptors — для логирования, auth, метрик
- Обрабатывайте статус-коды и богатые ошибки

### Операции
- Между сервисами — TLS/mTLS
- Retries с backoff для транзиентных ошибок
- Балансировка через client-side LB или service mesh
- Мониторинг задержки и ошибок по методам

## Зависимости
```bash
pip install grpcio grpcio-tools protobuf
# Go:
go get google.golang.org/grpc google.golang.org/protobuf
```

## Примеры
```proto
// proto/hello.proto
syntax = "proto3";
package hello;

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply);
  rpc StreamGreetings (HelloRequest) returns (stream HelloReply);
}

message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}
```
```python
import grpc
import hello_pb2, hello_pb2_grpc

class Greeter(hello_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return hello_pb2.HelloReply(message=f"Hello, {request.name}")

    def StreamGreetings(self, request, context):
        for i in range(5):
            yield hello_pb2.HelloReply(message=f"Hello #{i}, {request.name}")

server = grpc.server(grpc.ThreadPoolExecutor(max_workers=10))
hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
server.add_insecure_port("[::]:50051")
server.start()
server.wait_for_termination()
```
```python
# Клиент с deadline и retry
channel = grpc.insecure_channel("localhost:50051")
stub = hello_pb2_grpc.GreeterStub(channel)

try:
    reply = stub.SayHello(hello_pb2.HelloRequest(name="World"), timeout=5)
    print(reply.message)
except grpc.RpcError as e:
    print("status:", e.code(), e.details())
```
```go
// Go клиент с deadline
conn, _ := grpc.NewClient("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
defer conn.Close()
c := hellopb.NewGreeterClient(conn)

ctx, cancel := context.WithTimeout(context.Background(), time.Second)
defer cancel()
reply, err := c.SayHello(ctx, &hellopb.HelloRequest{Name: "World"})
```

## Пошаговое руководство
1. Определите контракт сервиса в `.proto`.
2. Сгенерируйте стабы для каждого языка.
3. Реализуйте сервер с бизнес-логикой.
4. Добавьте interceptors для auth, логирования и метрик.
5. Реализуйте клиентов с deadlines и retries.
6. Вне dev-окружений используйте TLS/mTLS.
7. Добавьте load balancing и circuit breakers.
8. Мониторьте задержку и error rates по методам.

## Валидация
1. Стабы генерируются чисто для всех языков
2. Unary и streaming вызовы возвращают корректные данные
3. Deadlines дают корректные статус-коды
4. Interceptors логируют и аутентифицируют
5. Распространение ошибок через правильные gRPC статус-коды

## Устранение неполадок
- DeadlineExceeded: поднимите таймауты или проверьте задержку ниже по стеку.
- Unimplemented: проверьте регистрацию метода на сервере.
- Connection refused: проверьте адрес сервера и порты.