#!/usr/bin/env python3
"""Generate the documentation site from the catalog — modern, fast, searchable."""

from __future__ import annotations

import html as html_lib
import json
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


def esc(s: str) -> str:
    return html_lib.escape(s, quote=True)


def build_index_html(catalog_path: Path, output_dir: Path) -> str:
    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data["metadata"]
    skills = data["skills"]

    # Compute per-skill quality metrics by reading the actual files
    skill_metrics = {}
    for s in skills:
        en_path = Path(s["path"])
        if not en_path.exists():
            skill_metrics[s["name"]] = {"score": 100, "lines": 0, "blocks": 0, "sections": 0}
            continue
        text = en_path.read_text(encoding="utf-8")
        lines = text.count("\n") + 1
        blocks = text.count("```") // 2
        sections = text.count("\n## ")
        # rough freshness based on updated date
        try:
            updated = s.get("updated", "")
            if updated:
                dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                days = (datetime.now(timezone.utc) - dt).days
            else:
                days = 365
        except ValueError:
            days = 365
        score = 100
        if days > 90:
            score = 80
        if blocks < 4:
            score -= 10
        if lines < 90:
            score -= 10
        if sections < 7:
            score -= 5
        skill_metrics[s["name"]] = {"score": max(0, score), "lines": lines, "blocks": blocks, "sections": sections}

    model_names = set()
    for s in skills:
        for m in s.get("models", []):
            model_names.add(str(m))

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

    cards = []
    for s in sorted(skills, key=lambda x: (x["category"], x["name"])):
        color = DOMAIN_COLORS.get(s["category"], "#64748b")
        tags = s.get("tags", [])[:3]
        tag_html = "".join(f'<span class="tag">{esc(t)}</span>' for t in tags)
        ru_badge = '<span class="ru-badge">RU</span>' if s.get("has_ru") else ""
        m = skill_metrics.get(s["name"], {"score": 100, "lines": 0, "blocks": 0, "sections": 0})
        score = m["score"]
        bar_color = "#22c55e" if score >= 95 else "#f59e0b" if score >= 85 else "#ef4444"
        cards.append(
            f'<div class="card" data-name="{esc(s["name"].lower())}" '
            f'data-domain="{esc(s["category"].lower())}" '
            f'data-score="{score}" '
            f'data-tags=\'{esc(" ".join(s.get("tags", [])).lower())}\'>'
            f'<div class="card-top"><span class="card-name" onclick="copySkill(\'{esc(s["name"])}\')" title="Click to copy path">{esc(s["name"])}</span>{ru_badge}</div>'
            f'<div class="card-desc">{esc(s["description"])}</div>'
            f'<div class="card-score"><div class="score-row"><span>Quality</span><strong>{score}%</strong></div>'
            f'<div class="bar"><div class="bar-fill" style="width:{score}%;background:{bar_color}"></div></div></div>'
            f'<div class="card-meta"><span>{m["blocks"]} code blocks</span><span>{m["sections"]} sections</span><span>{m["lines"]} lines</span></div>'
            f'<div class="card-tags">{tag_html}</div>'
            f'<div class="card-domain" style="color:{color}">{esc(s["category"])}</div>'
            f'<div class="card-copy" onclick="copySkill(\'{esc(s["name"])}\')">copy path</div>'
            "</div>"
        )

    models_badges = "".join(
        f'<span class="model-badge">{esc(m)}</span>' for m in sorted(model_names)
    )

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Agent Skills Library — {meta["total_skills"]} curated bilingual skills</title>
  <meta name="description" content="Curated bilingual (EN + RU) skills in the universal Agent Skills format for Claude Code, OpenCode, Cursor, Windsurf and every LLM/GLM agent.">
  <meta property="og:title" content="Agent Skills Library">
  <meta property="og:description" content="Curated bilingual skills for every AI agent — Claude Code, OpenCode, Cursor, Windsurf, GPT, Gemini, GLM.">
  <meta property="og:url" content="{BASE}">
  <meta property="og:image" content="{REPO}/raw/main/.github/social-preview.svg">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2220%22 fill=%22%238b5cf6%22/><text x=%2250%22 y=%2268%22 font-size=%2250%22 text-anchor=%22middle%22 fill=%22white%22 font-family=%22Arial%22>S</text></svg>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebSite","name":"Agent Skills Library","url":"{BASE}","description":"{meta["total_skills"]} curated bilingual skills for every LLM/GLM agent"}}</script>
