#!/usr/bin/env python3
"""Generate a premium multi-page catalog site from skills.

Pages:
  index.html          - landing with hero, dashboard, search, filters, cards
  skills/<name>.html  - a full page per skill
  domains/<name>.html - a page per domain listing its skills
"""

from __future__ import annotations

import html as html_lib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://ssrjkk.github.io/agent-skills/"
REPO = "https://github.com/ssrjkk/agent-skills"

DOMAIN_COLORS = {
    "ai": "#8b5cf6",
    "backend": "#0ea5e9",
    "blockchain": "#f59e0b",
    "data": "#10b981",
    "database": "#14b8a6",
    "desktop": "#6366f1",
    "devops": "#f43f5e",
    "embedded": "#84cc16",
    "engineering": "#a855f7",
    "finance": "#eab308",
    "frontend": "#3b82f6",
    "gamedev": "#ef4444",
    "healthcare": "#06b6d4",
    "mobile": "#ec4899",
    "qa": "#22c55e",
    "security": "#dc2626",
}

MODEL_ORDER = ["opus", "sonnet", "gpt-6", "gemini-3", "glm-5", "haiku"]


def esc(s: str) -> str:
    return html_lib.escape(s, quote=True)


def read_catalog(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def skill_metrics(name: str, path_str: str) -> dict:
    en_path = Path(path_str)
    if not en_path.exists():
        return {"score": 100, "lines": 0, "blocks": 0, "sections": 0, "preview": ""}
    text = en_path.read_text(encoding="utf-8")
    lines = text.count("\n") + 1
    blocks = text.count("```") // 2
    sections = text.count("\n## ")
    # extract a code preview: first fenced block, up to 6 lines
    m = re.search(r"```[a-zA-Z0-9]*\n(.*?)```", text, re.DOTALL)
    preview = ""
    if m:
        code = m.group(1)
        preview = "\n".join(code.splitlines()[:6])
    score = 100
    if blocks < 4:
        score -= 10
    if lines < 90:
        score -= 10
    if sections < 7:
        score -= 5
    return {"score": max(0, score), "lines": lines, "blocks": blocks, "sections": sections, "preview": preview}


def load_all(path: Path) -> tuple[dict, dict, dict]:
    data = read_catalog(path)
    meta = data["metadata"]
    skills = data["skills"]
    metrics = {}
    by_category: dict[str, list] = {}
    for s in skills:
        metrics[s["name"]] = skill_metrics(s["name"], s["path"])
        by_category.setdefault(s["category"], []).append(s)
    return meta, skills, metrics


def page_head(title: str, desc: str, canonical: str, extra: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{REPO}/raw/main/.github/social-preview.svg">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2220%22 fill=%22%238b5cf6%22/><text x=%2250%22 y=%2268%22 font-size=%2250%22 text-anchor=%22middle%22 fill=%22white%22 font-family=%22Arial%22>S</text></svg>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
  {extra}
</head>
<body data-theme="dark">
  <div class="bg-glow" aria-hidden="true"></div>
  <nav class="nav">
    <div class="nav-inner">
      <a class="nav-brand" href="../index.html"><span class="nav-logo">S</span><span class="nav-name">Agent&nbsp;Skills</span></a>
      <div class="nav-right">
        <a class="nav-link" href="../index.html#catalog">Catalog</a>
        <a class="nav-link" href="../index.html#dashboard">Stats</a>
        <a class="nav-link" href="{REPO}">GitHub</a>
        <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">🌙</button>
      </div>
    </div>
  </nav>
  <div class="container">
"""


def page_foot() -> str:
    return """  </div>
  <div class="toast" id="toast"></div>
  <script>
  function copyText(text) {
    navigator.clipboard.writeText(text).then(function() { showToast('Copied: ' + text); });
  }
  function copySkill(name) { copyText('.claude/skills/' + name); }
  function showToast(msg) {
    var t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(t._timer);
    t._timer = setTimeout(function() { t.classList.remove('show'); }, 1800);
  }
  function toggleTheme() {
    var b = document.body;
    var next = b.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    b.setAttribute('data-theme', next);
    var btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = next === 'dark' ? '🌙' : '☀️';
  }
  </script>
</body>
</html>"""


def build_index_html(catalog_path: Path, output_dir: Path) -> str:
    meta, skills, metrics = load_all(catalog_path)

    model_names = set()
    for s in skills:
        model_names.update(s.get("models", []))
    ordered_models = [m for m in MODEL_ORDER if m in model_names] + sorted(model_names - set(MODEL_ORDER))
    models_badges = "".join(f'<span class="model-badge">{esc(m)}</span>' for m in ordered_models)

    by_category: dict[str, list] = {}
    for s in skills:
        by_category.setdefault(s["category"], []).append(s)

    domain_pills = []
    for domain in sorted(by_category):
        color = DOMAIN_COLORS.get(domain, "#64748b")
        domain_pills.append(
            f'<button class="pill" data-domain="{esc(domain)}" style="--dc:{color}" onclick="filterByDomain(\'{esc(domain)}\', this)">'
            f'{esc(domain)}<span class="pill-count">{len(by_category[domain])}</span></button>'
        )

    # dashboard bars by domain
    max_count = max(len(v) for v in by_category.values()) if by_category else 1
    dash_rows = []
    for domain in sorted(by_category, key=lambda d: -len(by_category[d])):
        color = DOMAIN_COLORS.get(domain, "#64748b")
        n = len(by_category[domain])
        pct = int(n / max_count * 100)
        dash_rows.append(
            f'<div class="dash-row"><span class="dash-name">{esc(domain)}</span>'
            f'<div class="dash-bar"><div class="dash-fill" style="width:{pct}%;background:{color}"></div></div>'
            f'<span class="dash-count">{n}</span></div>'
        )

    cards = []
    for s in sorted(skills, key=lambda x: (x["category"], x["name"])):
        color = DOMAIN_COLORS.get(s["category"], "#64748b")
        tags = s.get("tags", [])[:3]
        tag_html = "".join(f'<span class="tag">{esc(t)}</span>' for t in tags)
        ru_badge = '<span class="ru-badge">RU</span>' if s.get("has_ru") else ""
        m = metrics[s["name"]]
        score = m["score"]
        bar_color = "#22c55e" if score >= 95 else "#f59e0b" if score >= 85 else "#ef4444"
        preview = esc(m["preview"])
        if preview:
            preview_html = f'<pre class="card-code"><code>{preview}</code></pre>'
        else:
            preview_html = ""
        cards.append(
            f'<a class="card" href="skills/{esc(s["name"])}.html" data-name="{esc(s["name"].lower())}" '
            f'data-domain="{esc(s["category"].lower())}" data-score="{score}" '
            f'data-tags=\'{esc(" ".join(s.get("tags", [])).lower())}\'>'
            f'<div class="card-top"><span class="card-name">{esc(s["name"])}</span>{ru_badge}</div>'
            f'<div class="card-desc">{esc(s["description"])}</div>'
            f'{preview_html}'
            f'<div class="card-score"><div class="score-row"><span>Quality</span><strong>{score}%</strong></div>'
            f'<div class="bar"><div class="bar-fill" style="width:{score}%;background:{bar_color}"></div></div></div>'
            f'<div class="card-meta"><span>{m["blocks"]} blocks</span><span>{m["sections"]} sections</span><span>{m["lines"]} lines</span></div>'
            f'<div class="card-tags">{tag_html}</div>'
            f'<div class="card-domain" style="color:{color}">{esc(s["category"])}</div>'
            "</a>"
        )

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    html_doc = page_head(
        "Agent Skills Library — 100 curated bilingual skills",
        "100 curated bilingual (EN + RU) skills in the universal Agent Skills format for Claude Code, OpenCode, Cursor, Windsurf and every LLM/GLM agent.",
        BASE,
        '<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"Agent Skills Library","url":"' + BASE + '"}</script>',
    ) + f"""
    <header class="hero">
      <div class="hero-badge">Universal Agent Skills Format</div>
      <h1>Agent Skills <span class="gradient">Library</span></h1>
      <p class="hero-sub">Curated bilingual (EN + RU) skills for Claude Code, OpenCode, Cursor, Windsurf and every Agent Skills–compatible agent.</p>
      <div class="hero-models">Models: {models_badges}</div>
      <div class="hero-cta">
        <a class="btn-primary" href="#catalog">Browse skills</a>
        <button class="btn-ghost" onclick="copyText('pip install agent-skills-library')">pip install agent-skills-library</button>
      </div>
    </header>

    <section class="stats" aria-label="Library statistics">
      <div class="stat"><span class="stat-num" data-count="{meta["total_skills"]}">0</span><span class="stat-label">Skills</span></div>
      <div class="stat"><span class="stat-num" data-count="{meta["total_ru"]}">0</span><span class="stat-label">Russian</span></div>
      <div class="stat"><span class="stat-num" data-count="{len(meta["domains"])}">0</span><span class="stat-label">Domains</span></div>
      <div class="stat"><span class="stat-num">100%</span><span class="stat-label">Quality</span></div>
    </section>

    <section class="install" id="install">
      <div class="install-header"><h2>Install in one line</h2></div>
      <div class="install-box">
        <code>curl -fsSL https://raw.githubusercontent.com/ssrjkk/agent-skills/main/install.sh | bash</code>
        <button class="copy-btn" onclick="copyText('curl -fsSL https://raw.githubusercontent.com/ssrjkk/agent-skills/main/install.sh | bash')">copy</button>
      </div>
      <div class="install-links">
        <a href="skills_catalog.json" download>Download catalog (JSON)</a> ·
        <a href="skills_catalog.schema.json" download>JSON Schema</a> ·
        <a href="{REPO}">GitHub</a>
      </div>
    </section>

    <section class="dashboard" id="dashboard">
      <h2>Distribution by domain</h2>
      <div class="dash-list">
        {"".join(dash_rows)}
      </div>
    </section>

    <section class="search-section" id="catalog">
      <div class="search-row">
        <input type="search" id="search" class="search" placeholder="Search skills by name, domain, or tag…" autocomplete="off" oninput="onSearch(this.value)">
        <select id="sort" class="sort" onchange="applyFilter()">
          <option value="domain">Sort: domain</option>
          <option value="name">Sort: name</option>
          <option value="score" selected>Sort: quality (high→low)</option>
        </select>
      </div>
      <div class="pills" id="pills">
        <button class="pill active" data-domain="all" onclick="filterByDomain('all', this)">all<span class="pill-count">{meta["total_skills"]}</span></button>
        {"".join(domain_pills)}
      </div>
    </section>

    <section class="results">
      <div class="cards" id="cards">
        {"".join(cards)}
      </div>
      <div class="empty" id="empty" hidden>No skills match your search.</div>
    </section>

    <footer>
      <p>Generated on {generated} · {meta["total_skills"]} skills · {len(meta["domains"])} domains</p>
      <p><a href="{REPO}">GitHub</a> · <a href="{REPO}/issues">Report Issue</a> · <a href="{REPO}/discussions">Discussions</a></p>
    </footer>
""" + """
  <script>
  var activeDomain = 'all';
  function filterByDomain(domain, btn) {
    activeDomain = domain;
    document.querySelectorAll('.pill').forEach(function(b) { b.classList.remove('active'); });
    btn.classList.add('active');
    applyFilter();
  }
  function onSearch(q) { applyFilter(); }
  function applyFilter() {
    var q = (document.getElementById('search').value || '').toLowerCase();
    var sort = document.getElementById('sort').value;
    var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
    var visible = 0;
    cards.forEach(function(c) {
      var name = c.getAttribute('data-name');
      var domain = c.getAttribute('data-domain');
      var tags = c.getAttribute('data-tags') || '';
      var domainMatch = activeDomain === 'all' || domain === activeDomain;
      var textMatch = !q || name.includes(q) || domain.includes(q) || tags.includes(q);
      var show = domainMatch && textMatch;
      c.style.display = show ? '' : 'none';
      if (show) visible++;
    });
    cards.sort(function(a, b) {
      if (sort === 'score') return (b.getAttribute('data-score') || 0) - (a.getAttribute('data-score') || 0);
      if (sort === 'name') return a.getAttribute('data-name').localeCompare(b.getAttribute('data-name'));
      return a.getAttribute('data-domain').localeCompare(b.getAttribute('data-domain'));
    });
    var grid = document.getElementById('cards');
    cards.forEach(function(c) { grid.appendChild(c); });
    document.getElementById('empty').hidden = visible !== 0;
  }
  // animated counters
  document.querySelectorAll('.stat-num[data-count]').forEach(function(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    var start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / 900, 1);
      el.textContent = Math.round(target * p);
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = target;
    }
    requestAnimationFrame(step);
  });
  </script>
