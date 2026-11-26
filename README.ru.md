# Agent Skills

> **Языки:** [English](README.md) · [Русский](README.ru.md)

Библиотека из 120 двуязычных навыков в формате Agent Skills: английский `SKILL.md`
и русский `SKILL.ru.md` в каждой директории. Каталог, IT-roadmaps и руководства
опубликованы на отдельном сайте; Python SDK и CLI проверяют структуру, качество
и синхронность данных.

**Сайт:** https://ssrjkk.github.io/agent-skills/  
**Исходники:** https://github.com/ssrjkk/agent-skills

## Возможности

- 120 навыков в 20 предметных областях.
- Поиск по локальной библиотеке и опубликованному реестру.
- Валидация frontmatter, качества и совместимости с агентами.
- Генерация каталога, документации и npm-снимка.
- CI на Python 3.10–3.13, CodeQL и проверка сгенерированных файлов.

## Установка SDK и CLI

```bash
pip install agent-skills-library

agent-skills stats
agent-skills search fastapi
agent-skills search fastapi --remote
agent-skills validate
agent-skills quality
agent-skills catalog
```

## Установка навыков

```bash
curl -fsSL https://raw.githubusercontent.com/ssrjkk/agent-skills/main/scripts/install.sh | bash
```

Каждый навык — отдельная директория:

```text
.claude/skills/
  {domain}/
    {skill-name}/
      SKILL.md
      SKILL.ru.md
```

Тот же формат используется в `.opencode/skills/`, `.cursor/skills/` и других
каталогах агентов, реализующих Agent Skills.

## Локальные проверки

```bash
pip install -e ".[dev]"
make ci
```

`make ci` запускает lint, typecheck, тесты, валидацию навыков, roadmaps,
генерацию каталога и документации, проверку README и согласованность сайта.

## Документация

- [Каталог](https://ssrjkk.github.io/agent-skills/)
- [Реестр JSON](https://ssrjkk.github.io/agent-skills/skills_catalog.json)
- [IT Roadmaps](https://ssrjkk.github.io/agent-skills/roadmaps.html)
- [Руководства](https://ssrjkk.github.io/agent-skills/guides.html)
- [Архитектура](docs/ARCHITECTURE.md)
- [Безопасность](SECURITY.md)

## Лицензия

MIT — см. [LICENSE](LICENSE).
