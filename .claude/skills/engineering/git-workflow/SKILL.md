---
name: git-workflow
description: "Use Git effectively: branching, commits, rebase vs merge, history hygiene, conflict resolution, and collaboration workflows. Use for any git-based project."
category: engineering
tags: [git, github, branching, rebase, merge, commits, collaboration, vcs]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-25
updated: 2026-09-28
author: ssrjkk
---
# Git Workflow

> Using Git effectively for clean history and smooth collaboration.

## Quick Start
```bash
git clone <repo>
git checkout -b feat/my-feature
# ... work, commit ...
git push -u origin feat/my-feature
```

## When to Use
- Every software project (or even docs and config)
- Working with branches and pull requests
- Recovering from mistakes safely
- Auditing who changed what and when

## Best Practices

### Branching
- Use feature branches off main; keep them short-lived
- Follow a naming convention: `feat/`, `fix/`, `docs/`, `chore/`
- Sync with main regularly (`git fetch && git rebase`)
- Delete merged branches

### Commits
- Commit small, focused changes with clear messages
- Follow conventional commits: `feat:`, `fix:`, `refactor:`
- Explain the "why" in the body when needed
- Never commit secrets or large binaries

### History
- Prefer rebase for local cleanup; merge for shared integration
- Squash WIP commits before merging
- Use `git log --oneline --graph` to review
- Avoid rewriting pushed history on shared branches

### Collaboration
- Pull with rebase to keep history linear
- Resolve conflicts by understanding both sides
- Use `git stash` for interruptions
- Keep `main` always green and releasable

## Dependencies
```bash
# Git 2.40+ recommended
git --version
# Optional: GitHub CLI for PRs
gh --version
```

## Examples
```bash
# Start a feature branch and commit well
git switch -c feat/user-auth
git add src/ tests/
git commit -m "feat: add user authentication

Adds email/password login with JWT issuance."
```
```bash
# Rebase onto latest main
git fetch origin
git rebase origin/main
git push --force-with-lease
```
```bash
# Undo safely
git restore src/          # discard working changes
git reset --soft HEAD~1   # undo commit, keep changes
git revert <sha>          # safe undo on shared history
```
```bash
# Inspect history
git log --oneline --graph -15
git show <sha>
git diff HEAD~1
```

## Step-by-Step
1. Pull the latest main and create a focused feature branch.
2. Implement in small, logical commits with clear messages.
3. Rebase onto main before pushing to keep history clean.
4. Open a PR, run CI, and address review feedback.
5. Merge with squash once green; delete the branch.
6. On conflicts, understand both sides before resolving.
7. Use `git reflog` to recover from accidental resets.
8. Keep `main` green; tag releases for traceability.

## Validation
1. History is linear and readable (`git log --graph`)
2. Every commit builds and passes tests
3. No secrets or large files in history
4. PRs are small and focused
5. `main` is always in a releasable state

## Troubleshooting
- Conflict confusion: fetch both sides, edit carefully, then `git add` + commit.
- Accidentally reset: `git reflog` to find the commit and `git reset --hard <sha>`.
- Push rejected: rebase onto the remote branch, then `--force-with-lease`.