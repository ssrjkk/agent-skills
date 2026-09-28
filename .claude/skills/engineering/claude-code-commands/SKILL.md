---
name: claude-code-commands
description: "Use Claude Code effectively: slash commands, context management, hooks, MCP, permissions, and workflows. Use for agentic coding with Claude Code."
category: engineering
tags: [claude-code, claude, commands, agent, cli, workflow, skills]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-25
updated: 2026-09-28
author: ssrjkk
---
# Claude Code Commands

> Getting the most out of Claude Code with commands, hooks, and skills.

## Quick Start
```bash
# Install and start
npm install -g @anthropic-ai/claude-code
cd your-project
claude
# then in the REPL: /help, /clear, /add <file>, /model sonnet
```

## When to Use
- Everyday agentic coding in the terminal
- Multi-file refactors and feature work
- Reviewing code and running tests with the agent
- Extending the agent with skills and MCP

## Best Practices

### Slash Commands
- Use `/init` to create an AGENTS.md at project start
- Use `/add` and `/drop` to manage context files
- Use `/compact` to summarize long conversations
- Use `/status` to review pending edits and costs

### Context Management
- Keep an `AGENTS.md` with project conventions
- Load only relevant files; drop noise
- Use `@path/to/file` to reference specific files
- `/clear` between unrelated tasks

### Hooks & Permissions
- Add hooks for formatting and linting before/after edits
- Use permission rules to avoid prompts for routine actions
- Review approvals for destructive commands
- Configure settings per project or user

### Skills & MCP
- Install skills into `.claude/skills/`
- Connect MCP servers for external tools
- Keep skill files short and focused
- Test skills with a representative task

## Dependencies
```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

## Examples
```bash
# Project setup
claude
> /init            # create AGENTS.md
> /model sonnet    # pick the model
> /permissions     # configure permission rules
```
```bash
# Working with files
> /add src/core.py tests/test_core.py
> /status
> /compact
> /clear
```
```bash
# One-shot non-interactive
claude -p "Run the tests and fix failures"
claude -p "Explain the architecture of this repo" --output-format json
```
```bash
# Hooks example (pre-edit formatting)
# .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Edit|Write", "hooks": [{ "type": "command", "command": "ruff format ." }] }
    ]
  }
}
```

## Step-by-Step
1. Install Claude Code and start a session in your project.
2. Run `/init` to establish project context and conventions.
3. Load relevant files with `/add`; drop noise.
4. Work iteratively; review with `/status`.
5. Compact long sessions; clear between tasks.
6. Add hooks for linting and formatting.
7. Install skills and MCP servers for your stack.
8. Configure permissions to keep the flow fast and safe.

## Validation
1. AGENTS.md captures project conventions
2. Context is focused (no stale files loaded)
3. Hooks run and keep code formatted
4. Destructive actions require approval
5. Skills/MCP work on a representative task

## Troubleshooting
- Wrong context: `/add` the right files, `/clear` stale state.
- Too many prompts: tighten permission rules.
- Slow agent: reduce context size and file count.