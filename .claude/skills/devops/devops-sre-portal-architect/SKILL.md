---
name: devops-sre-portal-architect
description: "Designs and generates 2026-2027 DevOps, SRE, Platform Engineering, and AI/GPU infrastructure roadmaps, production Kubernetes/bare-metal manifests, chaos troubleshooting labs, and AI-Coder learning-to-career portal modules. Use for curriculum design, platform blueprints, and SRE competency matrices."
category: devops
tags: [devops, sre, platform-engineering, roadmaps, kubernetes, chaos-engineering, ai-infra]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# DevOps & SRE Portal Architect

> Progressive competency tracks from Linux internals to bare-metal Talos, GPU inference, and chaos drills.

## Quick Start
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

## When to Use
- Structuring Junior-to-Principal DevOps, SRE, Platform Engineering, and AI/LLMOps roadmaps (Maps 01-23)
- Pairing infrastructure theory with runnable Kubernetes manifests, Go operators, and Chaos Drill troubleshooting labs
- Building or updating the AI-Coder Learning, Practice, and Career Portal on top of ssrjkk/agent-skills
- Designing System Design architectures (10k+ RPS, Multi-AZ) and ATS-ready XYZ resume achievements

## Best Practices
- Organize learning stages progressively: Foundation (01-03), Cloud-Native & SRE (04-13), Principal & AI-Infra (14-20), and Vibe-Coding/MCP/SEO (21-23).
- Never recommend deprecated patterns for new deployments: use Kafka KRaft instead of ZooKeeper, Cilium eBPF instead of sidecar-heavy meshes, and OIDC federation instead of static CI keys.
- Pair every roadmap stage with a concrete artifact: a hardened YAML manifest, a Go reconciler, a Dagger pipeline, or a chaos verification script.
- Keep English and Russian roadmap stages 1-to-1 in item count so validate_roadmaps.py passes without drift.
- Connect technical mastery directly to career outcomes (Learn -> Build -> Get Hired) using verifiable GitHub portfolio blueprints.
- Enforce SSR/prerendering and Open Graph metadata on all generated portal pages so search engines index every track.

## Dependencies
```bash
# Core validation and site generation tools
python3 -m pip install -e ".[dev]"
python3 scripts/validate_roadmaps.py
```

## Examples
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

## Step-by-Step
1. Audit existing tracks in roadmaps/*.json and skills in .claude/skills/ to identify coverage gaps.
2. Map competencies across the 4 progressive tiers: Foundation, Cloud-Native/SRE, Principal/AI-Infra, and Vibe-Coding/Portal.
3. Draft bilingual stage titles (title, title_ru) and 1-to-1 item lists (items, items_ru) with concrete tools and metrics.
4. Link existing catalog skills in related_skills and set catalog_domain to a valid domain from skills_catalog.json.
5. Bundle hands-on labs (break-my-cluster.yaml, verify-fixes.sh, vLLM and CloudNativePG manifests) alongside the tracks.
6. Run python scripts/validate_roadmaps.py and python scripts/build_docs.py to regenerate the bilingual portal.
7. Verify that README.md and docs/roadmaps.html reflect the updated live roadmap counts.

## Validation
1. python scripts/validate_roadmaps.py reports 0 errors and confirms all live tracks have full RU mirrors
2. Every skill listed in related_skills exists in skills_catalog.json
3. python scripts/check_site_consistency.py passes across all generated HTML pages
4. All accompanying Kubernetes, Go, and Python lab files pass syntax and schema validation

## Troubleshooting
- items_ru length mismatch error — ensure every English item in a stage has a corresponding Russian item at the exact same index.
- Unknown related_skills failure — run python -m claude_skills.cli catalog before validating roadmaps so new skills are indexed.
- Unknown catalog_domain failure — verify the domain has at least one skill in .claude/skills/<domain>/ or set catalog_domain to null.
- Russian header not toggling on roadmaps.html — confirm both name_ru and tagline_ru are populated on the live track JSON.
