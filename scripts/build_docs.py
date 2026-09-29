#!/usr/bin/env python3
"""Generate the documentation site from the catalog — with search & copy."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def build_index_html(catalog_path: Path, output_dir: Path) -> str:
    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data["metadata"]
    skills = data["skills"]

    model_names = set()
    for s in skills:
        for m in s.get("models", []):
            model_names.add(str(m))
    models_str = " · ".join(sorted(model_names))

    by_category: dict[str, list] = {}
    for s in skills:
        by_category.setdefault(s["category"], []).append(s)

    lines = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '  <meta charset="UTF-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f"  <title>Claude Skills Library — {meta['total_skills']} curated bilingual skills</title>",
        '  <meta name="description" content="Curated bilingual (EN + RU) skills in the universal Agent Skills format for Claude Code, OpenCode, Cursor, Windsurf and every LLM/GLM agent.">',
        '  <meta property="og:title" content="Claude Skills Library">',
        '  <meta property="og:description" content="Curated bilingual skills for every AI agent — Claude Code, OpenCode, Cursor, Windsurf, GPT, Gemini, GLM.">',
        '  <meta property="og:url" content="https://ssrjkk.github.io/agent-skills/">',
        '  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2220%22 fill=%22%23667eea%22/><text x=%2250%22 y=%2268%22 font-size=%2250%22 text-anchor=%22middle%22 fill=%22white%22 font-family=%22Arial%22>S</text></svg>">',
        '  <link rel="stylesheet" href="style.css">',
        "</head>",
        "<body>",
        '  <div class="container">',
        '    <header>',
        '      <h1>Claude Skills Library</h1>',
        (
            f'      <p class="subtitle">{meta["total_skills"]} skills across {len(meta["domains"])} domains · '
            f'{meta["total_ru"]} Russian translations</p>'
        ),
        "    </header>",
        (
            f'      <p class="subtitle" style="color:#666;font-size:.95rem;margin-top:.5rem">Models: '
            f"{models_str}</p>"
        ),
        '    <div class="search-bar">',
        (
            '      <input type="text" id="search" placeholder="Search skills by name, domain, or tag..." '
            'oninput="filterSkills(this.value)">'
        ),
        "    </div>",
        '    <section id="stats">',
        "      <div class=stats-grid>",
        f'        <div class=stat><strong>{meta["total_skills"]}</strong><span>Total Skills</span></div>',
        f'        <div class=stat><strong>{meta["total_ru"]}</strong><span>Russian</span></div>',
        f'        <div class=stat><strong>{len(meta["domains"])}</strong><span>Domains</span></div>',
        f'        <div class=stat><strong>{meta["schema_version"]}</strong><span>Schema</span></div>',
        "      </div>",
        "    </section>",
        '    <section id="domains">',
        "      <h2>Domains</h2>",
        '      <div class="domain-list" id="domain-list">',
    ]

    for domain in sorted(by_category):
        domain_skills = by_category[domain]
        ru = sum(1 for s in domain_skills if s.get("has_ru"))
        lines.extend([
            f'        <div class="domain" data-domain="{domain}">',
            (
                f'          <button class="domain-header" onclick="toggleDomain(this)">'
                f'            <strong>{domain}</strong>'
                f'            <span class="domain-meta">{len(domain_skills)} skills, {ru} RU</span>'
                f"          </button>"
            ),
            '          <ul class="skill-list" style="display:none">',
        ])
        for s in sorted(domain_skills, key=lambda x: x["name"]):
            flags = " " if s.get("has_ru") else ""
            tags = ", ".join(s.get("tags", [])[:3])
            esc_name = s["name"].replace("'", "\\'")
            lines.append(
                f'            <li class="skill-item" data-name="{esc_name}" '
                f'data-domain="{domain}" data-tags=\'{json.dumps(s.get("tags", []))}\'>'
                f'<code onclick="copySkill(\'{esc_name}\')" title="Click to copy path">{s["name"]}</code>{flags}'
                f'<br><small>{tags}</small></li>'
            )
        lines.extend([
            "          </ul>",
            "        </div>",
        ])

    # Inline JS
    skill_count = len(skills)
    lines.extend([
        "      </div>",
        "    </section>",
        '    <section id="install">',
        "      <h2>Install</h2>",
        '      <div class="install-box">',
        '        <code>curl -fsSL https://raw.githubusercontent.com/ssrjkk/agent-skills/main/install.sh | bash</code>',
        "      </div>",
        "      <p style='color:#666;font-size:.9rem'>"
        "Portable to Claude Code, OpenCode, Cursor, Windsurf. "
        '<a href="skills_catalog.json" download>Download catalog (JSON)</a></p>',
        "    </section>",
        "    <footer>",
        (
            f"      <p>Generated on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · "
            f'{skill_count} total skills</p>'
        ),
        (
            '      <p><a href="https://github.com/ssrjkk/agent-skills">GitHub</a> · '
            '<a href="https://github.com/ssrjkk/agent-skills/issues">Report Issue</a></p>'
        ),
        "    </footer>",
        "  </div>",
        "  <script>",
        "  function toggleDomain(btn) {",
        "    var list = btn.nextElementSibling;",
        "    list.style.display = list.style.display === 'none' ? 'block' : 'none';",
        "  }",
        "  function filterSkills(q) {",
        "    q = q.toLowerCase();",
        "    var items = document.querySelectorAll('.skill-item');",
        "    var domains = document.querySelectorAll('.domain');",
        "    var anyVisible = false;",
        "    items.forEach(function(item) {",
        "      var name = item.getAttribute('data-name').toLowerCase();",
        "      var domain = item.getAttribute('data-domain').toLowerCase();",
        "      var tags = (item.getAttribute('data-tags') || '').toLowerCase();",
        "      var match = name.includes(q) || domain.includes(q) || tags.includes(q);",
        "      item.style.display = match ? '' : 'none';",
        "      if (match) anyVisible = true;",
        "    });",
        "    if (q) {",
        "      domains.forEach(function(d) {",
        "        var list = d.querySelector('.skill-list');",
        "        list.style.display = 'block';",
        "      });",
        "    }",
        "  }",
        "  function copySkill(name) {",
        "    var path = '.claude/skills/' + name;",
        "    navigator.clipboard.writeText(path);",
        "    alert(' Copied: ' + path);",
        "  }",
        "  </script>",
        "</body>",
        "</html>",
    ])

    html = "\n".join(lines)
    (output_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"Index written to {output_dir / 'index.html'}")
    return html


def build_style_css(output_dir: Path) -> None:
    css = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;line-height:1.6;color:#1a1a2e;background:#f8f9fa;padding:2rem}
.container{max-width:1000px;margin:0 auto}
header{text-align:center;margin-bottom:2rem}
header h1{font-size:2.5rem;background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:.5rem}
.subtitle{color:#666;font-size:1.1rem}
.search-bar{margin-bottom:2rem}
.search-bar input{width:100%;padding:1rem 1.5rem;border:2px solid #e0e0e0;border-radius:12px;font-size:1.05rem;outline:none;transition:border-color .2s}
.search-bar input:focus{border-color:#667eea}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:1.5rem;margin:1.5rem 0}
.stat{background:white;border-radius:12px;padding:1.5rem;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.stat strong{display:block;font-size:2rem;color:#667eea}
.stat span{color:#666;font-size:.9rem}
h2{margin:2rem 0 1rem;font-size:1.5rem;color:#1a1a2e}
.domain{background:white;border-radius:8px;margin-bottom:.75rem;box-shadow:0 1px 4px rgba(0,0,0,.04);overflow:hidden}
.domain-header{width:100%;padding:1rem 1.5rem;border:none;background:none;cursor:pointer;font-size:1.05rem;text-align:left;display:flex;justify-content:space-between;align-items:center;transition:background .2s}
.domain-header:hover{background:#f0f0ff}
.domain-meta{color:#999;font-size:.85rem}
.skill-list{list-style:none;padding:.5rem 1.5rem 1rem;display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:.5rem}
.skill-list li{padding:.35rem .5rem;font-size:.9rem}
.skill-list code{color:#667eea;font-size:.85rem;cursor:pointer;transition:color .15s}
.skill-list code:hover{color:#764ba2;text-decoration:underline}
.skill-list small{color:#999;display:block}
footer{margin-top:3rem;text-align:center;color:#999;font-size:.9rem}
footer a{color:#667eea;text-decoration:none}
footer a:hover{text-decoration:underline}
.install-box{background:#1a1a2e;border-radius:10px;padding:1rem 1.25rem;overflow-x:auto;margin:.5rem 0 1rem}
.install-box code{color:#7ee787;font-size:.9rem}"""
    (output_dir / "style.css").write_text(css, encoding="utf-8")
    print(f"Stylesheet written to {output_dir / 'style.css'}")


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

    import shutil
    catalog_src = Path(args.catalog)
    if catalog_src.exists():
        shutil.copy2(catalog_src, output_dir / "skills_catalog.json")
        print(f"Catalog copied to {output_dir / 'skills_catalog.json'}")

    print(f"Documentation built in {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
