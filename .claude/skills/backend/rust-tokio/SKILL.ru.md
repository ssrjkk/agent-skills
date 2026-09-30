---
name: rust-tokio
description: "Async Rust with Tokio runtime"
category: backend
tags: [rust-tokio, backend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: rust-tokio
---
# Rust Tokio

> Создавайте высокопроизводительные асинхронные приложения на Rust с runtime Tokio.

## Быстрый старт
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
// Асинхронный HTTP-клиент
use reqwest;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
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

    for handle in handles {
        let result = handle.await?;
        println!("Got response: {} bytes", result.len());
    }

    Ok(())
}
```

## Ключевые концепции
Tokio — асинхронный runtime для Rust: I/O, таймеры, примитивы синхронизации и планировщик задач. `#[tokio::main]` вводит в асинхронный контекст. `tokio::spawn` создаёт конкурентные задачи. Для разделяемого состояния используйте `Mutex`/`RwLock`.

## Когда использовать
- Высоконагруженные сетевые сервисы (HTTP-серверы, прокси)
- Системы реального времени (чат, игры, стриминг)
- Конвейеры конкурентной обработки данных
- Микросервисы с максимальной производительностью

## Пошаговое руководство
1. Добавьте Tokio: `cargo add tokio --features full` и async `main` через `#[tokio::main]`.
2. Выберите I/O-примитив: `TcpListener`/`TcpStream` для сокетов, `UnixListener` для локальных pipe, `tokio::fs` для асинхронного доступа к файлам.
3. Обрабатывайте каждое соединение через `tokio::spawn` — никогда не блокируйте worker-потоки синхронной работой.
4. Разделяйте состояние через `tokio::sync::Mutex`/`RwLock` (или actor-каналы), клонируя в задачи.
5. Добавляйте конкурентность: `tokio::join!`/`try_join!` для параллельных await и `tokio::time::timeout` для дедлайнов.
6. Настройте runtime: задайте число worker-потоков и запускайте тесты с `--cfg tokio_unstable` при необходимости.

## Примеры
```rust
// Fan-out на N конкурентных задач и агрегация результатов
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
// Graceful shutdown через CancellationToken
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

## Лучшие практики
- Tokio async runtime для I/O-bound задач; потоки для CPU-heavy.
- `tokio::spawn` с owned tasks; не блокируйте executor.
- Каналы для общения; `Arc<Mutex>` экономно.
- Таймауты через `tokio::time` против зависаний.
- `tokio::select!` для конкурентных awaitable источников.
- Бенчмарки с tracing при важности задержки.

## Устранение неполадок
- Runtime не найден: добавьте `tokio` с фичей `full` или `rt-multi-thread`.
- Блокировка executor: переносите sync-работу в `spawn_blocking`.
- Deadlock: крошечные области блокировок без await под ними.
- Паника задачи: JoinHandle или супервизор для рестарта.

## Валидация
1. `cargo run` запускает сервер без паник
2. Обрабатываются несколько конкурентных соединений
3. Синхронизация разделяемого состояния без гонок
4. Бенчмарки показывают ожидаемую пропускную способность
