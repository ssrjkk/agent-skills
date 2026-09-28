---
name: mcp-servers
description: "Build Model Context Protocol servers and clients: tools, resources, prompts, transport, and secure agent integration. Use for connecting agents to external systems."
category: ai
tags: [mcp, model-context-protocol, agents, tools, server, llm, integration]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-25
updated: 2026-09-28
author: ssrjkk
---
# MCP Servers

> Building Model Context Protocol servers that connect agents to real systems.

## Quick Start
```bash
# Fastest way: use the Python SDK
pip install "mcp[cli]"
# or Node:
npm install @modelcontextprotocol/sdk
```

## When to Use
- Giving agents access to internal APIs, databases, or files
- Building reusable tool integrations across agents
- Exposing company data safely to LLM assistants
- Multi-agent systems that share capability servers

## Best Practices

### Tools
- Model each action as a tool with a JSON schema
- Keep tool descriptions concise and unambiguous
- Validate inputs and return structured errors
- Batch related operations into one tool when possible

### Resources
- Expose static data as resources (files, config, prompts)
- Use URI scheme per data source (`file://`, `db://`)
- Make resource contents read-only unless needed
- Provide meaningful `resourceTemplates` for dynamic URIs

### Transport
- Use `stdio` for local single-process servers
- Use `Streamable HTTP` for remote deployments
- Prefer streaming responses for long operations
- Set timeouts and handle disconnect gracefully

### Security
- Authenticate and authorize every request
- Never expose secrets or raw DB credentials
- Sandbox file access; deny dangerous paths
- Audit tool calls and resource reads

## Dependencies
```bash
pip install "mcp[cli]"
npm install @modelcontextprotocol/sdk
npx @modelcontextprotocol/inspector  # debug tool
```

## Examples
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
# Resource exposing configuration
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("config")

@mcp.resource("config://app")
def app_config() -> str:
    return '{"log_level": "info", "timeout": 30}'
```
```python
# Tool with structured validation and errors
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
// Node.js MCP server
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({ name: "demo", version: "1.0.0" });

server.tool("add", { a: "number", b: "number" }, ({ a, b }) => ({
  content: [{ type: "text", text: String(a + b) }],
}));

await server.connect(new StdioServerTransport());
```

## Step-by-Step
1. Choose a transport: stdio for local, HTTP for remote.
2. Define the tools your agent needs; model inputs with schemas.
3. Add resources and prompts for static data and reusable prompts.
4. Implement handlers with validation and structured errors.
5. Secure the server: auth, sandboxing, and auditing.
6. Test with the MCP Inspector and a real agent.
7. Document the tool set in the server README.
8. Deploy and monitor usage; version the API.

## Validation
1. Inspector connects and lists tools/resources
2. Each tool returns correct output for valid input
3. Invalid input returns a structured error
4. Auth rejects unauthorized requests
5. Agent can call tools end-to-end over the chosen transport

## Troubleshooting
- "Server not found": check the transport config and connection URL.
- Tool returns wrong types: align schemas with actual handlers.
- Timeouts: enable streaming or raise limits for long operations.