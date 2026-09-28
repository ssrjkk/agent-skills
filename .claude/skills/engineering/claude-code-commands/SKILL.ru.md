---
name: claude-code-commands
description: "Use Claude Code effectively: slash commands, context management, hooks, MCP, permissions, and workflows. Use for agentic coding with Claude Code."
category: engineering
tags: [claude-code-commands, engineering, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: claude-code-commands
author: ssrjkk
---
# Claude Code Commands (Команды Клод-Код)

> Максимальная польза от Claude Code: команды, хуки и скиллы.

## Быстрый старт
```bash
# Установка и запуск
npm install -g @anthropic-ai/claude-code
cd your-project
claude
# в REPL: /help, /clear, /add <file>, /model sonnet
```

## Когда использовать
- Повседневное agentic-кодирование в терминале
- Мультифайловые рефакторинги и фичи
- Ревью кода и прогон тестов с агентом
- Расширение агента скиллами и MCP

## Лучшие практики

### Slash-команды
- `/init` — создание AGENTS.md в начале проекта
- `/add` и `/drop` — управление контекстными файлами
- `/compact` — сжатие длинных диалогов
- `/status` — обзор правок и стоимости

### Управление контекстом
- Держите `AGENTS.md` с конвенциями проекта
- Загружайте только нужные файлы; выкидывайте шум
- Ссылайтесь на файлы через `@path/to/file`
- `/clear` между несвязанными задачами

### Хуки и права
- Добавляйте хуки на форматирование и линтинг до/после правок
- Правила permissions — меньше промптов для рутины
- Ревью апрувов для разрушительных команд
- Настройки на проект или пользователя

### Скиллы и MCP
- Ставьте скиллы в `.claude/skills/`
- Подключайте MCP-серверы для внешних инструментов
- Держите скиллы короткими и сфокусированными
- Тестируйте скилл на репрезентативной задаче

## Зависимости
```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

## Примеры
```bash
# Настройка проекта
claude
> /init            # создание AGENTS.md
> /model sonnet    # выбор модели
> /permissions     # настройка правил
```
```bash
# Работа с файлами
> /add src/core.py tests/test_core.py
> /status
> /compact
> /clear
```
```bash
# Одноразовый неинтерактивный режим
claude -p "Run the tests and fix failures"
claude -p "Explain the architecture of this repo" --output-format json
```
```bash
# Пример хука (форматирование до правки)
# .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Edit|Write", "hooks": [{ "type": "command", "command": "ruff format ." }] }
    ]
  }
}
```

## Пошаговое руководство
1. Установите Claude Code и запустите сессию в проекте.
2. Выполните `/init` для контекста и конвенций.
3. Загрузите нужные файлы через `/add`; уберите шум.
4. Работайте итеративно; смотрите `/status`.
5. Компактизируйте длинные сессии; чистите между задачами.
6. Добавьте хуки на линтинг и форматирование.
7. Установите скиллы и MCP-серверы под ваш стек.
8. Настройте permissions для скорости и безопасности.

## Валидация
1. AGENTS.md фиксирует конвенции проекта
2. Контекст сфокусирован (нет устаревших файлов)
3. Хуки работают и держат код отформатированным
4. Разрушительные действия требуют апрува
5. Скиллы/MCP работают на репрезентативной задаче

## Устранение неполадок
- Неверный контекст: `/add` нужные файлы, `/clear` устаревшее.
- Слишком много промптов: ужесточите правила permissions.
- Медленный агент: уменьшите размер контекста и число файлов.