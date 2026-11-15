#!/usr/bin/env python3
"""Validate conveyor track files against conveyors.schema.json semantics.

Hand-rolled checks (no extra dependency), mirroring validate_roadmaps.py:
  - a live conveyor ships the complete Russian mirror (name/tagline/target,
    and title/goal/gates/artifacts mirrored 1-to-1 for every stage);
  - every stage has >= 3 gates, >= 1 artifact, >= 1 catalog skill,
    >= 1 prompt that exists in prompts/ with an .ru.md pair;
  - referenced skills must exist in the skills catalog;
  - no "Gate drops soon" stubs in a live conveyor.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SLUG_RE = re.compile(r"^[a-z0-9-]+$")
STATUSES = {"soon", "live"}
STUB = "Gate drops soon"


def _fail(path: Path, where: str, msg: str, errors: list[str]) -> None:
    errors.append(f"{path.name}{where}: {msg}")


def _check_track(path: Path, errors: list[str], catalog_skills: set[str] | None, prompts_dir: Path) -> bool:
    local: list[str] = []
    try:
        track = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        _fail(path, "", f"unreadable JSON: {e}", errors)
        return False
    if not isinstance(track, dict):
        _fail(path, "", "conveyor must be a JSON object", errors)
        return False

    for key in ("slug", "name", "icon", "tagline", "target", "status", "stages"):
        if key not in track:
            _fail(path, "", f"missing required key: {key}", local)
    if local:
        errors.extend(local)
        return False

    if not isinstance(track["slug"], str) or not SLUG_RE.match(track["slug"]):
        _fail(path, "", "slug must match ^[a-z0-9-]+$", local)
    if track["slug"] != path.stem:
        _fail(path, "", f"slug {track['slug']!r} != filename stem", local)
    for key in ("name", "icon", "tagline", "target"):
        if not isinstance(track[key], str) or not track[key]:
            _fail(path, "", f"{key} must be a non-empty string", local)
    if track["status"] not in STATUSES:
        _fail(path, "", f"status must be one of {sorted(STATUSES)}", local)
    for key in ("name_ru", "tagline_ru", "target_ru"):
        if key in track and (not isinstance(track[key], str) or not track[key]):
            _fail(path, "", f"{key} must be a non-empty string when present", local)

    stages = track["stages"]
    if not isinstance(stages, list) or not stages:
        _fail(path, "", "stages must be a non-empty array", local)
        errors.extend(local)
        return False

    live = track["status"] == "live"
    for i, stage in enumerate(stages):
        where = f".stages[{i}]"
        if not isinstance(stage, dict):
            _fail(path, where, "stage must be an object", errors)
            continue
        for key in ("id", "title", "goal", "gates", "skills", "prompts", "artifacts"):
            if key not in stage:
                _fail(path, where, f"missing required key: {key}", errors)
        sid = stage.get("id", f"[{i}]")
        where = f".stages[{sid}]"

        if not isinstance(stage.get("id"), str) or not SLUG_RE.match(stage.get("id", "")):
            _fail(path, where, "id must match ^[a-z0-9-]+$", errors)
        if not isinstance(stage.get("title"), str) or not stage["title"]:
            _fail(path, where, "title must be a non-empty string", errors)
        if not isinstance(stage.get("goal"), str) or not stage["goal"]:
            _fail(path, where, "goal must be a non-empty string", errors)

        gates = stage.get("gates")
        if not isinstance(gates, list) or len(gates) < 3 or not all(isinstance(g, str) and g.strip() for g in gates):
            _fail(path, where, "gates must be >= 3 non-empty strings", errors)
        if STUB in [str(g) for g in gates if isinstance(g, str)] and live:
            _fail(path, where, f'live stage must not contain the "{STUB}" stub', errors)

        for key in ("gates_ru", "artifacts_ru"):
            val = stage.get(key)
            en_key = "gates" if key == "gates_ru" else "artifacts"
            if val is not None:
                if not isinstance(val, list) or not val or not all(isinstance(x, str) and x.strip() for x in val):
                    _fail(path, where, f"{key} must be a non-empty array of strings", errors)
                elif live and len(val) != len(stage.get(en_key, [])):
                    _fail(path, where, f"{key} ({len(val)}) must mirror {en_key} ({len(stage.get(en_key, []))}) one-to-one", errors)

        skills = stage.get("skills")
        if not isinstance(skills, list) or not skills or not all(isinstance(x, str) for x in skills):
            _fail(path, where, "skills must be a non-empty array of catalog skill names", errors)
        elif catalog_skills is not None:
            unknown = [x for x in skills if x not in catalog_skills]
            if unknown:
                _fail(path, where, f"unknown skills: {unknown}", errors)

        prompts = stage.get("prompts")
        if not isinstance(prompts, list) or not prompts or not all(isinstance(x, str) for x in prompts):
            _fail(path, where, "prompts must be a non-empty array of prompt slugs", errors)
        else:
            for slug in prompts:
                en_p = prompts_dir / f"{slug}.md"
                ru_p = prompts_dir / f"{slug}.ru.md"
                if not en_p.exists():
                    _fail(path, where, f"prompt file missing: prompts/{slug}.md", errors)
                if not ru_p.exists():
                    _fail(path, where, f"prompt RU mirror missing: prompts/{slug}.ru.md", errors)

        artifacts = stage.get("artifacts")
        if not isinstance(artifacts, list) or not artifacts or not all(isinstance(x, str) and x.strip() for x in artifacts):
            _fail(path, where, "artifacts must be a non-empty array of strings", errors)

    if live:
        for key in ("name_ru", "tagline_ru", "target_ru"):
            if key not in track:
                _fail(path, "", f"live conveyor needs the RU mirror: {key}", errors)
        for i, stage in enumerate(stages):
            if isinstance(stage, dict):
                for key in ("title_ru", "goal_ru"):
                    if key not in stage:
                        _fail(path, f".stages[{i}]", f"live stage needs the RU mirror: {key}", errors)

    errors.extend(local)
    return True


def validate_directory(
    conveyors_dir: Path,
    catalog_path: Path | None = None,
    prompts_dir: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    paths = sorted(conveyors_dir.glob("*.json"))
    if not paths:
        errors.append(f"no conveyor files found in {conveyors_dir}")
        return errors

    names: set[str] = set()
    if catalog_path is not None and catalog_path.exists():
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        names = {s["name"] for s in catalog["skills"]}

    pdir = prompts_dir or (conveyors_dir.parent / "prompts")
    for path in paths:
        _check_track(path, errors, names or None, pdir)
    return errors


def main() -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _console import ensure_utf8_console

    ensure_utf8_console()
    root = Path(__file__).resolve().parent.parent
    errors = validate_directory(root / "conveyors", root / "skills_catalog.json")
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print(f"conveyors validation: {len(errors)} error(s)")
        return 1
    live = 0
    for path in sorted((root / "conveyors").glob("*.json")):
        t = json.loads(path.read_text(encoding="utf-8"))
        live += 1 if t.get("status") == "live" else 0
    total = len(list((root / "conveyors").glob("*.json")))
    print(f"conveyors validation: {total} conveyors OK ({live} live)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