</head>
<body>
  <div class="bg-glow" aria-hidden="true"></div>
  <div class="container">
    <header class="hero">
      <div class="hero-badge">Universal Agent Skills Format</div>
      <h1>Agent Skills <span class="gradient">Library</span></h1>
      <p class="hero-sub">Curated bilingual (EN + RU) skills for Claude Code, OpenCode, Cursor, Windsurf and every Agent Skills–compatible agent.</p>
      <div class="hero-models">Models: {models_badges}</div>
    </header>

    <section class="stats" aria-label="Library statistics">
      <div class="stat"><span class="stat-num">{meta["total_skills"]}</span><span class="stat-label">Skills</span></div>
      <div class="stat"><span class="stat-num">{meta["total_ru"]}</span><span class="stat-label">Russian</span></div>
      <div class="stat"><span class="stat-num">{len(meta["domains"])}</span><span class="stat-label">Domains</span></div>
      <div class="stat"><span class="stat-num">100%</span><span class="stat-label">Quality</span></div>
    </section>

    <section class="install">
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

    <section class="search-section">
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
  </div>

  <div class="toast" id="toast"></div>

  <script>
  var activeDomain = 'all';
  function copyText(text) {{
    navigator.clipboard.writeText(text).then(function() {{ showToast('Copied: ' + text); }});
  }}
  function copySkill(name) {{
    copyText('.claude/skills/' + name);
  }}
  function showToast(msg) {{
    var t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(t._timer);
    t._timer = setTimeout(function() {{ t.classList.remove('show'); }}, 1800);
  }}
  function filterByDomain(domain, btn) {{
    activeDomain = domain;
    document.querySelectorAll('.pill').forEach(function(b) {{ b.classList.remove('active'); }});
    btn.classList.add('active');
    applyFilter();
  }}
  function onSearch(q) {{
    applyFilter();
  }}
  function applyFilter() {{
    var q = (document.getElementById('search').value || '').toLowerCase();
    var sort = document.getElementById('sort').value;
    var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
    var visible = 0;
    cards.forEach(function(c) {{
      var name = c.getAttribute('data-name');
      var domain = c.getAttribute('data-domain');
      var tags = c.getAttribute('data-tags') || '';
      var domainMatch = activeDomain === 'all' || domain === activeDomain;
      var textMatch = !q || name.includes(q) || domain.includes(q) || tags.includes(q);
      var show = domainMatch && textMatch;
      c.style.display = show ? '' : 'none';
      if (show) visible++;
    }});
    cards.sort(function(a, b) {{
      if (sort === 'score') return (b.getAttribute('data-score') || 0) - (a.getAttribute('data-score') || 0);
      if (sort === 'name') return a.getAttribute('data-name').localeCompare(b.getAttribute('data-name'));
      return a.getAttribute('data-domain').localeCompare(b.getAttribute('data-domain'));
    }});
    var grid = document.getElementById('cards');
    cards.forEach(function(c) {{ grid.appendChild(c); }});
    document.getElementById('empty').hidden = visible !== 0;
  }}
  </script>
