"""Roadmap track files: repo sanity + validator unit behavior."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path
from typing import Any

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
REPO = Path(__file__).resolve().parents[1]


def _load() -> Any:
    spec = importlib.util.spec_from_file_location("validate_roadmaps", SCRIPTS / "validate_roadmaps.py")
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _small_track(**overrides: Any) -> dict[str, Any]:
    track: dict[str, Any] = {
        "slug": "demo",
        "name": "Demo",
        "icon": "🧪",
        "tagline": "demo tagline",
        "status": "soon",
        "eta": "soon",
        "stages": [{"title": "Stage 0", "items": ["Map drops soon"], "status": "soon"}],
    }
    track.update(overrides)
    return track


def _write_track(tmp_path: Path, data: dict[str, Any], name: str = "demo.json") -> Path:
    tracks = tmp_path / "roadmaps"
    tracks.mkdir(parents=True, exist_ok=True)
    (tracks / name).write_text(json.dumps(data), encoding="utf-8")
    return tracks


class TestRepoTracks:
    def test_all_repo_tracks_pass_validation(self):
        mod = _load()
        errors = mod.validate_directory(REPO / "roadmaps")
        assert errors == []

    def test_repo_live_tracks_mirror_links(self):
        """related_skills and catalog_domain of live tracks exist in the real catalog."""
        names: set[str] = set()
        domains: set[str] = set()
        for path in sorted((REPO / ".claude" / "skills").glob("*/*/SKILL.md")):
            fm = path.read_text(encoding="utf-8").split("---", 2)[1]
            m = re.search(r"^name: (.*)$", fm, re.M)
            c = re.search(r"^category: (.*)$", fm, re.M)
            if m:
                names.add(m.group(1).strip())
            if c:
                domains.add(c.group(1).strip())
        for path in sorted((REPO / "roadmaps").glob("*.json")):
            track = json.loads(path.read_text(encoding="utf-8"))
            if track.get("status") != "live":
                continue
            domain = track.get("catalog_domain")
            assert domain is None or domain in domains, f"{track['slug']}: bad catalog_domain {domain!r}"
            unknown = [r for r in track.get("related_skills", []) if r not in names]
            assert not unknown, f"{track['slug']}: unknown related_skills {unknown}"


class TestValidator:
    def test_valid_soon_track_has_no_findings(self, tmp_path: Path):
        mod = _load()
        tracks = _write_track(tmp_path, _small_track())
        assert mod.validate_directory(tracks) == []

    def test_not_a_json_object(self, tmp_path: Path):
        mod = _load()
        tracks_dir = tmp_path / "roadmaps"
        tracks_dir.mkdir()
        (tracks_dir / "bad.json").write_text("[]", encoding="utf-8")
        errors = mod.validate_directory(tracks_dir)
        assert any("must be a JSON object" in e for e in errors)

    def test_unreadable_json(self, tmp_path: Path):
        mod = _load()
        tracks_dir = tmp_path / "roadmaps"
        tracks_dir.mkdir()
        (tracks_dir / "bad.json").write_text("{nope", encoding="utf-8")
        errors = mod.validate_directory(tracks_dir)
        assert any("unreadable" in e for e in errors)

    def test_missing_required_key(self, tmp_path: Path):
        mod = _load()
        track = _small_track()
        del track["status"]
        errors = mod.validate_directory(_write_track(tmp_path, track))
        assert any("missing required key: status" in e for e in errors)

    def test_bad_slug(self, tmp_path: Path):
        mod = _load()
        errors = mod.validate_directory(_write_track(tmp_path, _small_track(slug="Demo_X")))
        assert any("slug" in e for e in errors)

    def test_bad_status_enum(self, tmp_path: Path):
        mod = _load()
        errors = mod.validate_directory(_write_track(tmp_path, _small_track(status="finished")))
        assert any("`status` must" in e or "status must" in e for e in errors)

    def test_empty_stage_items(self, tmp_path: Path):
        mod = _load()
        track = _small_track()
        track["stages"][0]["items"] = []
        errors = mod.validate_directory(_write_track(tmp_path, track))
        assert any("items must be a non-empty array" in e for e in errors)

    def test_bad_catalog_domain(self, tmp_path: Path):
        mod = _load()
        catalog = tmp_path / "catalog.json"
        catalog.write_text(
            json.dumps({"metadata": {"domains": ["qa"]}, "skills": [{"name": "pytest"}]}),
            encoding="utf-8",
        )
        errors = mod.validate_directory(
            _write_track(tmp_path, _small_track(catalog_domain="not-a-domain")), catalog_path=catalog
        )
        assert any("unknown catalog_domain" in e for e in errors)

    def test_unknown_related_skill(self, tmp_path: Path):
        mod = _load()
        catalog = tmp_path / "catalog.json"
        catalog.write_text(json.dumps({"metadata": {"domains": []}, "skills": [{"name": "pytest"}]}), encoding="utf-8")
        errors = mod.validate_directory(
            _write_track(tmp_path, _small_track(related_skills=["pytest", "ghost-skill"])), catalog_path=catalog
        )
        assert any("unknown related_skills" in e and "ghost-skill" in e for e in errors)

    def test_empty_directory(self, tmp_path: Path):
        mod = _load()
        errors = mod.validate_directory(tmp_path / "roadmaps" if (tmp_path / "roadmaps").exists() else tmp_path)
        assert errors and "no track files" in errors[0]


class TestLiveInvariants:
    def _live(self, **over: Any) -> dict[str, Any]:
        stage = {
            "title": "Stage 0",
            "title_ru": "Этап 0",
            "items": ["first", "second"],
            "items_ru": ["первый", "второй"],
            "status": "live",
        }
        stage.update(over)
        return _small_track(
            status="live",
            name_ru="Демо",
            tagline_ru="демо тэглайн",
            stages=[stage],
        )

    def test_valid_live_track_passes(self, tmp_path: Path):
        mod = _load()
        assert mod.validate_directory(_write_track(tmp_path, self._live())) == []

    def test_live_without_ru_mirror(self, tmp_path: Path):
        mod = _load()
        track = self._live()
        del track["name_ru"], track["tagline_ru"]
        track["stages"][0].pop("title_ru")
        track["stages"][0].pop("items_ru")
        errors = mod.validate_directory(_write_track(tmp_path, track))
        assert any("needs the RU mirror: name_ru" in e for e in errors)
        assert any("needs title_ru" in e for e in errors)
        assert any("needs items_ru" in e for e in errors)

    def test_live_stub_item_rejected(self, tmp_path: Path):
        mod = _load()
        errors = mod.validate_directory(_write_track(tmp_path, self._live(items=["first", "Map drops soon"])))
        assert any('"Map drops soon" stub' in e for e in errors)

    def test_live_single_item_stage_rejected(self, tmp_path: Path):
        mod = _load()
        errors = mod.validate_directory(_write_track(tmp_path, self._live(items=["only"], items_ru=["только"])))
        assert any("at least 2 real items" in e for e in errors)

    def test_items_ru_must_mirror_length(self, tmp_path: Path):
        mod = _load()
        errors = mod.validate_directory(
            _write_track(tmp_path, self._live(items_ru=["первый", "второй", "третий"]))
        )
        assert any("must mirror items (2) one-to-one" in e for e in errors)

    def test_bad_items_ru_type(self, tmp_path: Path):
        mod = _load()
        errors = mod.validate_directory(_write_track(tmp_path, self._live(items_ru="not a list")))
        assert any("items_ru must be a non-empty array" in e for e in errors)

    def test_bad_title_ru_type(self, tmp_path: Path):
        mod = _load()
        errors = mod.validate_directory(_write_track(tmp_path, self._live(title_ru="")))
        assert any("title_ru must be a non-empty string" in e for e in errors)
