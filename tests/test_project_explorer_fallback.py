from __future__ import annotations

import json
from pathlib import Path

from scripts.build_project_explorer_fallback import main, render_fallback


def _write_data(root: Path) -> None:
    (root / "data").mkdir()
    projects = {
        "projects": [
            {
                "project_id": "DA-EO-001", "title": "Escaped <title>",
                "start_year": 2024, "end_year": 2025, "cohorts": ["Pilot A"],
                "topics": ["water-resources"], "status": "completed",
                "project_type": "analysis", "handoff_status": "accepted",
                "developedia_url": "projects/example/index.html",
            },
            {
                "project_id": "DA-EO-002", "title": "No geometry",
                "start_year": 2026, "end_year": None, "cohorts": ["Pilot B"],
                "topics": ["education-outreach"], "status": "active",
                "project_type": "training", "handoff_status": "draft",
            },
        ]
    }
    areas = {
        "features": [
            {"properties": {"project_id": "DA-EO-001", "label": "Area <one>", "geometry_representation": "broad-service-region", "geometry_precision": "generalized"}},
            {"properties": {"project_id": "DA-EO-001", "label": "Area two", "geometry_representation": "representative-location", "geometry_precision": "representative"}},
        ]
    }
    (root / "data/projects.json").write_text(json.dumps(projects), encoding="utf-8")
    (root / "data/project-service-areas.geojson").write_text(json.dumps(areas), encoding="utf-8")


def test_fallback_is_deterministic_escaped_and_complete(tmp_path: Path) -> None:
    _write_data(tmp_path)

    first = render_fallback(tmp_path)
    second = render_fallback(tmp_path)

    assert first == second
    assert "Escaped &lt;title&gt;" in first
    assert "Area &lt;one&gt;; Area two" in first
    assert "No mapped service area" in first
    assert "broad-service-region, representative-location" in first
    assert "generalized, representative" in first
    assert 'href="projects/example/index.html"' in first
    assert 'data-project-id="DA-EO-001"' in first
    assert 'data-project-id="DA-EO-002"' in first
    assert "Synthetic demonstration record" in first
    assert "<caption>" in first and 'scope="col"' in first and 'scope="row"' in first


def test_generate_and_check_mode_success(tmp_path: Path) -> None:
    _write_data(tmp_path)

    assert main([], tmp_path) == 0
    assert main(["--check"], tmp_path) == 0


def test_check_mode_fails_when_output_is_missing(tmp_path: Path) -> None:
    _write_data(tmp_path)

    assert main(["--check"], tmp_path) == 1


def test_check_mode_fails_when_output_is_stale(tmp_path: Path) -> None:
    _write_data(tmp_path)
    assert main([], tmp_path) == 0
    (tmp_path / "_generated/project-explorer-table.html").write_text("stale", encoding="utf-8")

    assert main(["--check"], tmp_path) == 1
