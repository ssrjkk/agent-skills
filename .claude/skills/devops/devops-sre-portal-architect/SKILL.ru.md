---
name: devops-sre-portal-architect
description: "Designs and generates 2026-2027 DevOps, SRE, Platform Engineering, and AI/GPU infrastructure roadmaps, production Kubernetes/bare-metal manifests, chaos troubleshooting labs, and AI-Coder learning-to-career portal modules. Use for curriculum design, platform blueprints, and SRE competency matrices."
category: devops
tags: [devops, sre, platform-engineering, roadmaps, kubernetes, chaos-engineering, ai-infra]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
language: ru
original: devops-sre-portal-architect
author: ssrjkk
---
# DevOps & SRE Portal Architect (Архитектор карт и портала DevOps/SRE)

> Сквозные матрицы компетенций от ядра Linux до bare-metal Talos, GPU-инференса и полигонов траблшутинга.

## Быстрый старт
```bash
# Validate all roadmap tracks and skill definitions in the repository
python scripts/validate_roadmaps.py
python -m claude_skills.cli validate --dir .claude/skills
```

```python
# Check roadmap track coverage and live stage counts
import json
from pathlib import Path

tracks = [json.loads(p.read_text(encoding="utf-8")) for p in Path("roadmaps").glob("*.json")]
live = [t["slug"] for t in tracks if t.get("status") == "live"]
print(f"Live tracks ({len(live)}/{len(tracks)}): {live}")
```

## Когда использовать
- Проектирование дорожных карт DevOps, SRE, Platform Engineering и AI/LLMOps от Junior до Principal (карты 01–23)
- Связывание теории с боевыми манифестами Kubernetes, операторами на Go и полигонами Chaos Drill
- Развитие образовательно-карьерного портала для AI-кодеров на базе репозитория ssrjkk/agent-skills
- Подготовка архитектур System Design (10k+ RPS, Multi-AZ) и резюме по метрической формуле XYZ

## Лучшие практики
- Стройте треки от фундамента к архитектуре: База (01–03), Cloud-Native и SRE (04–13), Principal и AI-Infra (14–20), Вайбкодинг/MCP/SEO (21–23).
- Исключайте устаревшие паттерны в новых проектах: используйте Kafka KRaft вместо ZooKeeper, Cilium eBPF вместо тяжелых sidecar-сеток и OIDC вместо статических ключей в CI.
- Привязывайте каждый этап карты к проверяемому артефакту: манифесту K8s, оператору на Go, конвейеру Dagger или скрипту проверки аварии.
- Держите строгое соответствие 1-к-1 между массивами items и items_ru в roadmaps/*.json для прохождения гейта validate_roadmaps.py.
- Соединяйте обучение с наймом по формуле Учись -> Строй -> Выходи на оффер через эталонные пет-проекты.
- Обеспечивайте SSR/пререндер и разметку Open Graph на всех страницах портала для полной индексации поисковиками.

## Зависимости
```bash
# Core validation and site generation tools
python3 -m pip install -e ".[dev]"
python3 scripts/validate_roadmaps.py
```

## Примеры
```json
{
  "$schema": "../roadmaps.schema.json",
  "slug": "devops",
  "name": "DevOps & SRE",
  "name_ru": "DevOps и SRE",
  "icon": "🚀",
  "tagline": "From Linux kernel and eBPF to Talos bare-metal, vLLM GPU clusters, and SRE chaos drills",
  "tagline_ru": "От ядра Linux и eBPF до bare-metal Talos, GPU-кластеров vLLM и SRE траблшутинга",
  "status": "live",
  "eta": "2026-11",
  "catalog_domain": "devops"
}
```

```python
# Verify 1-to-1 bilingual parity across all stages of a roadmap track
import json
from pathlib import Path

track = json.loads(Path("roadmaps/devops.json").read_text(encoding="utf-8"))
for idx, stage in enumerate(track["stages"]):
    assert len(stage["items"]) == len(stage["items_ru"]), f"Mismatch at stage {idx}"
    assert len(stage["items"]) >= 2
print(f"Verified {len(track['stages'])} bilingual stages successfully.")
```

## Пошаговое руководство
1. Проведите ревизию текущих треков в roadmaps/*.json и навыков в .claude/skills/ для выявления пробелов.
2. Распределите темы по 4 уровням: Фундамент, Cloud-Native и SRE, Principal и AI-Infra, Вайбкодинг и Карьера.
3. Составьте двуязычные заголовки этапов (title, title_ru) и зеркальные списки пунктов (items, items_ru) с конкретным стеком.
4. Привяжите связанные скиллы в поле related_skills и укажите валидный catalog_domain из каталога.
5. Приложите практические лабораторные стенды (break-my-cluster.yaml, verify-fixes.sh, манифесты vLLM и CloudNativePG).
6. Запустите python scripts/validate_roadmaps.py и python scripts/build_docs.py для пересборки двуязычного сайта.
7. Проверьте обновление счетчиков живых карт в README.md и docs/roadmaps.html.

## Валидация
1. Скрипт python scripts/validate_roadmaps.py завершается с 0 ошибок и подтверждает полноту RU-зеркал
2. Каждый скилл из списка related_skills присутствует в skills_catalog.json
3. Проверка python scripts/check_site_consistency.py проходит по всем сгенерированным HTML-страницам
4. Все сопутствующие лабораторные манифесты Kubernetes, Go и Python проходят проверку синтаксиса

## Устранение неполадок
- Ошибка несовпадения длины items_ru — проверьте, что каждому пункту в items соответствует перевод в items_ru на той же позиции.
- Ошибка unknown related_skills — сначала обновите каталог командой python -m claude_skills.cli catalog, чтобы новые скиллы попали в индекс.
- Ошибка unknown catalog_domain — убедитесь, что в папке .claude/skills/<domain>/ есть хотя бы один скилл, либо укажите null.
- Не переключается шапка трека на русский язык — проверьте наличие полей name_ru и tagline_ru в корне JSON-файла карты.
