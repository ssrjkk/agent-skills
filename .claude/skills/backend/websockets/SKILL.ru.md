---
name: websockets
description: "Build real-time features with WebSockets: connection lifecycle, protocols, backpressure, scaling, and reconnection. Use for live updates and chat."
category: backend
tags: [websockets, backend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: websockets
author: ssrjkk
---
# WebSockets (ВебСокеты)

> Двунаправленная связь в реальном времени через WebSockets.

## Быстрый старт
```bash
npm i ws
node server.js  # ws://localhost:8080
```

## Когда использовать
- Live-обновления (чат, уведомления, дашборды)
- Совместное редактирование и presence
- Стриминг данных и прогресс
- Двунаправленные взаимодействия клиент-сервер

## Лучшие практики

### Дизайн протокола
- Конверты сообщений: type + payload
- Версионируйте протокол сообщений
- Консистентный JSON или бинарный формат
- Correlation/request ID

### Жизненный цикл соединения
- Обрабатывайте open, message, close, error
- Keepalive через ping/pong
- Детектируйте half-open соединения
- Чистите ресурсы при закрытии

### Backpressure и поток
- Уважайте медленных потребителей; без бесконечных буферов
- Очереди с лимитами и политикой дропа
- Батчите частые обновления
- Пауза/закрытие при насыщении

### Масштабирование
- Общее состояние через pub/sub (Redis) между нодами
- Sticky sessions или gateway
- Реconnect с экспоненциальным backoff на клиенте
- Auth на этапе handshake

## Зависимости
```bash
npm i ws
# Python: pip install websockets
# Node: socket.io для fallback/rooms
```

## Примеры
```js
// Минимальный WebSocket сервер (Node)
import { WebSocketServer } from "ws";

const wss = new WebSocketServer({ port: 8080 });
wss.on("connection", (ws) => {
  ws.send(JSON.stringify({ type: "hello", data: "welcome" }));
  ws.on("message", (raw) => {
    const msg = JSON.parse(raw.toString());
    broadcast({ type: "chat", data: msg });
  });
});

function broadcast(obj) {
  const text = JSON.stringify(obj);
  wss.clients.forEach((c) => c.readyState === 1 && c.send(text));
}
```
```python
# Python сервер через websockets
import asyncio, websockets

async def handler(ws):
    await ws.send("hello")
    async for raw in ws:
        await ws.send("echo: " + raw)

async def main():
    async with websockets.serve(handler, "localhost", 8080):
        await asyncio.Future()

asyncio.run(main())
```
```js
// Клиент с реконнектом и backoff
function connect(url) {
  const ws = new WebSocket(url);
  let delay = 500;
  ws.onclose = () => setTimeout(() => connect(url), delay);
  ws.onopen = () => { delay = 500; };
  return ws;
}
```
```js
// Keepalive ping/pong
const interval = setInterval(() => {
  if (ws.readyState === 1) {
    ws.ping();
    if (!ws.isAlive) return ws.terminate();
    ws.isAlive = false;
  }
}, 30000);
```

## Пошаговое руководство
1. Определите конверт сообщений и типы событий.
2. Настройте сервер с обработкой соединений.
3. Добавьте keepalive (ping/pong) и реконнект.
4. Реализуйте broadcast и роутинг по комнатам/скоупам.
5. Добавьте обработку backpressure для медленных клиентов.
6. Auth на handshake (token/cookie).
7. Масштабируйте через pub/sub backbone для multi-node.
8. Мониторьте соединения, сообщения и ошибки.

## Валидация
1. Сообщения проходят в обе стороны
2. Реконнект возобновляется без потерь
3. Keepalive детектирует мёртвые соединения
4. Медленные потребители не стопорят сервер
5. Multi-node broadcast консистентен

## Устранение неполадок
- Соединения падают: добавьте keepalive и проверьте таймауты прокси.
- Проблемы порядка: sequence numbers или один писатель на топик.
- Пределы масштаба: состояние в pub/sub и gateway.