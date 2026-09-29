---
name: rust-tokio
description: "Async Rust with Tokio runtime"
category: backend
tags: [rust, tokio, async, concurrency, runtime]
models: [sonnet, opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# Rust Tokio

> Build high-performance async applications in Rust using the Tokio runtime.

## Quick Start
```rust
use tokio::net::TcpListener;
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use std::sync::Arc;
use tokio::sync::Mutex;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let listener = TcpListener::bind("127.0.0.1:8080").await?;
    let counter = Arc::new(Mutex::new(0u64));

    println!("Server listening on :8080");

    loop {
        let (socket, addr) = listener.accept().await?;
        let counter = counter.clone();
        
        tokio::spawn(async move {
            println!("New connection: {}", addr);
            
            let (reader, mut writer) = socket.into_split();
            let mut buf_reader = BufReader::new(reader);
            let mut line = String::new();

            loop {
                line.clear();
                match buf_reader.read_line(&mut line).await {
                    Ok(0) => break, // EOF
                    Ok(_) => {
                        let response = format!("Echo: {}", line.trim());
                        
                        // Update shared counter
                        let mut count = counter.lock().await;
                        *count += 1;
                        drop(count);

                        if let Err(e) = writer.write_all(response.as_bytes()).await {
                            eprintln!("Write error: {}", e);
                            break;
                        }
                        if let Err(e) = writer.write_all(b"\n").await {
                            eprintln!("Write error: {}", e);
                            break;
                        }
                    }
                    Err(e) => {
                        eprintln!("Read error: {}", e);
                        break;
                    }
                }
            }
            println!("Connection closed: {}", addr);
        });
    }
}
```

```rust
// Async HTTP client
use reqwest;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Concurrent requests with join
    let urls = vec![
        "https://api.example.com/users",
        "https://api.example.com/products",
        "https://api.example.com/orders",
    ];

    let mut handles = Vec::new();
    for url in urls {
        handles.push(tokio::spawn(async move {
            reqwest::get(url).await.unwrap().text().await.unwrap()
        }));
    }

    // Join all concurrent requests
    for handle in handles {
        let result = handle.await?;
        println!("Got response: {} bytes", result.len());
    }

    Ok(())
}
```

## Key Concepts
Tokio is an async runtime for Rust providing I/O, timers, synchronization primitives, and task scheduling. Use `#[tokio::main]` to enter async context. `tokio::spawn` creates concurrent tasks. Use `Mutex`/`RwLock` for shared state.

## When to Use
- High-throughput network services (HTTP servers, proxies)
- Real-time systems (chat, gaming, streaming)
- Concurrent data processing pipelines
- Microservices requiring maximum performance

## Step-by-Step
1. Add Tokio: `cargo add tokio --features full` and set an async `main` with `#[tokio::main]`.
2. Pick the I/O primitive: `TcpListener`/`TcpStream` for sockets, `UnixListener` for local pipes, `tokio::fs` for async file access.
3. Handle each connection by `tokio::spawn` — never block tokio worker threads with synchronous work.
4. Share state via `tokio::sync::Mutex`/`RwLock` (or actor channels) cloned into tasks.
5. Add concurrency: use `tokio::join!`/`try_join!` for parallel awaits and `tokio::time::timeout` for deadlines.
6. Tune the runtime: set worker threads and run tests with `cargo test` under `--cfg tokio_unstable` if multi-thread stats are needed.

## Examples
```rust
// Fan-out to N concurrent tasks and aggregate results
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let handles: Vec<_> = (0..5)
        .map(|i| tokio::spawn(async move {
            sleep(Duration::from_millis(100 * i)).await;
            i * i
        }))
        .collect();

    let mut total = 0;
    for h in handles {
        total += h.await?;
    }
    println!("sum of squares = {total}");
    Ok(())
}
```
```rust
// Graceful shutdown with CancellationToken
use tokio_util::sync::CancellationToken;

#[tokio::main]
async fn main() {
    let token = CancellationToken::new();
    let child = token.clone();
    tokio::spawn(async move {
        tokio::select! {
            _ = child.cancelled() => println!("task cancelled"),
            _ = tokio::time::sleep(Duration::from_secs(60)) => println!("task done"),
        }
    });
    tokio::time::sleep(Duration::from_millis(50)).await;
    token.cancel();
    tokio::time::sleep(Duration::from_millis(50)).await;
}
```

1. Add Tokio: `cargo add tokio --features full` and set an async `main` with `#[tokio::main]`.
2. Pick the I/O primitive: `TcpListener`/`TcpStream` for sockets, `UnixListener` for local pipes, `tokio::fs` for async file access.
3. Handle each connection by `tokio::spawn` — never block tokio worker threads with synchronous work.
4. Share state via `tokio::sync::Mutex`/`RwLock` (or actor channels) cloned into tasks.
5. Add concurrency: use `tokio::join!`/`try_join!` for parallel awaits and `tokio::time::timeout` for deadlines.
6. Tune the runtime: set worker threads and run tests with `cargo test` under `--cfg tokio_unstable` if multi-thread stats are needed.

```rust
// Fan-out to N concurrent tasks and aggregate results
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let handles: Vec<_> = (0..5)
        .map(|i| tokio::spawn(async move {
            sleep(Duration::from_millis(100 * i)).await;
            i * i
        }))
        .collect();

    let mut total = 0;
    for h in handles {
        total += h.await?;
    }
    println!("sum of squares = {total}");
    Ok(())
}
```
```rust
// Graceful shutdown with CancellationToken
use tokio_util::sync::CancellationToken;

#[tokio::main]
async fn main() {
    let token = CancellationToken::new();
    let child = token.clone();
    tokio::spawn(async move {
        tokio::select! {
            _ = child.cancelled() => println!("task cancelled"),
            _ = tokio::time::sleep(Duration::from_secs(60)) => println!("task done"),
        }
    });
    tokio::time::sleep(Duration::from_millis(50)).await;
    token.cancel();
    tokio::time::sleep(Duration::from_millis(50)).await;
}
```

## Validation
1. `cargo run` starts server without panics
2. Multiple concurrent connections are handled
3. Shared state synchronization is race-condition free
4. Performance benchmarks show expected throughput