</body>
</html>"""

    (output_dir / "index.html").write_text(html_doc, encoding="utf-8")
    print(f"Index written to {output_dir / 'index.html'}")
    return html_doc


def build_skill_pages(catalog_path: Path, output_dir: Path) -> int:
    _meta, skills, metrics = load_all(catalog_path)
    skills_dir = output_dir / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    count = 0

    for s in skills:
        name = s["name"]
        cat = s["category"]
        color = DOMAIN_COLORS.get(cat, "#64748b")
        m = metrics[name]
        en_path = Path(s["path"])
        body = ""
        if en_path.exists():
            text = en_path.read_text(encoding="utf-8")
            # strip frontmatter
            parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.MULTILINE)
            if len(parts) >= 3:
                body = parts[2].strip()

        tags_html = "".join(f'<span class="tag">{esc(t)}</span>' for t in s.get("tags", []))
        models_html = "".join(f'<span class="model-badge">{esc(mod)}</span>' for mod in s.get("models", []))
        prev_name = None
        next_name = None
        domain_skills = sorted([x for x in skills if x["category"] == cat], key=lambda x: x["name"])
        for i, ds in enumerate(domain_skills):
            if ds["name"] == name:
                if i > 0:
                    prev_name = domain_skills[i - 1]["name"]
                if i < len(domain_skills) - 1:
                    next_name = domain_skills[i + 1]["name"]

        nav_html = ""
        if prev_name or next_name:
            nav_html = '<div class="page-nav">'
            if prev_name:
                nav_html += f'<a class="page-nav-link" href="{esc(prev_name)}.html">← {esc(prev_name)}</a>'
            else:
                nav_html += '<span></span>'
            if next_name:
                nav_html += f'<a class="page-nav-link" href="{esc(next_name)}.html">{esc(next_name)} →</a>'
            nav_html += "</div>"

        # render markdown-ish body: code fences, headings, lists, paragraphs
        rendered = render_skill_body(body)

        html_doc = page_head(
            f"{name} — Agent Skills Library",
            s["description"],
            BASE + f"skills/{name}.html",
        ) + f"""
    <article class="skill-page">
      <div class="skill-page-head">
        <div class="skill-page-badges">
          <span class="domain-chip" style="background:{color}1a;color:{color};border-color:{color}44">{esc(cat)}</span>
          {tags_html}
        </div>
        <h1 class="skill-page-title">{esc(name)}</h1>
        <p class="skill-page-desc">{esc(s["description"])}</p>
        <div class="skill-page-meta">
          <span>Quality <strong>{m["score"]}%</strong></span>
          <span>Code blocks <strong>{m["blocks"]}</strong></span>
          <span>Sections <strong>{m["sections"]}</strong></span>
          <span>Lines <strong>{m["lines"]}</strong></span>
          <span>RU translation <strong>{'yes' if s.get('has_ru') else 'no'}</strong></span>
        </div>
        <div class="skill-page-actions">
          <button class="copy-btn" onclick="copySkill('{esc(name)}')">copy path</button>
          <a class="btn-ghost" href="{REPO}/tree/main/.claude/skills/{esc(cat)}/{esc(name)}">view source</a>
        </div>
      </div>
      <div class="skill-page-models">Models: {models_html}</div>
      {nav_html}
      <div class="skill-page-body">
        {rendered}
      </div>
      {nav_html}
    </article>
