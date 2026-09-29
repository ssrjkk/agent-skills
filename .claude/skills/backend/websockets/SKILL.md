---
name: websockets
description: "Build real-time features with WebSockets: connection lifecycle, protocols, backpressure, scaling, and reconnection. Use for live updates and chat."
category: backend
tags: [websockets, realtime, socket.io, chat, live-updates, bidirectional]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# WebSockets

> Building real-time, bidirectional communication with WebSockets.

## Quick Start
```bash
npm i ws
node server.js  # ws://localhost:8080
```

## When to Use
- Live updates (chat, notifications, dashboards)
- Collaborative editing and presence
- Streaming data and progress
- Bidirectional client-server interactions

## Best Practices

### Protocol Design
- Define message envelopes with a type + payload
- Version the message protocol
- Use JSON or a binary format consistently
- Include correlation/request IDs

### Connection Lifecycle
- Handle open, message, close, and error events
- Implement ping/pong keepalive
- Detect half-open connections
- Clean up resources on close

### Backpressure & Flow
- Respect slow consumers; don't buffer unbounded
- Use queues with limits and drop policies
- Batch high-frequency updates
- Pause/close on saturation

### Scaling
- Share state via pub/sub (Redis) across nodes
- Use sticky sessions or a gateway
- Reconnect with exponential backoff client-side
- Handle authentication at handshake

## Dependencies
```bash
npm i ws
# Python: pip install websockets
# Node: socket.io for fallback/rooms
```

## Examples
```js
// Minimal WebSocket server (Node)
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
# Python server with websockets
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
// Client with reconnect + backoff
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

## Step-by-Step
1. Define the message envelope and event types.
2. Set up the server with connection handling.
3. Add keepalive (ping/pong) and reconnection.
4. Implement broadcast and room/scope routing.
5. Add backpressure handling for slow clients.
6. Auth at the handshake (token/cookie).
7. Scale with a pub/sub backbone for multi-node.
8. Monitor connections, messages, and errors.

## Validation
1. Messages round-trip bidirectionally
2. Reconnection resumes without data loss
3. Keepalive detects dead connections
4. Slow consumers don't stall the server
5. Multi-node broadcast is consistent

## Troubleshooting
- Connections drop: add keepalive and check proxy timeouts.
- Order issues: use sequence numbers or a single writer per topic.
- Scale limits: move state to pub/sub and add a gateway.