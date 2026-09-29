# Claude Models Compatibility Matrix

## Quick Reference

|Model|Speed|Context Window|Best For|
|-------|:-----:|:--------------:|----------|
|**Haiku**|Fastest|200K tokens|Simple, repetitive tasks, quick code gen|
| **Sonnet**|Balanced|200K tokens|**Most skills** (recommended default)|
|**Opus**|Most powerful|200K tokens|Complex reasoning, architecture, security|

## Skill Coverage by Model

All **100 skills** across **16 domains** are tested with **Sonnet** and **Opus**.

|Domain|Skills|Sonnet|Opus|
|--------|:-----:|:------:|:----:|
|DevOps|19||||
|AI|15||||
|Backend|14||||
|Frontend|10||||
|Database|8||||
|Data|7||||
|Engineering|7||||
|Security|4||||
|Mobile|4||||
|QA|3||||
|Finance|2||||
|Gamedev|2||||
|Healthcare|2||||
|Blockchain|1||||
|Desktop|1||||
|Embedded|1||||

> Full support · No recommendation

## Recommendations

|Use Case|Recommended Model|
|----------|:-----------------:|
|Daily development, CRUD, scripting|**Sonnet**|
|Complex architecture, system design|**Opus**|
|Simple automation, file operations|**Haiku**|
|Security audits, penetration testing|**Opus**|
|Smart contract development|**Opus**|
|ML pipeline design|**Opus**|
|Quick code snippets, bash scripts|**Haiku**|

## Model Notes

- Most skills declare `models: [sonnet, opus]`; newer skills also declare
  `gpt-5`, `gemini-2.5`, and `glm-4.6` for cross-provider portability.
- `ai/llm-finetuning` is **Opus-only** (full fine-tuning runs benefit from the
  strongest reasoning model).
- No skill in the curated library declares Haiku support.

---

*Last updated: 2026-09-29*