""" + page_foot()
        (skills_dir / f"{name}.html").write_text(html_doc, encoding="utf-8")
        count += 1

    print(f"Wrote {count} skill pages to {skills_dir}")
    return count


def render_skill_body(body: str) -> str:
    """A small, safe renderer for the markdown used inside SKILL.md files."""
    out: list[str] = []
    in_fence = False
    fence_lines: list[str] = []
    in_list = False

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for line in body.splitlines():
        if line.strip().startswith("```"):
            if not in_fence:
                in_fence = True
                fence_lines = []
            else:
                in_fence = False
                close_list()
                code = esc("\n".join(fence_lines))
                out.append(f'<div class="codeblock"><pre class="code"><code>{code}</code></pre>'
                           f'<button class="copy-btn code-copy" onclick="copyText(this.parentNode.querySelector(\'code\').textContent)">copy</button></div>')
            continue
        if in_fence:
            fence_lines.append(line)
            continue
        stripped = line.strip()
        if not stripped:
            close_list()
            continue
        if stripped.startswith("### "):
            close_list()
            out.append(f"<h3>{esc(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            close_list()
            out.append(f"<h2>{esc(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            close_list()
            out.append(f"<h1>{esc(stripped[2:])}</h1>")
        elif stripped.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{esc(stripped[2:])}</li>")
        elif re.match(r"^\d+\. ", stripped):
            close_list()
            out.append(f"<p class='ordered'>{esc(stripped)}</p>")
        elif stripped.startswith(">"):
            close_list()
            out.append(f'<blockquote>{esc(stripped.lstrip("> "))}</blockquote>')
        else:
            close_list()
            out.append(f"<p>{esc(stripped)}</p>")
    close_list()
    return "\n".join(out)


def build_domain_pages(catalog_path: Path, output_dir: Path) -> int:
    _meta, skills, metrics = load_all(catalog_path)
    domains_dir = output_dir / "domains"
    domains_dir.mkdir(parents=True, exist_ok=True)
    by_category: dict[str, list] = {}
    for s in skills:
        by_category.setdefault(s["category"], []).append(s)

    count = 0
    for domain, domain_skills in sorted(by_category.items()):
        color = DOMAIN_COLORS.get(domain, "#64748b")
        rows = []
        for s in sorted(domain_skills, key=lambda x: x["name"]):
            m = metrics[s["name"]]
            rows.append(
                f'<a class="domain-skill" href="../skills/{esc(s["name"])}.html">'
                f'<span class="domain-skill-name">{esc(s["name"])}</span>'
                f'<span class="domain-skill-score">{m["score"]}%</span></a>'
            )
        html_doc = page_head(
            f"{domain} skills — Agent Skills Library",
            f"{len(domain_skills)} skills in the {domain} domain.",
            BASE + f"domains/{domain}.html",
        ) + f"""
    <article class="domain-page">
      <div class="domain-page-head">
        <span class="domain-chip" style="background:{color}1a;color:{color};border-color:{color}44">{esc(domain)}</span>
        <h1>{esc(domain)} skills</h1>
        <p>{len(domain_skills)} skills · {sum(1 for x in domain_skills if x.get('has_ru'))} with RU</p>
      </div>
      <div class="domain-list">
        {"".join(rows)}
      </div>
      <p class="back-link"><a href="../index.html">← Back to catalog</a></p>
    </article>