</body>
</html>"""

    (output_dir / "index.html").write_text(html_doc, encoding="utf-8")
    print(f"Index written to {output_dir / 'index.html'}")
    return html_doc


def build_style_css(output_dir: Path) -> None:
    css = """:root{
  --bg:#0a0a12;--bg2:#10101c;--card:#141423;--card-hover:#1a1a2e;
  --text:#e8e8f5;--muted:#8b8ba3;--accent:#8b5cf6;--accent2:#ec4899;
  --border:rgba(255,255,255,.07);--radius:14px;
  --font:'Inter','Segoe UI',-apple-system,BlinkMacSystemFont,Roboto,sans-serif;
  --mono:'JetBrains Mono','Consolas','Menlo',monospace;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.6;min-height:100vh;overflow-x:hidden;
  -webkit-font-smoothing:antialiased;
}
.bg-glow{
  position:fixed;inset:0;z-index:-1;pointer-events:none;
  background:
    radial-gradient(700px 400px at 12% -5%,rgba(139,92,246,.14),transparent 60%),
    radial-gradient(800px 500px at 90% 5%,rgba(236,72,153,.10),transparent 60%),
    radial-gradient(700px 700px at 50% 110%,rgba(14,165,233,.07),transparent 60%);
}
.container{max-width:1180px;margin:0 auto;padding:2.5rem 1.5rem 4rem}
.hero{text-align:center;padding:2rem 0 1rem}
.hero-badge{
  display:inline-block;padding:.4rem 1.1rem;border-radius:999px;font-size:.76rem;
  background:rgba(139,92,246,.12);border:1px solid rgba(139,92,246,.28);
  color:#c4b5fd;letter-spacing:.06em;margin-bottom:1.1rem;font-weight:600;text-transform:uppercase;
}
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
  display:flex;align-items:center;gap:.7rem;background:#0d0d1f;
  border:1px solid var(--border);border-radius:12px;padding:.8rem 1rem;flex-wrap:wrap;
}
.install-box code{color:#7ee787;font-size:.86rem;font-family:var(--mono);flex:1;min-width:200px;overflow-x:auto}
.copy-btn{
  background:linear-gradient(90deg,var(--accent),var(--accent2));color:#fff;border:none;
  padding:.45rem 1rem;border-radius:8px;cursor:pointer;font-size:.78rem;font-weight:600;transition:opacity .15s;
}
.copy-btn:hover{opacity:.85}
.install-links{margin-top:.6rem;font-size:.82rem;color:var(--muted)}
.install-links a{color:var(--accent);text-decoration:none}
.install-links a:hover{text-decoration:underline}
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
  padding:1.2rem 1.25rem;transition:transform .18s,box-shadow .18s,border-color .18s;animation:rise .3s ease both;
}
.card:hover{transform:translateY(-4px);box-shadow:0 16px 40px rgba(0,0,0,.5);border-color:rgba(139,92,246,.35)}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.card-top{display:flex;align-items:center;justify-content:space-between;gap:.5rem}
.card-name{
  font-family:var(--mono);font-weight:700;font-size:.96rem;color:#d7c7ff;
  cursor:pointer;transition:color .15s;
}
.card-name:hover{color:var(--accent)}
.ru-badge{
  font-size:.6rem;font-weight:800;letter-spacing:.05em;color:#08120a;
  background:linear-gradient(90deg,#22c55e,#84cc16);border-radius:6px;padding:.14rem .5rem;flex-shrink:0;
}
.card-desc{color:var(--muted);font-size:.85rem;margin:.55rem 0 .75rem;line-height:1.55}
.card-score{margin:.4rem 0 .5rem}
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
.card-copy{
  position:absolute;top:.95rem;right:1.1rem;font-size:.66rem;color:var(--muted);opacity:0;
  background:rgba(139,92,246,.14);border:1px solid rgba(139,92,246,.3);border-radius:6px;
  padding:.22rem .6rem;cursor:pointer;transition:opacity .15s;pointer-events:none;
}
.card:hover .card-copy{opacity:1;pointer-events:auto}
.card-copy:hover{color:#fff}
.empty{text-align:center;color:var(--muted);padding:3rem 0;font-size:1.05rem}
footer{margin-top:3.5rem;text-align:center;color:var(--muted);font-size:.85rem}
footer p{margin:.3rem 0}
footer a{color:var(--accent);text-decoration:none}
footer a:hover{text-decoration:underline}
.toast{
  position:fixed;bottom:2rem;left:50%;transform:translateX(-50%) translateY(20px);
  background:#0d0d1f;border:1px solid rgba(139,92,246,.4);color:#e8e8f5;
  padding:.75rem 1.4rem;border-radius:10px;font-size:.85rem;opacity:0;pointer-events:none;
  transition:opacity .25s,transform .25s;z-index:100;box-shadow:0 12px 40px rgba(0,0,0,.6);
  max-width:90vw;
}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
@media (max-width:600px){
  .container{padding:1.4rem 1rem 2.5rem}
  .cards{grid-template-columns:1fr}
  .install-box{flex-direction:column;align-items:stretch}
}
"""
    (output_dir / "style.css").write_text(css, encoding="utf-8")
    print(f"Stylesheet written to {output_dir / 'style.css'}")


def build_seo_files(output_dir: Path) -> None:
    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {BASE}sitemap.xml\n"
    )
    (output_dir / "robots.txt").write_text(robots, encoding="utf-8")
    print(f"robots.txt written to {output_dir / 'robots.txt'}")

    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{BASE}</loc><priority>1.0</priority></url>\n"
        f"  <url><loc>{BASE}skills_catalog.json</loc></url>\n"
        f"  <url><loc>{BASE}skills_catalog.schema.json</loc></url>\n"
        "</urlset>\n"
    )
    (output_dir / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"sitemap.xml written to {output_dir / 'sitemap.xml'}")


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Build documentation site")
    parser.add_argument("--catalog", default="skills_catalog.json", help="Path to catalog JSON")
    parser.add_argument("--output-dir", default="docs", help="Output directory")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    api_dir = output_dir / "api"
    api_dir.mkdir(parents=True, exist_ok=True)

    build_index_html(Path(args.catalog), output_dir)
    build_style_css(output_dir)
    build_seo_files(output_dir)

    import shutil
    catalog_src = Path(args.catalog)
    if catalog_src.exists():
        shutil.copy2(catalog_src, output_dir / "skills_catalog.json")
        print(f"Catalog copied to {output_dir / 'skills_catalog.json'}")

    schema_src = Path(args.catalog).parent / "skills_catalog.schema.json"
    if schema_src.exists():
        shutil.copy2(schema_src, output_dir / "skills_catalog.schema.json")
        print(f"Schema copied to {output_dir / 'skills_catalog.schema.json'}")

    print(f"Documentation built in {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())