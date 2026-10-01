---
name: grpc
description: "Build high-performance services with gRPC: protobuf schemas, unary/streaming RPCs, interceptors, and error handling. Use for inter-service communication."
category: backend
tags: [grpc, protobuf, rpc, microservices, streaming, schema, backend]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-26
updated: 2026-09-28
author: ssrjkk
---
# gRPC

> Building high-performance service communication with gRPC.

## Quick Start
```bash
pip install grpcio grpcio-tools
# or Go:
go get google.golang.org/grpc
```

## When to Use
- Internal service-to-service calls
- Low-latency, typed, cross-language APIs
- Streaming use cases (live data, progress)
- Microservices that share a contract via proto

## Best Practices

### Schemas
- Define contracts in `.proto` first
- Use semantic proto3 field numbering (stable)
- Version via package and field compatibility rules
- Keep messages small and focused

### RPC Styles
- Use unary for request/response
- Server streaming for pagination or live updates
- Client streaming for uploads and batching
- Bidi streaming for interactive sessions

### Implementation
- Generate stubs into a shared module
- Set deadlines/timeouts on every call
- Use interceptors for logging, auth, metrics
- Handle status codes and rich errors

### Operations
- Use TLS/mTLS between services
- Add retries with backoff for transient errors
- Load balance with client-side LB or service mesh
- Monitor latency and error rates per method

## Dependencies
```bash
pip install grpcio grpcio-tools protobuf
# Go:
go get google.golang.org/grpc google.golang.org/protobuf
```

## Examples
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
# Client with deadline and retry
channel = grpc.insecure_channel("localhost:50051")
stub = hello_pb2_grpc.GreeterStub(channel)

try:
    reply = stub.SayHello(hello_pb2.HelloRequest(name="World"), timeout=5)
    print(reply.message)
except grpc.RpcError as e:
    print("status:", e.code(), e.details())
```
```go
// Go client with deadline
conn, _ := grpc.NewClient("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
defer conn.Close()
c := hellopb.NewGreeterClient(conn)

ctx, cancel := context.WithTimeout(context.Background(), time.Second)
defer cancel()
reply, err := c.SayHello(ctx, &hellopb.HelloRequest{Name: "World"})
```

## Step-by-Step
1. Define the service contract in a `.proto` file.
2. Generate stubs for each language.
3. Implement the server with business logic.
4. Add interceptors for auth, logging, and metrics.
5. Implement clients with deadlines and retries.
6. Use TLS/mTLS in non-dev environments.
7. Add load balancing and circuit breakers.
8. Monitor per-method latency and error rates.

## Validation
1. Stubs generate cleanly for all languages
2. Unary and streaming calls return correct data
3. Deadlines trigger appropriate status codes
4. Interceptors log and authenticate
5. Error propagation uses proper gRPC status codes

## Troubleshooting
- DeadlineExceeded: raise timeouts or check downstream latency.
- Unimplemented: verify the method is registered on the server.
- Connection refused: check the server address and ports.