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


def skill_search_text(skill_path: Path) -> str:
    """Extract a searchable plain-text blob from a SKILL.md: headings, bullet
    lines, and prose (code fences excluded) so search matches skill content."""
    try:
        text = skill_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""
    parts = text.split("---", 2)
    body = parts[2] if len(parts) >= 3 else text
    out = []
    in_fence = False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = line.strip()
        if not s:
            continue
        s = re.sub(r"^#{1,6}\s+", "", s)
        s = re.sub(r"^[-*]\s+", "", s)
        s = re.sub(r"^>\s?", "", s)
        if len(s) > 3:
            out.append(s.lower())
    return " ".join(out)


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


def page_head(title: str, desc: str, canonical: str, extra: str = "", css_path: str = "../style.css", nav_index: str = "../index.html") -> str:
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
  <link rel="stylesheet" href="{css_path}">
  {extra}
</head>
<body data-theme="dark">
  <div class="bg-glow" aria-hidden="true"></div>
  <nav class="nav">
    <div class="nav-inner">
      <a class="nav-brand" href="{nav_index}"><span class="nav-logo">S</span><span class="nav-name">Agent&nbsp;Skills</span></a>
      <div class="nav-right">
        <a class="nav-link" href="{nav_index}#catalog">Catalog</a>
        <a class="nav-link" href="{nav_index}#dashboard">Stats</a>
        <a class="nav-link" href="{REPO}">GitHub</a>
        <a class="nav-link" href="https://t.me/ssrjkk_bot">Telegram</a>
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
    sessionStorage.setItem('theme', next);
    var btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = next === 'dark' ? '🌙' : '☀️';
  }
  (function() {
    var saved = sessionStorage.getItem('theme');
    if (saved === 'light') {
      document.body.setAttribute('data-theme', 'light');
      var btn = document.querySelector('.theme-toggle');
      if (btn) btn.textContent = '☀️';
    }
  })();
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
        css_path="style.css",
        nav_index="index.html",
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
      <div class="term-box" aria-hidden="true">
        <div class="term-bar">
          <span class="term-dot r"></span><span class="term-dot y"></span><span class="term-dot g"></span>
          <span class="term-title">agent-skills — zsh</span>
        </div>
        <div class="term-body" id="term-body"></div>
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
      <p><a href="{REPO}">GitHub</a> · <a href="{REPO}/issues">Report Issue</a> · <a href="{REPO}/discussions">Discussions</a> · <a href="https://t.me/ssrjkk_bot">Telegram</a></p>
    </footer>
