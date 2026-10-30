"""Tests for Claude Skills Library."""

import glob
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILLS_DIR = ROOT / ".claude" / "skills"
CATALOG = ROOT / "skills_catalog.json"


def test_catalog_exists():
    assert CATALOG.exists(), "skills_catalog.json not found"


def test_catalog_valid_json():
    with open(CATALOG, encoding='utf-8') as f:
        data = json.load(f)
    assert "metadata" in data
    assert "skills" in data
    assert isinstance(data["skills"], list)


def test_catalog_metadata():
    with open(CATALOG, encoding='utf-8') as f:
        data = json.load(f)
    meta = data["metadata"]
    assert meta["total_skills"] == len(data["skills"])
    assert meta["total_skills"] > 0
    assert len(meta["domains"]) > 0


def test_catalog_paths_are_correct():
    with open(CATALOG, encoding='utf-8') as f:
        data = json.load(f)
    bad = [s for s in data["skills"] if ".claude/skills/.claude/skills" in s.get("path", "")]
    assert len(bad) == 0, f"{len(bad)} skills have double-prefixed paths"


def test_all_skills_exist_on_disk():
    with open(CATALOG, encoding='utf-8') as f:
        data = json.load(f)
    missing = []
    for s in data["skills"]:
        p = SKILLS_DIR / s["category"] / s["name"] / "SKILL.md"
        if not p.exists():
            p2 = SKILLS_DIR / s["category"] / (s["name"] + ".md")
            if not p2.exists():
                missing.append(f'{s["category"]}/{s["name"]}')
    assert len(missing) == 0, f"{len(missing)} skills missing: {missing[:10]}"


def _get_skill_name(sk_path: str | Path) -> str:
    parent = Path(sk_path).parent
    if parent.name == "SKILL":
        return parent.parent.name
    return parent.name

def test_all_skill_files_have_frontmatter():
    for sk_path in sorted(glob.glob(str(SKILLS_DIR / "**" / "SKILL.md"), recursive=True)):
        name = _get_skill_name(sk_path)
        with open(sk_path, encoding='utf-8') as f:
            content = f.read()
        assert content.startswith('---'), f'{name}: Missing frontmatter'


def test_all_skills_have_required_frontmatter_fields():
    required = ['name', 'description', 'category', 'tags', 'models', 'version']
    errors = []
    for sk_path in sorted(glob.glob(str(SKILLS_DIR / "**" / "SKILL.md"), recursive=True)):
        name = _get_skill_name(sk_path)
        with open(sk_path, encoding='utf-8') as f:
            content = f.read()
        if not content.startswith('---'):
            continue
        end = content.find('---', 3)
        if end < 0:
            continue
        fm = content[3:end].strip()
        fields = set()
        for line in fm.split('\n'):
            if ':' in line:
                fields.add(line.split(':')[0].strip())
        missing = [f for f in required if f not in fields]
        if missing:
            errors.append(f'{name}: missing {missing}')
    assert len(errors) == 0, 'Frontmatter errors:\n' + '\n'.join(errors[:20])


def test_catalog_domains_match_disk():
    with open(CATALOG, encoding='utf-8') as f:
        data = json.load(f)
    catalog_domains = set(data["metadata"]["domains"])
    disk_domains = set()
    for d in SKILLS_DIR.iterdir():
        if d.is_dir() and not d.name.startswith('.'):
            has_skills = any(d.rglob("SKILL.md"))
            if has_skills:
                disk_domains.add(d.name)
    missing_from_catalog = disk_domains - catalog_domains
    extra_in_catalog = catalog_domains - disk_domains
    assert not missing_from_catalog, f"Domains on disk not in catalog: {missing_from_catalog}"
    assert not extra_in_catalog, f"Domains in catalog not on disk: {extra_in_catalog}"


def test_no_template_placeholders():
    bad_patterns = ['TODO', 'FIXME']
    issues = []
    for sk_path in sorted(glob.glob(str(SKILLS_DIR / "**" / "SKILL.md"), recursive=True)):
        name = Path(sk_path).parent.name
        with open(sk_path, encoding='utf-8') as f:
            content = f.read()
        for pat in bad_patterns:
            if pat in content:
                issues.append(f'{name}: contains "{pat}"')
    assert len(issues) == 0, 'Templates with placeholders:\n' + '\n'.join(issues[:20])


def test_readme_table_in_sync():
    import re
    with open(CATALOG, encoding='utf-8') as f:
        data = json.load(f)
    byname = {s['name']: s for s in data['skills']}
    readme = (ROOT / "README.md").read_text(encoding='utf-8')
    seen = set()
    bad = []
    for m in re.finditer(r"^\| `(\w[\w-]*)` \| `([\w-]+)` \| (.*?) \|$", readme, re.MULTILINE):
        domain, skill, desc = m.group(1), m.group(2), m.group(3).strip()
        seen.add(skill)
        s = byname.get(skill)
        if not s:
            bad.append(f'{skill}: in README but not in catalog')
            continue
        if s['description'].strip() != desc:
            bad.append(f'{skill}: description differs from SKILL.md')
        if s['category'] != domain:
            bad.append(f'{skill}: domain {domain} != {s["category"]}')
    missing = [n for n in byname if n not in seen]
    if missing:
        bad.append(f'missing from README table: {missing[:10]}')
    assert not bad, 'README out of sync:\n' + '\n'.join(bad[:20])


def test_body_length():
    short = []
    for sk_path in sorted(glob.glob(str(SKILLS_DIR / "**" / "SKILL.md"), recursive=True)):
        name = _get_skill_name(sk_path)
        with open(sk_path, encoding='utf-8') as f:
            content = f.read()
        if not content.startswith('---'):
            continue
        end = content.find('---', 3)
        body = content[end + 3:].strip() if end > 0 else content.strip()
        if len(body) < 80:
            short.append(f'{name} ({len(body)} chars)')
    assert len(short) == 0, 'Very short bodies:\n' + '\n'.join(short[:20])
