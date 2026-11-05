#!/usr/bin/env python3
"""Validate roadmap track files against roadmaps.schema.json semantics.

Hand-rolled checks (no extra dependency). Beyond generic schema shape:
  - a live track must ship the complete Russian mirror (name_ru, tagline_ru,
    and title_ru/items_ru equal in length for every stage);
  - a live stage must have at least 2 real items (one "Map drops soon"
    stub item can never be live);
  - related_skills must exist in the skills catalog (catalog names are
    read from skills_catalog.json when present);
  - catalog_domain must exist in the catalog domain set.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SLUG_RE = re.compile(r"^[a-z0-9-]+$")
STATUSES = {"soon", "live"}
STUB_ITEM = "Map drops soon"


def _fail(path: Path, where: str, msg: str, errors: list[str]) -> None:
    errors.append(f"{path.name}{where}: {msg}")


def _check_track(path: Path, errors: list[str]) -> bool:
    """Type/shape checks for one file; appends findings to `errors`.
    Returns False when the file is too broken for reporting (skip link checks)."""
    local: list[str] = []
    try:
        track = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        _fail(path, "", f"unreadable JSON: {e}", errors)
        return False
    if not isinstance(track, dict):
        _fail(path, "", "track must be a JSON object", errors)
        return False

    for key in ("slug", "name", "icon", "tagline", "status", "eta", "stages"):
        if key not in track:
            _fail(path, "", f"missing required key: {key}", local)
    if local:
        errors.extend(local)
        return False
    if not isinstance(track["slug"], str) or not SLUG_RE.match(track["slug"]):
        _fail(path, "", "slug must match ^[a-z0-9-]+$", local)
    for key in ("name", "icon", "tagline", "eta"):
        if not isinstance(track[key], str) or not track[key]:
            _fail(path, "", f"{key} must be a non-empty string", local)
    if track["status"] not in STATUSES:
        _fail(path, "", f"status must be one of {sorted(STATUSES)}", local)
    for key in ("name_ru", "tagline_ru"):
        if key in track and (not isinstance(track[key], str) or not track[key]):
            _fail(path, "", f"{key} must be a non-empty string when present", local)

    stages = track["stages"]
    if not isinstance(stages, list) or not stages:
        _fail(path, "", "stages must be a non-empty array", local)
        errors.extend(local)
        return False
    for i, stage in enumerate(stages):
        where = f".stages[{i}]"
        if not isinstance(stage, dict):
            _fail(path, where, "stage must be an object", errors)
            continue
        for key in ("title", "items", "status"):
            if key not in stage:
                _fail(path, where, f"missing required key: {key}", errors)
        if not isinstance(stage.get("title"), str) or not stage.get("title"):
            _fail(path, where, "title must be a non-empty string", errors)
        items = stage.get("items")
        if not isinstance(items, list) or not items or not all(isinstance(x, str) for x in items):
            _fail(path, where, "items must be a non-empty array of strings", errors)
        if stage.get("status") not in STATUSES:
            _fail(path, where, f"status must be one of {sorted(STATUSES)}", errors)
        title_ru = stage.get("title_ru")
        if title_ru is not None and (not isinstance(title_ru, str) or not title_ru):
            _fail(path, where, "title_ru must be a non-empty string when present", errors)
        items_ru = stage.get("items_ru")
        if items_ru is not None:
            if not isinstance(items_ru, list) or not items_ru or not all(isinstance(x, str) for x in items_ru):
                _fail(path, where, "items_ru must be a non-empty array of strings", errors)
            elif isinstance(items, list) and len(items_ru) != len(items):
                _fail(
                    path,
                    where,
                    f"items_ru ({len(items_ru)}) must mirror items ({len(items)}) one-to-one",
                    errors,
                )

    live = track["status"] == "live"
    if live:
        for key in ("name_ru", "tagline_ru"):
            if key not in track:
                _fail(path, "", f"live track needs the RU mirror: {key}", errors)
        for i, stage in enumerate(stages):
            if not isinstance(stage, dict):
                continue
            where = f".stages[{i}]"
            items = stage.get("items") if isinstance(stage.get("items"), list) else []
            items_ru = stage.get("items_ru") if isinstance(stage.get("items_ru"), list) else []
            if "title_ru" not in stage:
                _fail(path, where, "live stage needs title_ru", errors)
            if "items_ru" not in stage:
                _fail(path, where, "live stage needs items_ru", errors)
            if STUB_ITEM in [str(x) for x in items + items_ru]:
                _fail(path, where, 'live stage must not contain the "Map drops soon" stub', errors)
            if len(items) < 2:
                _fail(path, where, "live stage needs at least 2 real items", errors)
    errors.extend(local)
    return True


def _check_links(path: Path, track: dict, names: set[str], domains: set[str], errors: list[str]) -> None:
    domain = track.get("catalog_domain")
    if domain is not None and domain not in domains:
        _fail(path, "", f"unknown catalog_domain: {domain!r}", errors)
    related = track.get("related_skills")
    if related is not None:
        if not isinstance(related, list) or not all(isinstance(x, str) for x in related):
            _fail(path, "", "related_skills must be an array of skill names", errors)
        else:
            unknown = [r for r in related if r not in names]
            if unknown:
                _fail(path, "", f"unknown related_skills: {unknown}", errors)


def validate_directory(tracks_dir: Path, catalog_path: Path | None = None) -> list[str]:
    errors: list[str] = []
    paths = sorted(tracks_dir.glob("*.json"))
    if not paths:
        errors.append(f"no track files found in {tracks_dir}")
        return errors
    names: set[str] = set()
    domains: set[str] = set()
    if catalog_path is not None and catalog_path.exists():
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        names = {s["name"] for s in catalog["skills"]}
        domains = set(catalog["metadata"]["domains"])
    checked: list[dict] = []
    for path in paths:
        if _check_track(path, errors):
            checked.append(json.loads(path.read_text(encoding="utf-8")))
    if names or domains:
        # link checks only make sense with a known skills catalog; a build
        # pipeline that has not generated one yet is not an error
        for track in checked:
            _check_links(Path(tracks_dir) / f'{track["slug"]}.json', track, names, domains, errors)
    return errors


def main() -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _console import ensure_utf8_console

    ensure_utf8_console()
    root = Path(__file__).resolve().parent.parent
    catalog_path = root / "skills_catalog.json"
    errors = validate_directory(root / "roadmaps", catalog_path)
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print(f"roadmaps validation: {len(errors)} error(s)")
        return 1
    live = 0
    for path in sorted((root / "roadmaps").glob("*.json")):
        t = json.loads(path.read_text(encoding="utf-8"))
        live += 1 if t.get("status") == "live" else 0
    total = len(list((root / "roadmaps").glob("*.json")))
    print(f"roadmaps validation: {total} tracks OK ({live} live)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
