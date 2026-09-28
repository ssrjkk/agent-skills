---
name: git-workflow
description: "Use Git effectively: branching, commits, rebase vs merge, history hygiene, conflict resolution, and collaboration workflows. Use for any git-based project."
category: engineering
tags: [git-workflow, engineering, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: git-workflow
author: ssrjkk
---
# Git Workflow (Гит-воркфлоу)

> Эффективное использование Git для чистой истории и гладкой коллаборации.

## Быстрый старт
```bash
git clone <repo>
git checkout -b feat/my-feature
# ... работа, коммиты ...
git push -u origin feat/my-feature
```

## Когда использовать
- Каждый программный проект (даже доки и конфиг)
- Работа с ветками и pull request
- Безопасное восстановление после ошибок
- Аудит кто, что и когда менял

## Лучшие практики

### Ветвление
- Feature-ветки от main; держите их недолгоживущими
- Нейминг по конвенции: `feat/`, `fix/`, `docs/`, `chore/`
- Синхронизируйтесь с main регулярно (`git fetch && git rebase`)
- Удаляйте смёрженные ветки

### Коммиты
- Коммитьте небольшими сфокусированными изменениями с ясными сообщениями
- Conventional commits: `feat:`, `fix:`, `refactor:`
- Объясняйте "почему" в теле сообщения при необходимости
- Никогда не коммитьте секреты и большие бинарники

### История
- Для локальной чистки — rebase; для общей интеграции — merge
- Скушивайте WIP-коммиты перед мержем
- Смотрите историю через `git log --oneline --graph`
- Не переписывайте запушенную историю в общих ветках

### Коллаборация
- Pull с rebase для линейной истории
- Конфликты решайте, понимая обе стороны
- Для прерываний используйте `git stash`
- Держите `main` всегда зелёным и релизабельным

## Зависимости
```bash
# Git 2.40+ рекомендуется
git --version
# Опционально: GitHub CLI для PR
gh --version
```

## Примеры
```bash
# Начните feature-ветку и коммитьте хорошо
git switch -c feat/user-auth
git add src/ tests/
git commit -m "feat: add user authentication

Adds email/password login with JWT issuance."
```
```bash
# Rebase на свежий main
git fetch origin
git rebase origin/main
git push --force-with-lease
```
```bash
# Безопасный откат
git restore src/          # отбросить рабочие изменения
git reset --soft HEAD~1   # отменить коммит, сохранить изменения
git revert <sha>          # безопасный откат на общей истории
```
```bash
# Инспекция истории
git log --oneline --graph -15
git show <sha>
git diff HEAD~1
```

## Пошаговое руководство
1. Подтяните свежий main и создайте сфокусированную feature-ветку.
2. Реализуйте небольшими логичными коммитами с ясными сообщениями.
3. Перед пушем rebase на main, чтобы держать историю чистой.
4. Откройте PR, прогоните CI и учтите фидбек ревью.
5. После зелёного CI мержите через squash; удалите ветку.
6. При конфликтах понимайте обе стороны до решения.
7. Для восстановления после случайных reset используйте `git reflog`.
8. Держите `main` зелёным; тегируйте релизы для трассируемости.

## Валидация
1. История линейна и читаема (`git log --graph`)
2. Каждый коммит собирается и проходит тесты
3. В истории нет секретов и больших файлов
4. PR небольшие и сфокусированные
5. `main` всегда в релизабельном состоянии

## Устранение неполадок
- Путаница с конфликтами: возьмите обе стороны, аккуратно отредактируйте, затем `git add` + commit.
- Случайный reset: `git reflog` найдите коммит и `git reset --hard <sha>`.
- Push rejected: rebase на удалённую ветку, затем `--force-with-lease`.