""" + page_foot()
        (domains_dir / f"{domain}.html").write_text(html_doc, encoding="utf-8")
        count += 1
    print(f"Wrote {count} domain pages to {domains_dir}")
    return count


def build_style_css(output_dir: Path) -> None:
    css = """:root{
  --bg:#0a0a12;--bg2:#10101c;--card:#141423;--card-hover:#1a1a2e;
  --text:#e8e8f5;--muted:#8b8ba3;--accent:#8b5cf6;--accent2:#ec4899;
  --border:rgba(255,255,255,.07);--radius:14px;
  --font:'Inter','Segoe UI',-apple-system,BlinkMacSystemFont,Roboto,sans-serif;
  --mono:'JetBrains Mono','Consolas','Menlo',monospace;
}
body[data-theme="light"]{
  --bg:#f6f7fb;--bg2:#eef0f6;--card:#ffffff;--card-hover:#fbfbff;
  --text:#16161f;--muted:#5f5f75;--border:rgba(20,20,40,.1);
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.6;min-height:100vh;overflow-x:hidden;
  -webkit-font-smoothing:antialiased;transition:background .25s,color .25s;
}
.bg-glow{
  position:fixed;inset:0;z-index:-1;pointer-events:none;
  background:
    radial-gradient(700px 400px at 12% -5%,rgba(139,92,246,.14),transparent 60%),
    radial-gradient(800px 500px at 90% 5%,rgba(236,72,153,.10),transparent 60%),
    radial-gradient(700px 700px at 50% 110%,rgba(14,165,233,.07),transparent 60%);
}
.nav{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--bg) 82%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--border)}
.nav-inner{max-width:1180px;margin:0 auto;padding:.8rem 1.5rem;display:flex;align-items:center;justify-content:space-between}
.nav-brand{display:flex;align-items:center;gap:.6rem;text-decoration:none;color:var(--text)}
.nav-logo{width:30px;height:30px;border-radius:9px;display:grid;place-items:center;font-weight:800;color:#fff;background:linear-gradient(135deg,var(--accent),var(--accent2));font-family:var(--mono)}
.nav-name{font-weight:700;letter-spacing:-.01em}
.nav-right{display:flex;align-items:center;gap:1rem}
.nav-link{color:var(--muted);text-decoration:none;font-size:.9rem;transition:color .15s}
.nav-link:hover{color:var(--text)}
.theme-toggle{background:var(--card);border:1px solid var(--border);color:var(--text);border-radius:9px;width:34px;height:34px;cursor:pointer;font-size:1rem}
.theme-toggle:hover{border-color:var(--accent)}
.container{max-width:1180px;margin:0 auto;padding:2.5rem 1.5rem 4rem}
.hero{text-align:center;padding:2.5rem 0 1.5rem}
.hero-badge{
  display:inline-block;padding:.4rem 1.1rem;border-radius:999px;font-size:.76rem;
  background:rgba(139,92,246,.12);border:1px solid rgba(139,92,246,.28);
  color:#c4b5fd;letter-spacing:.06em;margin-bottom:1.1rem;font-weight:600;text-transform:uppercase;
}
body[data-theme="light"] .hero-badge{color:#6d28d9}
.hero h1{font-size:clamp(2.6rem,5.5vw,4rem);font-weight:800;letter-spacing:-.03em;line-height:1.12}
.gradient{
  background:linear-gradient(100deg,var(--accent),var(--accent2));
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;
}
.hero-sub{max-width:620px;margin:.9rem auto 1.3rem;color:var(--muted);font-size:1.08rem;font-weight:400}
.hero-models{display:flex;flex-wrap:wrap;gap:.45rem;justify-content:center}
.model-badge{
  padding:.22rem .8rem;border-radius:999px;font-size:.72rem;font-weight:600;font-family:var(--mono);
  background:rgba(255,255,255,.05);border:1px solid var(--border);color:var(--muted);
}
.hero-cta{display:flex;gap:.8rem;justify-content:center;margin-top:1.6rem;flex-wrap:wrap}
.btn-primary{
  padding:.7rem 1.5rem;border-radius:10px;border:none;cursor:pointer;text-decoration:none;font-weight:600;font-size:.95rem;color:#fff;
  background:linear-gradient(100deg,var(--accent),var(--accent2));transition:opacity .15s,transform .15s;display:inline-block;
}
.btn-primary:hover{opacity:.88;transform:translateY(-1px)}
.btn-ghost{
  padding:.7rem 1.5rem;border-radius:10px;border:1px solid var(--border);cursor:pointer;text-decoration:none;font-weight:600;font-size:.95rem;color:var(--text);
  background:var(--card);transition:border-color .15s;display:inline-block;
}
.btn-ghost:hover{border-color:var(--accent)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1rem;margin:2rem 0}
.stat{
  background:var(--card);border:1px solid var(--border);border-radius:var(--radius);
  padding:1.4rem 1rem;text-align:center;transition:transform .2s,border-color .2s;
}
.stat:hover{transform:translateY(-3px);border-color:rgba(139,92,246,.35)}
.stat-num{display:block;font-size:2rem;font-weight:800;letter-spacing:-.02em;background:linear-gradient(90deg,var(--accent),var(--accent2));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.stat-label{color:var(--muted);font-size:.8rem;text-transform:uppercase;letter-spacing:.08em}
.install{margin:1.5rem 0}
.install-header h2{font-size:1.25rem;margin-bottom:.9rem;letter-spacing:-.01em}
.install-box{
  display:flex;align-items:center;gap:.7rem;background:color-mix(in srgb,var(--card) 70%,transparent);
  border:1px solid var(--border);border-radius:12px;padding:.8rem 1rem;flex-wrap:wrap;
}
.install-box code{color:#22c55e;font-size:.86rem;font-family:var(--mono);flex:1;min-width:200px;overflow-x:auto}
.copy-btn{
  background:linear-gradient(90deg,var(--accent),var(--accent2));color:#fff;border:none;
  padding:.45rem 1rem;border-radius:8px;cursor:pointer;font-size:.78rem;font-weight:600;transition:opacity .15s;
}
.copy-btn:hover{opacity:.85}
.install-links{margin-top:.6rem;font-size:.82rem;color:var(--muted)}
.install-links a{color:var(--accent);text-decoration:none}
.install-links a:hover{text-decoration:underline}
.dashboard{margin:2.5rem 0}
.dashboard h2{font-size:1.4rem;margin-bottom:1rem;letter-spacing:-.01em}
.dash-list{display:flex;flex-direction:column;gap:.5rem}
.dash-row{display:grid;grid-template-columns:130px 1fr 40px;gap:.8rem;align-items:center}
.dash-name{font-family:var(--mono);font-size:.85rem;color:var(--muted);text-transform:capitalize}
.dash-bar{height:18px;border-radius:6px;background:rgba(255,255,255,.05);overflow:hidden;border:1px solid var(--border)}
.dash-fill{height:100%;border-radius:6px;transition:width .6s ease;min-width:4px}
.dash-count{font-family:var(--mono);font-size:.85rem;text-align:right;color:var(--muted)}
.search-section{margin:2rem 0 1.5rem}
.search-row{display:flex;gap:.6rem;flex-wrap:wrap}
.search{
  flex:1;min-width:220px;padding:1rem 1.2rem;border-radius:12px;font-size:1rem;color:var(--text);
  background:var(--card);border:1px solid var(--border);outline:none;transition:border-color .2s,box-shadow .2s;
}
.search:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(139,92,246,.16)}
.sort{
  padding:1rem 1.1rem;border-radius:12px;font-size:.88rem;color:var(--text);
  background:var(--card);border:1px solid var(--border);outline:none;cursor:pointer;font-family:var(--font);
}
.sort:hover{border-color:var(--accent)}
.pills{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1rem}
.pill{
  display:inline-flex;align-items:center;gap:.45rem;padding:.42rem .95rem;border-radius:999px;
  background:var(--card);border:1px solid var(--border);color:var(--text);cursor:pointer;
  font-size:.82rem;font-weight:500;transition:all .15s;
}
.pill:hover{border-color:var(--dc,#8b5cf6);transform:translateY(-1px)}
.pill.active{background:var(--dc,#8b5cf6);border-color:var(--dc,#8b5cf6);color:#fff}
.pill-count{font-size:.68rem;opacity:.75;background:rgba(0,0,0,.25);border-radius:999px;padding:.08rem .5rem}
.pill.active .pill-count{background:rgba(255,255,255,.25)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:1.1rem}
.card{
  position:relative;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);
  padding:1.2rem 1.25rem;transition:transform .18s,box-shadow .18s,border-color .18s;animation:rise .3s ease both;text-decoration:none;color:inherit;display:block;
}
.card:hover{transform:translateY(-4px);box-shadow:0 16px 40px rgba(0,0,0,.5);border-color:rgba(139,92,246,.35)}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.card-top{display:flex;align-items:center;justify-content:space-between;gap:.5rem}
.card-name{font-family:var(--mono);font-weight:700;font-size:.96rem;color:#d7c7ff;cursor:pointer;transition:color .15s}
body[data-theme="light"] .card-name{color:#6d28d9}
.card-name:hover{color:var(--accent)}
.ru-badge{
  font-size:.6rem;font-weight:800;letter-spacing:.05em;color:#08120a;
  background:linear-gradient(90deg,#22c55e,#84cc16);border-radius:6px;padding:.14rem .5rem;flex-shrink:0;
}
.card-desc{color:var(--muted);font-size:.85rem;margin:.55rem 0 .6rem;line-height:1.55}
.card-code{
  background:color-mix(in srgb,var(--bg2) 60%,transparent);border:1px solid var(--border);border-radius:8px;
  padding:.6rem .8rem;margin:0 0 .6rem;font-family:var(--mono);font-size:.7rem;line-height:1.45;overflow-x:auto;color:var(--muted);
}
.card-score{margin:.3rem 0 .5rem}
.score-row{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.35rem;font-size:.78rem}
.score-row span{color:var(--muted);text-transform:uppercase;letter-spacing:.06em;font-size:.66rem}
.score-row strong{color:var(--text);font-size:.88rem;font-family:var(--mono)}
.bar{height:5px;border-radius:999px;background:rgba(255,255,255,.07);overflow:hidden}
.bar-fill{height:100%;border-radius:999px;transition:width .4s ease}
.card-meta{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:.55rem;font-size:.66rem;color:var(--muted)}
.card-meta span{background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:6px;padding:.12rem .5rem;font-family:var(--mono)}
.card-tags{display:flex;flex-wrap:wrap;gap:.3rem;margin-bottom:.7rem}
.tag{
  font-size:.67rem;padding:.14rem .55rem;border-radius:6px;color:var(--muted);
  background:rgba(255,255,255,.05);border:1px solid var(--border);
}
.card-domain{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;opacity:.9}
.empty{text-align:center;color:var(--muted);padding:3rem 0;font-size:1.05rem}
footer{margin-top:3.5rem;text-align:center;color:var(--muted);font-size:.85rem}
footer p{margin:.3rem 0}
footer a{color:var(--accent);text-decoration:none}
footer a:hover{text-decoration:underline}
.toast{
  position:fixed;bottom:2rem;left:50%;transform:translateX(-50%) translateY(20px);
  background:color-mix(in srgb,var(--card) 90%,transparent);border:1px solid rgba(139,92,246,.4);color:var(--text);
  padding:.75rem 1.4rem;border-radius:10px;font-size:.85rem;opacity:0;pointer-events:none;
  transition:opacity .25s,transform .25s;z-index:100;box-shadow:0 12px 40px rgba(0,0,0,.6);
  max-width:90vw;
}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
/* skill pages */
.skill-page{max-width:900px;margin:0 auto}
.skill-page-head{padding:1.5rem 0 1rem}
.skill-page-badges{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center}
.domain-chip{
  display:inline-block;padding:.28rem .9rem;border-radius:999px;font-size:.78rem;font-weight:600;text-transform:uppercase;letter-spacing:.06em;border:1px solid;
}
.skill-page-title{font-size:2.4rem;font-weight:800;letter-spacing:-.02em;margin:.8rem 0 .4rem}
.skill-page-desc{color:var(--muted);font-size:1.05rem;max-width:720px}
.skill-page-meta{display:flex;flex-wrap:wrap;gap:1.2rem;margin:1rem 0;font-size:.85rem;color:var(--muted)}
.skill-page-meta strong{color:var(--text);font-family:var(--mono)}
.skill-page-actions{display:flex;gap:.7rem;margin:1rem 0}
.skill-page-models{display:flex;gap:.45rem;flex-wrap:wrap;margin:0 0 1.5rem;align-items:center}
.page-nav{display:flex;justify-content:space-between;gap:1rem;margin:1.2rem 0}
.page-nav-link{color:var(--accent);text-decoration:none;font-size:.9rem}
.page-nav-link:hover{text-decoration:underline}
.skill-page-body h1{font-size:1.7rem;margin:1.6rem 0 .7rem}
.skill-page-body h2{font-size:1.4rem;margin:1.5rem 0 .6rem;letter-spacing:-.01em}
.skill-page-body h3{font-size:1.1rem;margin:1.2rem 0 .5rem}
.skill-page-body p{margin:.5rem 0;color:var(--text)}
.skill-page-body ul{margin:.5rem 0 .5rem 1.2rem}
.skill-page-body li{margin:.25rem 0}
.skill-page-body blockquote{border-left:3px solid var(--accent);padding-left:1rem;color:var(--muted);margin:.8rem 0;font-style:italic}
.skill-page-body .ordered{margin:.3rem 0;color:var(--text)}
.codeblock{position:relative;margin:1rem 0;background:color-mix(in srgb,var(--bg2) 70%,transparent);border:1px solid var(--border);border-radius:10px;overflow:hidden}
.code{display:block;padding:1rem;overflow-x:auto;font-family:var(--mono);font-size:.8rem;line-height:1.5;color:var(--text)}
.code-copy{position:absolute;top:.5rem;right:.5rem;font-size:.68rem;padding:.25rem .7rem}
/* domain pages */
.domain-page{max-width:900px;margin:0 auto}
.domain-page-head{padding:1.5rem 0 1rem}
.domain-page-head h1{font-size:2.2rem;font-weight:800;margin:.7rem 0 .3rem}
.domain-page-head p{color:var(--muted)}
.domain-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:.7rem;margin:1.5rem 0}
.domain-skill{
  display:flex;justify-content:space-between;align-items:center;gap:.6rem;padding:.8rem 1rem;
  background:var(--card);border:1px solid var(--border);border-radius:10px;text-decoration:none;color:inherit;transition:border-color .15s,transform .15s;
}
.domain-skill:hover{border-color:rgba(139,92,246,.35);transform:translateY(-2px)}
.domain-skill-name{font-family:var(--mono);font-size:.86rem}
.domain-skill-score{font-family:var(--mono);font-size:.78rem;color:var(--muted)}
.back-link{margin-top:1.5rem}
.back-link a{color:var(--accent);text-decoration:none}
.back-link a:hover{text-decoration:underline}
@media (max-width:600px){
  .container{padding:1.4rem 1rem 2.5rem}
  .cards{grid-template-columns:1fr}
  .install-box{flex-direction:column;align-items:stretch}
  .dash-row{grid-template-columns:90px 1fr 36px}
  .skill-page-title{font-size:1.8rem}
}
"""
    (output_dir / "style.css").write_text(css, encoding="utf-8")
    print(f"Stylesheet written to {output_dir / 'style.css'}")


def build_seo_files(output_dir: Path, catalog_path: Path) -> None:
    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {BASE}sitemap.xml\n"
    )
    (output_dir / "robots.txt").write_text(robots, encoding="utf-8")

    _meta, skills, _ = load_all(catalog_path)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f"  <url><loc>{BASE}</loc><priority>1.0</priority></url>",
        f"  <url><loc>{BASE}skills_catalog.json</loc></url>",
        f"  <url><loc>{BASE}skills_catalog.schema.json</loc></url>",
    ]
    for s in sorted(skills, key=lambda x: x["name"]):
        lines.append(f"  <url><loc>{BASE}skills/{esc(s['name'])}.html</loc></url>")
    lines.append("</urlset>")
    (output_dir / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")
    print(f"robots.txt and sitemap.xml written to {output_dir}")


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Build documentation site")
    parser.add_argument("--catalog", default="skills_catalog.json", help="Path to catalog JSON")
    parser.add_argument("--output-dir", default="docs", help="Output directory")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    build_index_html(Path(args.catalog), output_dir)
    build_skill_pages(Path(args.catalog), output_dir)
    build_domain_pages(Path(args.catalog), output_dir)
    build_style_css(output_dir)
    build_seo_files(output_dir, Path(args.catalog))

    import shutil
    catalog_src = Path(args.catalog)
    if catalog_src.exists():
        shutil.copy2(catalog_src, output_dir / "skills_catalog.json")
    schema_src = Path(args.catalog).parent / "skills_catalog.schema.json"
    if schema_src.exists():
        shutil.copy2(schema_src, output_dir / "skills_catalog.schema.json")

    print(f"Documentation built in {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())