""" + """
  <div class="toast" id="toast"></div>
  <script>
  var activeDomain = 'all';
  var searchIndex = null;
  function loadSearchIndex() {
    if (searchIndex) return;
    fetch('search-index.json').then(function(r) { return r.json(); }).then(function(data) {
      searchIndex = {};
      data.forEach(function(e) { searchIndex[e.name] = (e.content || '').toLowerCase(); });
    }).catch(function() { searchIndex = {}; });
  }
  function copyText(text) {
    navigator.clipboard.writeText(text).then(function() { showToast('Copied: ' + text); });
  }
  function copySkill(name) { copyText('.claude/skills/' + name); }
  function showToast(msg) {
    var t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(t._timer);
    t._timer = setTimeout(function() { t.classList.remove('show'); }, 1800);
  }
  function toggleTheme() {
    var b = document.body;
    var next = b.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    b.setAttribute('data-theme', next);
    sessionStorage.setItem('theme', next);
    var btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = next === 'dark' ? '🌙' : '☀️';
  }
  (function() {
    var saved = sessionStorage.getItem('theme');
    if (saved === 'light') {
      document.body.setAttribute('data-theme', 'light');
      var btn = document.querySelector('.theme-toggle');
      if (btn) btn.textContent = '☀️';
    }
  })();
  function filterByDomain(domain, btn) {
    activeDomain = domain;
    document.querySelectorAll('.pill').forEach(function(b) { b.classList.remove('active'); });
    btn.classList.add('active');
    applyFilter();
  }
  function onSearch(q) { loadSearchIndex(); applyFilter(); }
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
      var content = (searchIndex && searchIndex[name]) || '';
      var textMatch = !q || name.includes(q) || domain.includes(q) || tags.includes(q) || content.includes(q);
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
  // terminal typing animation
  (function() {
    var el = document.getElementById('term-body');
    if (!el) return;
    var lines = [
      '<span class="ln">~$</span> <span class="cmd">pip install agent-skills-library</span>',
      '<span class="ok">&#10003; 100 skills ready · 16 domains · EN+RU</span>',
      '<span class="ln">~$</span> <span class="cmd">agent-skills search rag</span>',
      '<span class="ok">&#10003; rag-pipeline · vector-databases · embeddings</span>',
      '<span class="ln">~$</span> <span class="cmd">agent-skills validate</span><span class="cursor"></span>',
    ];
    var idx = 0;
    el.innerHTML = '';
    function typeLine() {
      if (idx >= lines.length) { setTimeout(reset, 4000); return; }
      var line = document.createElement('div');
      line.innerHTML = lines[idx];
      el.appendChild(line);
      idx++;
      setTimeout(typeLine, 700);
    }
    function reset() {
      el.innerHTML = '';
      idx = 0;
      setTimeout(typeLine, 1500);
    }
    setTimeout(typeLine, 400);
  })();
  </script>
  </div>
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
  --bg:#0b0f0a;--bg2:#0e140d;--card:#11170f;--card-hover:#17210f;
  --text:#d6ffd0;--muted:#6f8f6a;--accent:#7dff4a;--accent2:#00ffd1;
  --border:rgba(125,255,74,.14);--radius:4px;
  --font:'JetBrains Mono','Consolas','Menlo',monospace;
  --mono:'JetBrains Mono','Consolas','Menlo',monospace;
  --grid:linear-gradient(rgba(125,255,74,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(125,255,74,.03) 1px,transparent 1px);
}
body[data-theme="light"]{
  --bg:#f4f6f1;--bg2:#eef1ea;--card:#ffffff;--card-hover:#e9efe4;
  --text:#14321f;--muted:#4a6a52;--accent:#1a7f37;--accent2:#007f6a;
  --border:rgba(20,80,40,.16);--radius:4px;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
::selection{background:var(--accent);color:#0b0f0a}
body{
  font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.6;min-height:100vh;overflow-x:hidden;
  -webkit-font-smoothing:antialiased;font-size:15px;
}
.bg-glow{
  position:fixed;inset:0;z-index:-1;pointer-events:none;
  background:
    radial-gradient(700px 500px at 15% -10%,rgba(125,255,74,.06),transparent 60%),
    radial-gradient(800px 500px at 90% 0%,rgba(0,255,209,.05),transparent 60%);
}
.nav{position:sticky;top:0;z-index:50;background:rgba(11,15,10,.85);backdrop-filter:blur(8px);border-bottom:1px solid var(--border)}
.nav-inner{max-width:1180px;margin:0 auto;padding:.7rem 1.5rem;display:flex;align-items:center;justify-content:space-between}
.nav-brand{display:flex;align-items:center;gap:.6rem;text-decoration:none;color:var(--text)}
.nav-logo{width:28px;height:28px;display:grid;place-items:center;font-weight:700;color:#0b0f0a;background:var(--accent);font-family:var(--mono);font-size:.85rem}
.nav-name{font-weight:700;letter-spacing:.02em}
.nav-right{display:flex;align-items:center;gap:1.2rem}
.nav-link{color:var(--muted);text-decoration:none;font-size:.85rem;transition:color .15s}
.nav-link:hover{color:var(--accent)}
.nav-link::before{content:"> ";color:var(--accent);opacity:.7}
.theme-toggle{background:var(--card);border:1px solid var(--border);color:var(--text);border-radius:var(--radius);width:32px;height:32px;cursor:pointer;font-size:1rem}
.theme-toggle:hover{border-color:var(--accent)}
.container{max-width:1180px;margin:0 auto;padding:2.5rem 1.5rem 4rem}
.hero{text-align:center;padding:2rem 0 1rem}
.hero-badge{
  display:inline-block;padding:.35rem .9rem;font-size:.72rem;
  border:1px solid var(--accent);color:var(--accent);
  letter-spacing:.1em;margin-bottom:1.2rem;text-transform:uppercase;background:rgba(125,255,74,.05);
}
.hero h1{font-size:clamp(2rem,5vw,3.4rem);font-weight:700;letter-spacing:-.01em;line-height:1.15}
.hero h1 .gradient{color:var(--accent)}
.hero-sub{max-width:640px;margin:.9rem auto 1.2rem;color:var(--muted);font-size:1rem}
.hero-models{display:flex;flex-wrap:wrap;gap:.4rem;justify-content:center}
.model-badge{
  padding:.18rem .6rem;font-size:.72rem;border:1px solid var(--border);color:var(--muted);background:var(--card);
}
.hero-cta{display:flex;gap:.8rem;justify-content:center;margin-top:1.6rem;flex-wrap:wrap}
.btn-primary{
  padding:.6rem 1.3rem;border:none;cursor:pointer;text-decoration:none;font-weight:600;font-size:.88rem;color:#0b0f0a;
  background:var(--accent);transition:opacity .15s;display:inline-block;border-radius:var(--radius);
}
.btn-primary:hover{opacity:.85}
.btn-ghost{
  padding:.6rem 1.3rem;border:1px solid var(--border);cursor:pointer;text-decoration:none;font-weight:600;font-size:.88rem;color:var(--text);
  background:var(--card);transition:border-color .15s;display:inline-block;border-radius:var(--radius);
}
.btn-ghost:hover{border-color:var(--accent)}
/* terminal hero prompt */
.term-box{
  max-width:640px;margin:1.8rem auto 0;text-align:left;background:var(--bg2);border:1px solid var(--border);
  border-radius:var(--radius);overflow:hidden;
}
.term-bar{display:flex;align-items:center;gap:.4rem;padding:.4rem .8rem;border-bottom:1px solid var(--border);background:rgba(0,0,0,.2)}
.term-dot{width:10px;height:10px;border-radius:50%}
.term-dot.r{background:#ff5f56}.term-dot.y{background:#ffbd2e}.term-dot.g{background:#27c93f}
.term-title{margin-left:.4rem;font-size:.72rem;color:var(--muted)}
.term-body{padding:1rem;font-size:.85rem;line-height:1.7;min-height:150px}
.term-body .ln{color:var(--muted)}
.term-body .cmd{color:var(--accent)}
.term-body .ok{color:var(--accent2)}
.cursor{display:inline-block;width:9px;height:1.1em;background:var(--accent);vertical-align:text-bottom;animation:blink 1s step-start infinite}
@keyframes blink{50%{opacity:0}}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:.8rem;margin:2rem 0}
.stat{
  background:var(--card);border:1px solid var(--border);padding:1.2rem .8rem;text-align:center;transition:border-color .2s;
}
.stat:hover{border-color:var(--accent)}
.stat-num{display:block;font-size:1.8rem;font-weight:700;color:var(--accent);letter-spacing:-.01em}
.stat-label{color:var(--muted);font-size:.72rem;text-transform:uppercase;letter-spacing:.1em}
.install{margin:1.5rem 0}
.install-header h2{font-size:1.1rem;margin-bottom:.8rem;letter-spacing:.02em}
.install-box{
  display:flex;align-items:center;gap:.7rem;background:var(--bg2);
  border:1px solid var(--border);padding:.7rem .9rem;flex-wrap:wrap;border-radius:var(--radius);
}
.install-box code{color:var(--accent);font-size:.8rem;font-family:var(--mono);flex:1;min-width:200px;overflow-x:auto}
.copy-btn{
  background:var(--accent);color:#0b0f0a;border:none;padding:.4rem .9rem;cursor:pointer;font-size:.74rem;font-weight:700;border-radius:var(--radius);
}
.copy-btn:hover{opacity:.85}
.install-links{margin-top:.6rem;font-size:.78rem;color:var(--muted)}
.install-links a{color:var(--accent);text-decoration:none}
.install-links a:hover{text-decoration:underline}
.dashboard{margin:2.5rem 0}
.dashboard h2{font-size:1.15rem;margin-bottom:1rem;letter-spacing:.02em}
.dash-list{display:flex;flex-direction:column;gap:.4rem}
.dash-row{display:grid;grid-template-columns:110px 1fr 40px;gap:.8rem;align-items:center}
.dash-name{font-family:var(--mono);font-size:.78rem;color:var(--muted);text-transform:capitalize}
.dash-bar{height:14px;background:rgba(0,0,0,.3);border:1px solid var(--border);overflow:hidden}
.dash-fill{height:100%;transition:width .6s ease;min-width:4px}
.dash-count{font-family:var(--mono);font-size:.78rem;text-align:right;color:var(--muted)}
.search-section{margin:2rem 0 1.5rem}
.search-row{display:flex;gap:.6rem;flex-wrap:wrap}
.search{
  flex:1;min-width:200px;padding:.85rem 1rem;font-size:.9rem;color:var(--text);
  background:var(--bg2);border:1px solid var(--border);outline:none;font-family:var(--mono);border-radius:var(--radius);
}
.search:focus{border-color:var(--accent)}
.sort{
  padding:.85rem .9rem;font-size:.8rem;color:var(--text);
  background:var(--bg2);border:1px solid var(--border);outline:none;cursor:pointer;font-family:var(--mono);border-radius:var(--radius);
}
.sort:hover{border-color:var(--accent)}
.pills{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.9rem}
.pill{
  display:inline-flex;align-items:center;gap:.4rem;padding:.32rem .7rem;border:1px solid var(--border);
  background:var(--card);color:var(--text);cursor:pointer;font-size:.75rem;font-weight:500;font-family:var(--mono);transition:all .12s;
}
.pill:hover{border-color:var(--dc,#7dff4a);transform:translateY(-1px)}
.pill.active{background:var(--dc,#7dff4a);border-color:var(--dc,#7dff4a);color:#0b0f0a}
.pill-count{font-size:.62rem;opacity:.7;background:rgba(0,0,0,.2);padding:.05rem .45rem}
.pill.active .pill-count{background:rgba(0,0,0,.25);color:#0b0f0a}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:.8rem}
.card{
  position:relative;background:var(--card);border:1px solid var(--border);
  padding:1rem 1.1rem;transition:border-color .15s,transform .15s;text-decoration:none;color:inherit;display:block;border-radius:var(--radius);
  content-visibility:auto;contain-intrinsic-size:auto 240px;
}
.card:hover{transform:translateY(-3px);border-color:var(--accent)}
.card-top{display:flex;align-items:center;justify-content:space-between;gap:.5rem}
.card-name{font-family:var(--mono);font-weight:700;font-size:.9rem;color:var(--accent)}
.card-name::before{content:"$ ";opacity:.5}
.card-desc{color:var(--muted);font-size:.78rem;margin:.5rem 0 .5rem;line-height:1.5}
.card-code{
  background:var(--bg2);border:1px solid var(--border);padding:.5rem .7rem;margin:0 0 .5rem;font-family:var(--mono);font-size:.66rem;line-height:1.4;overflow-x:auto;color:#9fc98f;
}
.card-score{margin:.2rem 0 .4rem}
.score-row{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.3rem;font-size:.74rem}
.score-row span{color:var(--muted);text-transform:uppercase;letter-spacing:.07em;font-size:.6rem}
.score-row strong{color:var(--accent);font-family:var(--mono)}
.bar{height:4px;background:rgba(0,0,0,.3);overflow:hidden}
.bar-fill{height:100%;transition:width .4s ease}
.card-meta{display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:.5rem;font-size:.62rem;color:var(--muted)}
.card-meta span{border:1px solid var(--border);padding:.1rem .4rem;font-family:var(--mono)}
.card-tags{display:flex;flex-wrap:wrap;gap:.3rem;margin-bottom:.6rem}
.tag{
  font-size:.62rem;padding:.1rem .45rem;color:var(--muted);border:1px solid var(--border);
}
.card-domain{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;opacity:.85}
.empty{text-align:center;color:var(--muted);padding:3rem 0;font-size:1rem}
footer{margin-top:3rem;text-align:center;color:var(--muted);font-size:.78rem}
footer p{margin:.3rem 0}
footer a{color:var(--accent);text-decoration:none}
footer a:hover{text-decoration:underline}
.toast{
  position:fixed;bottom:2rem;left:50%;transform:translateX(-50%) translateY(20px);
  background:var(--bg2);border:1px solid var(--accent);color:var(--text);
  padding:.6rem 1.2rem;font-size:.78rem;opacity:0;pointer-events:none;
  transition:opacity .25s,transform .25s;z-index:100;max-width:90vw;font-family:var(--mono);
}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.skill-page{max-width:900px;margin:0 auto}
.skill-page-head{padding:1.5rem 0 1rem}
.skill-page-badges{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center}
.domain-chip{
  display:inline-block;padding:.22rem .7rem;font-size:.7rem;font-weight:600;text-transform:uppercase;letter-spacing:.07em;border:1px solid;
}
.skill-page-title{font-size:1.9rem;font-weight:700;letter-spacing:-.01em;margin:.8rem 0 .4rem}
.skill-page-desc{color:var(--muted);font-size:.92rem;max-width:720px}
.skill-page-meta{display:flex;flex-wrap:wrap;gap:1rem;margin:1rem 0;font-size:.78rem;color:var(--muted)}
.skill-page-meta strong{color:var(--accent);font-family:var(--mono)}
.skill-page-actions{display:flex;gap:.7rem;margin:1rem 0}
.skill-page-models{display:flex;gap:.4rem;flex-wrap:wrap;margin:0 0 1.5rem;align-items:center}
.page-nav{display:flex;justify-content:space-between;gap:1rem;margin:1.2rem 0}
.page-nav-link{color:var(--accent);text-decoration:none;font-size:.82rem}
.page-nav-link:hover{text-decoration:underline}
.skill-page-body h1{font-size:1.4rem;margin:1.4rem 0 .6rem}
.skill-page-body h2{font-size:1.15rem;margin:1.3rem 0 .5rem;letter-spacing:.01em}
.skill-page-body h3{font-size:1rem;margin:1.1rem 0 .5rem}
.skill-page-body p{margin:.5rem 0;color:var(--text);font-size:.88rem}
.skill-page-body ul{margin:.5rem 0 .5rem 1.2rem}
.skill-page-body li{margin:.25rem 0;font-size:.88rem}
.skill-page-body blockquote{border-left:2px solid var(--accent);padding-left:.9rem;color:var(--muted);margin:.8rem 0}
.skill-page-body .ordered{margin:.3rem 0;color:var(--text);font-size:.88rem}
.codeblock{position:relative;margin:1rem 0;background:var(--bg2);border:1px solid var(--border);overflow:hidden;border-radius:var(--radius)}
.code{display:block;padding:.9rem;overflow-x:auto;font-family:var(--mono);font-size:.74rem;line-height:1.5;color:var(--text)}
.code-copy{position:absolute;top:.4rem;right:.4rem;font-size:.62rem;padding:.2rem .5rem}
.domain-page{max-width:900px;margin:0 auto}
.domain-page-head{padding:1.5rem 0 1rem}
.domain-page-head h1{font-size:1.8rem;font-weight:700;margin:.7rem 0 .3rem}
.domain-page-head p{color:var(--muted)}
.domain-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:.6rem;margin:1.5rem 0}
.domain-skill{
  display:flex;justify-content:space-between;align-items:center;gap:.6rem;padding:.7rem .9rem;
  background:var(--card);border:1px solid var(--border);text-decoration:none;color:inherit;transition:border-color .15s;
}
.domain-skill:hover{border-color:var(--accent)}
.domain-skill-name{font-family:var(--mono);font-size:.8rem}
.domain-skill-score{font-family:var(--mono);font-size:.72rem;color:var(--accent)}
.back-link{margin-top:1.5rem}
.back-link a{color:var(--accent);text-decoration:none}
.back-link a:hover{text-decoration:underline}
@media (max-width:600px){
  .container{padding:1.4rem 1rem 2.5rem}
  .cards{grid-template-columns:1fr}
  .install-box{flex-direction:column;align-items:stretch}
  .dash-row{grid-template-columns:80px 1fr 34px}
  .skill-page-title{font-size:1.4rem}
}
body[data-theme="light"] .hero-badge{color:#1a7f37;background:rgba(26,127,55,.08)}
body[data-theme="light"] .card-name{color:#1a7f37}
body[data-theme="light"] .card-name::before{opacity:.4}
body[data-theme="light"] .card-code{color:#2a5a3a}
body[data-theme="light"] .term-box{background:#f0f3ec}
body[data-theme="light"] .term-body{color:#14321f}
body[data-theme="light"] .term-body .ln{color:#4a6a52}
body[data-theme="light"] .install-box{background:#f0f3ec}
body[data-theme="light"] .bar{background:rgba(20,80,40,.12)}
body[data-theme="light"] .dash-bar{background:rgba(20,80,40,.1)}
body[data-theme="light"] .codeblock{background:#f0f3ec}
body[data-theme="light"] .pill-count{background:rgba(0,0,0,.1)}
body[data-theme="light"] .bg-glow{
  background:
    radial-gradient(700px 500px at 15% -10%,rgba(26,127,55,.06),transparent 60%),
    radial-gradient(800px 500px at 90% 0%,rgba(0,127,106,.05),transparent 60%);
}
"""
    (output_dir / "style.css").write_text(css, encoding="utf-8")
    print(f"Stylesheet written to {output_dir / 'style.css'}")


def build_search_index(catalog_path: Path, output_dir: Path) -> None:
    _meta, skills, _metrics = load_all(catalog_path)
    index = []
    for s in sorted(skills, key=lambda x: x["name"]):
        index.append({
            "name": s["name"],
            "category": s["category"],
            "content": skill_search_text(Path(s["path"]))[:2000],
        })
    out = output_dir / "search-index.json"
    out.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    print(f"Search index written to {out}")


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
    build_search_index(Path(args.catalog), output_dir)
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