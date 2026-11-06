---
name: ai-coder-career-architect
description: "Accelerates AI-Native Developer, DevOps, and Platform Engineer careers with XYZ-formula resumes, production pet-project blueprints, Senior/Staff System Design (10k+ RPS, Multi-AZ), and technical interview prep. Use for portfolio packaging, resume rewriting, and interview readiness."
category: education
tags: [career, resume, interview-prep, system-design, portfolio, education, devops]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# AI-Coder & DevOps Career Architect (XYZ & System Design)

> From passive duty lists to metric-driven XYZ resumes, production GitHub repositories, and 10k+ RPS System Design mastery.

## Quick Start
```bash
# Audit a portfolio repository for production engineering signals
test -f README.md && test -f Dockerfile && test -d .github/workflows && echo "Portfolio repository ready"
```

```markdown
<!-- XYZ Formula: Achieved [X], measured by [Y], by implementing [Z] -->
- Cut CI/CD release duration by 79% (from 24 to 5 minutes) and shrank container image size by 75% (420 MB to 35 MB) by migrating 15 microservices to multi-stage distroless builds with BuildKit caching.
- Reduced monthly cloud compute spend by 42% while maintaining 99.95% SLO availability by deploying Karpenter Spot consolidation and Argo Rollouts canary analysis.
```

## When to Use
- Rewriting passive engineering resumes into high-converting, ATS-friendly bullets using the Google XYZ impact formula
- Designing 1-2 deep production portfolio repositories on GitHub instead of dozens of shallow tutorial clones
- Preparing for Middle, Senior, or Staff technical interviews across Linux, Kubernetes, CI/CD, Databases, and Incident Response
- Structuring 45-minute Highload System Design interviews (10k+ RPS, Multi-AZ, RTO/RPO, Cache-Aside, Kafka spike smoothing, Outbox)

## Best Practices
- Write every resume bullet with the XYZ structure: start with an active past-tense verb, state the percentage/time/cost impact, and name the exact stack.
- Include an architecture diagram (Mermaid or ASCII), a 3-command Quick Start, and green CI badges at the top of every portfolio README.
- Start every System Design session by clarifying functional requirements, traffic shape (read/write RPS), and target SLO/RTO/RPO before drawing boxes.
- Design every production layer with zero Single Points of Failure (SPOF): multi-AZ stateless pods, Redis Cache-Aside with jittered TTLs, and HA CloudNativePG.
- Use the transactional Outbox pattern whenever a service must atomically update PostgreSQL and publish an event to Kafka.
- Practice hands-on troubleshooting drills (break-my-cluster.yaml) so live debugging rounds are solved systematically in under 10 minutes.

## Dependencies
```bash
# Verify portfolio repo hygiene with Gitleaks and Ruff
gitleaks detect --source . -v
python3 -m ruff check .
```

## Examples
```python
# Score a resume bullet for XYZ completeness (action verb, numeric metric, and technical mechanism)
import re

def score_xyz_bullet(bullet: str) -> dict:
    has_metric = bool(re.search(r"\b\d+(\.\d+)?(%|x|ms|s|m|min|hr|MB|GB|TB|RPS|SLO)\b", bullet))
    has_mechanism = bool(re.search(r"\b(by|via|using|through|за счет|путем|внедрив)\b", bullet, flags=re.I))
    words = len(bullet.split())
    return {"has_metric": has_metric, "has_mechanism": has_mechanism, "word_count": words, "valid_xyz": has_metric and has_mechanism and 14 <= words <= 45}

assert score_xyz_bullet("Cut CI build time by 79% (from 24m to 5m) by implementing BuildKit layer caching.")["valid_xyz"]
```

```markdown
# 45-Minute System Design Interview Blueprint (10,000+ RPS)
1. Requirements (5m): Read/Write ratio (80/20), peak 30k RPS, SLO 99.95%, RPO = 0, RTO < 30s.
2. Edge & Ingress (5m): GeoDNS + CDN/WAF -> L4/L7 Load Balancers -> Gateway API (Cilium Envoy).
3. Stateless Compute (10m): K8s pods across 3 AZs with topologySpreadConstraints, HPA/KEDA, and Karpenter.
4. Caching & Async Queues (10m): Redis/Valkey Cache-Aside (jittered TTL) + Kafka KRaft for write spike smoothing.
5. Stateful Storage & DR (15m): CloudNativePG (1 Primary + 2 Sync/Quorum Replicas) via PgBouncer + WAL-G S3 PITR.
```

## Step-by-Step
1. Audit every bullet in your resume with score_xyz_bullet() and replace vague duty statements with quantified XYZ outcomes.
2. Select 1-2 flagship GitHub repositories and add bilingual READMEs, architecture diagrams, multi-stage Dockerfiles, and CI workflows.
3. Deploy a live demo or static documentation portal that passes the Vibe-SEO and Zero-CLS checks.
4. Review the 5 core technical interview blocks: Linux internals (curl lifecycle, D-state, lsof), Containers/K8s, CI/CD & OIDC/IaC, DB locks/replication, and Incident Playbooks.
5. Rehearse the 5-step System Design framework for 10k+ RPS services, calculating network bandwidth, IOPS, and RTO/RPO explicitly.
6. Complete the 4 Chaos Drill troubleshooting scenarios so you can narrate root-cause isolation calmly during live interviews.

## Validation
1. 100% of resume experience bullets pass score_xyz_bullet() with concrete metrics and mechanisms
2. Flagship GitHub repositories have passing CI workflows, zero leaked secrets, and a 3-command local startup
3. Candidate can explain end-to-end request flow, SPOF mitigation, Outbox consistency, and RTO/RPO for a 10k+ RPS architecture

## Troubleshooting
- Resume gets filtered out before human review — ensure exact keyword alignment with job description stack (Kubernetes, OpenTofu, Prometheus, Python, Go) inside XYZ bullets.
- No exact business dollar metrics available — use engineering metrics you directly control: build duration (min), image size (MB), p99 latency (ms), MTTR (min), or test coverage (%).
- Running out of time in System Design interviews — spend no more than 5 minutes on requirements and jump straight to the high-level Edge -> Compute -> Cache/Queue -> DB data flow.
- Cache stampede when popular Redis key expires under 10k RPS — add random TTL jitter and request coalescing (singleflight) in the backend service.
