from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path

import pytest

from scripts.validate_project_map_data import REPOSITORY_ROOT, validate


def _copy_valid_tree(root: Path) -> None:
    for relative in (
        "data/projects.json",
        "data/project-service-areas.geojson",
        "data/reference/natural-earth-land-110m.geojson",
        "data/reference/README.md",
        "schemas/projects.schema.json",
        "schemas/project-service-areas.schema.json",
    ):
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPOSITORY_ROOT / relative, target)
    shutil.copytree(
        REPOSITORY_ROOT / "assets/vendor/leaflet/1.9.4",
        root / "assets/vendor/leaflet/1.9.4",
    )
    for relative in ("projects/da-eo-001/index.qmd", "projects/da-eo-001/handoff.qmd"):
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("Synthetic local target.\n", encoding="utf-8")


def _read(root: Path, relative: str) -> dict[str, object]:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def _write(root: Path, relative: str, value: object) -> None:
    (root / relative).write_text(json.dumps(value), encoding="utf-8")


def test_complete_valid_registry_and_service_areas_pass(tmp_path: Path) -> None:
    _copy_valid_tree(tmp_path)

    assert validate(tmp_path) == []

    registry = _read(tmp_path, "data/projects.json")
    areas = _read(tmp_path, "data/project-service-areas.geojson")
    assert any(project["handoff_status"] == "accepted" and project["handoff_url"] for project in registry["projects"])
    assert any(project["status"] == "continued" and len(project["cohorts"]) > 1 for project in registry["projects"])
    mapped_ids = {feature["properties"]["project_id"] for feature in areas["features"]}
    assert any(project["project_id"] not in mapped_ids for project in registry["projects"])
    assert len([feature for feature in areas["features"] if feature["properties"]["project_id"] == "DA-EO-010"]) == 2
    assert {feature["geometry"]["type"] for feature in areas["features"]} == {"Point", "MultiPoint", "Polygon", "MultiPolygon"}


def test_malformed_project_json_is_reported(tmp_path: Path) -> None:
    _copy_valid_tree(tmp_path)
    (tmp_path / "data/projects.json").write_text("{broken", encoding="utf-8")

    assert any("data/projects.json" in error for error in validate(tmp_path))


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        (lambda p: p.pop("summary"), "required property"),
        (lambda p: p.update(start_year=2030, end_year=2020), "end_year must be"),
        (lambda p: p.update(status="completed", end_year=None), "require end_year"),
        (lambda p: p.update(status="continued", cohorts=["Only cohort"]), "at least two cohorts"),
        (lambda p: p.update(topics=["unknown-topic"]), "unknown-topic"),
        (lambda p: p.update(project_type="unknown"), "unknown"),
        (lambda p: p.update(status="unknown"), "unknown"),
        (lambda p: p.update(handoff_status="accepted", handoff_url=None), "handoff_url"),
        (lambda p: p.update(synthetic=False), "synthetic"),
        (lambda p: p.update(developedia_url="missing/local.html"), "local target does not exist"),
        (lambda p: p.update(application_url="javascript:alert(1)"), "credential-free HTTPS"),
    ],
)
def test_invalid_project_records_are_rejected(tmp_path: Path, mutation, expected: str) -> None:
    _copy_valid_tree(tmp_path)
    registry = _read(tmp_path, "data/projects.json")
    project = copy.deepcopy(registry["projects"][1])
    mutation(project)
    registry["projects"] = [project]
    _write(tmp_path, "data/projects.json", registry)

    assert any(expected in error for error in validate(tmp_path))


def test_duplicate_project_id_is_rejected(tmp_path: Path) -> None:
    _copy_valid_tree(tmp_path)
    registry = _read(tmp_path, "data/projects.json")
    registry["projects"].append(copy.deepcopy(registry["projects"][0]))
    _write(tmp_path, "data/projects.json", registry)

    assert any("duplicate project_id" in error for error in validate(tmp_path))


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        (lambda f: f.update(id="other"), "feature id must equal"),
        (lambda f: f["properties"].update(project_id="DA-EO-999"), "does not join"),
        (lambda f: f["geometry"].update(type="LineString"), "not valid under"),
        (lambda f: f["geometry"].update(coordinates=[[181, 0]]), "not valid under"),
        (lambda f: f["geometry"].update(coordinates=[[0, 91]]), "not valid under"),
        (lambda f: f["properties"].pop("geometry_source"), "required property"),
        (lambda f: f["properties"].pop("geometry_precision"), "required property"),
        (lambda f: f["properties"].update(geometry_representation="representative-location", geometry_precision="generalized"), "representative precision"),
        (lambda f: f["properties"].update(geometry_representation="generalized-location", geometry_precision="representative"), "generalized precision"),
        (lambda f: f["properties"].update(geometry_representation="exact-project-boundary", geometry_precision="exact"), "may not use exact-project-boundary"),
    ],
)
def test_invalid_service_areas_are_rejected(tmp_path: Path, mutation, expected: str) -> None:
    _copy_valid_tree(tmp_path)
    areas = _read(tmp_path, "data/project-service-areas.geojson")
    feature = copy.deepcopy(areas["features"][0])
    mutation(feature)
    areas["features"] = [feature]
    _write(tmp_path, "data/project-service-areas.geojson", areas)

    assert any(expected in error for error in validate(tmp_path))


def test_duplicate_service_area_and_unclosed_ring_are_rejected(tmp_path: Path) -> None:
    _copy_valid_tree(tmp_path)
    areas = _read(tmp_path, "data/project-service-areas.geojson")
    duplicate = copy.deepcopy(areas["features"][1])
    areas["features"] = [areas["features"][1], duplicate]
    areas["features"][0]["geometry"]["coordinates"][0][-1] = [-99, 39]
    _write(tmp_path, "data/project-service-areas.geojson", areas)

    errors = validate(tmp_path)
    assert any("duplicate service_area_id" in error for error in errors)
    assert any("polygon rings must be closed" in error for error in errors)


@pytest.mark.parametrize(
    ("relative", "expected"),
    [
        ("assets/vendor/leaflet/1.9.4/LICENSE", "LICENSE: missing"),
        ("assets/vendor/leaflet/1.9.4/VERSION", "expected 1.9.4"),
        ("data/reference/README.md", "Natural Earth provenance"),
    ],
)
def test_missing_dependency_metadata_is_rejected(tmp_path: Path, relative: str, expected: str) -> None:
    _copy_valid_tree(tmp_path)
    (tmp_path / relative).unlink()

    assert any(expected in error for error in validate(tmp_path))


def test_leaflet_checksum_mismatch_is_rejected(tmp_path: Path) -> None:
    _copy_valid_tree(tmp_path)
    (tmp_path / "assets/vendor/leaflet/1.9.4/leaflet.js").write_text("changed", encoding="utf-8")

    assert any("leaflet.js: checksum mismatch" in error for error in validate(tmp_path))
