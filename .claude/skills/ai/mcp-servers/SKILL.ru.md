---
name: mcp-servers
description: "Build Model Context Protocol servers and clients: tools, resources, prompts, transport, and secure agent integration. Use for connecting agents to external systems."
category: ai
tags: [mcp-servers, ai, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: mcp-servers
author: ssrjkk
---
# MCP Servers (ЭмСиПи-серверы)

> Создание Model Context Protocol серверов, подключающих агентов к реальным системам.

## Быстрый старт
```bash
# Быстрее всего — Python SDK
pip install "mcp[cli]"
# или Node:
npm install @modelcontextprotocol/sdk
```

## Когда использовать
- Доступ агентов к внутренним API, базам данных или файлам
- Переиспользуемые интеграции инструментов между агентами
- Безопасный доступ компании к LLM-ассистентам
- Multi-agent системы с общими серверами возможностей

## Лучшие практики

### Инструменты
- Каждое действие — это tool с JSON-схемой
- Держите описания инструментов краткими и однозначными
- Валидируйте входы и возвращайте структурированные ошибки
- Группируйте связанные операции в один tool, когда можно

### Ресурсы
- Статичные данные — как ресурсы (файлы, конфиг, промпты)
- Схема URI на источник данных (`file://`, `db://`)
- Содержимое ресурсов read-only, если не нужно иначе
- Для динамических URI давайте `resourceTemplates`

### Транспорт
- `stdio` — для локальных однопроцессных серверов
- `Streamable HTTP` — для удалённых деплоев
- Предпочитайте стриминг для длинных операций
- Ставьте таймауты и корректно обрабатывайте разрывы

### Безопасность
- Аутентифицируйте и авторизуйте каждый запрос
- Никогда не отдавайте секреты или сырые креды БД
- Песочница для доступа к файлам; блокируйте опасные пути
- Аудируйте вызовы инструментов и чтения ресурсов

## Зависимости
```bash
pip install "mcp[cli]"
npm install @modelcontextprotocol/sdk
npx @modelcontextprotocol/inspector  # отладчик
```

## Примеры
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"Weather in {city}: sunny, 22C"

if __name__ == "__main__":
    mcp.run()
```
```python
# Ресурс с конфигурацией
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("config")

@mcp.resource("config://app")
def app_config() -> str:
    return '{"log_level": "info", "timeout": 30}'
```
```python
# Tool с валидацией и ошибками
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("todos")

class Todo(BaseModel):
    title: str
    done: bool = False

@mcp.tool()
def add_todo(todo: Todo) -> dict:
    if not todo.title.strip():
        return {"error": "title required"}
    todos.append(todo)
    return {"ok": True, "id": len(todos) - 1}
```
```typescript
// Node.js MCP сервер
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({ name: "demo", version: "1.0.0" });

server.tool("add", { a: "number", b: "number" }, ({ a, b }) => ({
  content: [{ type: "text", text: String(a + b) }],
}));

await server.connect(new StdioServerTransport());
```

## Пошаговое руководство
1. Выберите транспорт: stdio для локального, HTTP для удалённого.
2. Определите нужные агенту инструменты; смоделируйте входы схемами.
3. Добавьте ресурсы и промпты для статичных данных и переиспользуемых промптов.
4. Реализуйте обработчики с валидацией и структурированными ошибками.
5. Обеспечьте безопасность: auth, песочницу и аудит.
6. Тестируйте через MCP Inspector и реального агента.
7. Задокументируйте набор инструментов в README сервера.
8. Деплойте и мониторьте использование; версионируйте API.

## Валидация
1. Inspector подключается и показывает tools/resources
2. Каждый tool возвращает корректный вывод на валидный ввод
3. Невалидный ввод возвращает структурированную ошибку
4. Auth отклоняет неавторизованные запросы
5. Агент вызывает инструменты end-to-end через выбранный транспорт

## Устранение неполадок
- "Server not found": проверьте конфиг транспорта и URL подключения.
- Неверные типы на выходе: согласуйте схемы с фактическими обработчиками.
- Таймауты: включите стриминг или поднимите лимиты для длинных операций.