"""Tests for scripts/validate_roadmaps.py gate logic (beyond source-data checks).

test_roadmaps_source.py validates the real repo data; here we validate the
validator itself against crafted tracks, including every failure branch.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tests.load_scripts import load_script


def _load() -> Any:
    return load_script("validate_roadmaps.py")


def _track(**overrides: Any) -> dict[str, Any]:
    track: dict[str, Any] = {
        "slug": "qa",
        "name": "QA",
        "icon": "🧪",
        "tagline": "Test design",
        "status": "soon",
        "eta": "2026-11",
        "stages": [{"title": "S0", "items": ["a", "b"], "status": "soon"}],
    }
    track.update(overrides)
    return track


def _write(tmp_path: Path, track: dict[str, Any], name: str = "qa.json") -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / name
    path.write_text(json.dumps(track), encoding="utf-8")
    return path


def _errors(tmp_path: Path, track: dict[str, Any], catalog: Path | None = None) -> list[str]:
    _write(tmp_path, track)
    mod = _load()
    errors: list[str] = mod.validate_directory(tmp_path, catalog)
    return errors


def _catalog(tmp_path: Path) -> Path:
    cat = {
        "metadata": {"domains": ["qa", "frontend"]},
        "skills": [{"name": "alpha"}, {"name": "beta"}],
    }
    path = tmp_path / "skills_catalog.json"
    path.write_text(json.dumps(cat), encoding="utf-8")
    return path


def test_valid_live_bilingual_track(tmp_path: Path):
    track = _track(
        status="live",
        name_ru="QA",
        tagline_ru="Тест-дизайн",
        stages=[{
            "title": "S0", "title_ru": "Э0",
            "items": ["a", "b"], "items_ru": ["а", "б"],
            "status": "live",
        }],
    )
    assert _errors(tmp_path, track) == []


def test_missing_required_key(tmp_path: Path):
    track = _track()
    del track["eta"]
    errors = _errors(tmp_path, track)
    assert any("missing required key: eta" in e for e in errors)


def test_bad_slug(tmp_path: Path):
    errors = _errors(tmp_path, _track(slug="QA_Bad"))
    assert any("slug must match" in e for e in errors)


def test_bad_status(tmp_path: Path):
    errors = _errors(tmp_path, _track(status="wip"))
    assert any("status must be one of" in e for e in errors)


def test_stage_items_ru_must_mirror_one_to_one(tmp_path: Path):
    track = _track(status="live", name_ru="Q", tagline_ru="Т",
                   stages=[{"title": "S", "title_ru": "С",
                            "items": ["a", "b"], "items_ru": ["а"],
                            "status": "live"}])
    errors = _errors(tmp_path, track)
    assert any("one-to-one" in e for e in errors)


def test_stub_item_rejected_in_live(tmp_path: Path):
    track = _track(status="live", name_ru="Q", tagline_ru="Т",
                   stages=[{"title": "S", "title_ru": "С",
                            "items": ["Map drops soon", "b"],
                            "items_ru": ["скоро", "б"],
                            "status": "live"}])
    errors = _errors(tmp_path, track)
    assert any("Map drops soon" in e for e in errors)


def test_live_stage_needs_two_items(tmp_path: Path):
    track = _track(status="live", name_ru="Q", tagline_ru="Т",
                   stages=[{"title": "S", "title_ru": "С",
                            "items": ["only"], "items_ru": ["один"],
                            "status": "live"}])
    errors = _errors(tmp_path, track)
    assert any("at least 2 real items" in e for e in errors)


def test_items_must_be_strings(tmp_path: Path):
    errors = _errors(tmp_path, _track(stages=[{"title": "S", "items": [1, 2], "status": "soon"}]))
    assert any("array of strings" in e for e in errors)


def test_live_track_needs_ru_mirror(tmp_path: Path):
    track = _track(status="live")
    errors = _errors(tmp_path, track)
    assert any("name_ru" in e for e in errors)
    assert any("title_ru" in e for e in errors)


def test_unknown_related_skills_with_catalog(tmp_path: Path):
    track = _track(related_skills=["ghost-skill"], catalog_domain="qa")
    errors = _errors(tmp_path, track, catalog=_catalog(tmp_path))
    assert any("unknown related_skills" in e and "ghost-skill" in e for e in errors)


def test_unknown_catalog_domain_with_catalog(tmp_path: Path):
    errors = _errors(tmp_path, _track(catalog_domain="nope"), catalog=_catalog(tmp_path))
    assert any("unknown catalog_domain" in e for e in errors)


def test_unreadable_json(tmp_path: Path):
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "broken.json").write_text("{not json", encoding="utf-8")
    mod = _load()
    errors = mod.validate_directory(tmp_path)
    assert any("unreadable JSON" in e for e in errors)


def test_empty_directory(tmp_path: Path):
    tmp_path.mkdir(parents=True, exist_ok=True)
    mod = _load()
    errors = mod.validate_directory(tmp_path)
    assert errors == [f"no track files found in {tmp_path}"]


def test_main_passes_on_real_repo():
    mod = _load()
    assert mod.main() == 0
