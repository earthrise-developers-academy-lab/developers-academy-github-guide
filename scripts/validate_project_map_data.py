"""Validate project-explorer data, provenance, and vendored dependencies."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEAFLET_FILES = frozenset(
    {
        "leaflet.css", "leaflet.js", "LICENSE", "images/layers.png",
        "images/layers-2x.png", "images/marker-icon.png",
        "images/marker-icon-2x.png", "images/marker-shadow.png",
    }
)
URL_FIELDS = ("repository_url", "application_url", "developedia_url", "handoff_url")
SYNTHETIC_GEOMETRY_SOURCE = "Synthetic generalized geometry created for Issue #5 demonstration; not a real project service area."
SYNTHETIC_SOURCE_RIGHTS = "Not applicable — synthetic demonstration geometry with no external boundary source."


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _load_json(path: Path, root: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        errors.append(f"{_relative(path, root)}: {error}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{_relative(path, root)}: top-level value must be an object")
        return None
    return value


def _schema_errors(data: dict[str, Any], schema: dict[str, Any], label: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for error in sorted(validator.iter_errors(data), key=lambda item: tuple(str(part) for part in item.absolute_path)):
        path = ".".join(str(part) for part in error.absolute_path) or "$"
        errors.append(f"{label}:{path}: {error.message}")
    return errors


def _check_url(value: str, root: Path, display: str) -> list[str]:
    parsed = urlparse(value)
    if parsed.scheme:
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
            return [f"{display}: external URL must use credential-free HTTPS"]
        if (parsed.hostname or "").casefold() in {"localhost", "127.0.0.1", "::1"}:
            return [f"{display}: localhost URLs are prohibited"]
        return []
    if value.startswith(("/", "\\")) or ".." in Path(value).parts:
        return [f"{display}: local URL must be repository-relative and stay inside the repository"]
    source_target = root / Path(value)
    if source_target.suffix == ".html":
        source_target = source_target.with_suffix(".qmd")
    if not source_target.is_file():
        return [f"{display}: local target does not exist: {value}"]
    return []


def _positions(geometry: dict[str, Any]) -> Iterable[list[float]]:
    kind = geometry.get("type")
    coordinates = geometry.get("coordinates", [])
    if kind == "Point":
        yield coordinates
    elif kind == "MultiPoint":
        yield from coordinates
    elif kind == "Polygon":
        for ring in coordinates:
            yield from ring
    elif kind == "MultiPolygon":
        for polygon in coordinates:
            for ring in polygon:
                yield from ring


def _rings(geometry: dict[str, Any]) -> Iterable[list[list[float]]]:
    if geometry.get("type") == "Polygon":
        yield from geometry.get("coordinates", [])
    elif geometry.get("type") == "MultiPolygon":
        for polygon in geometry.get("coordinates", []):
            yield from polygon


def _validate_projects(registry: dict[str, Any], root: Path) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    projects = registry.get("projects", [])
    ids = [project.get("project_id") for project in projects if isinstance(project, dict)]
    for project_id in sorted({value for value in ids if ids.count(value) > 1 and isinstance(value, str)}):
        errors.append(f"data/projects.json: duplicate project_id '{project_id}'")
    for index, project in enumerate(projects):
        if not isinstance(project, dict):
            continue
        label = f"data/projects.json:projects.{index}"
        start, end = project.get("start_year"), project.get("end_year")
        if isinstance(start, int) and isinstance(end, int) and end < start:
            errors.append(f"{label}: end_year must be greater than or equal to start_year")
        if project.get("status") in {"completed", "archived"} and end is None:
            errors.append(f"{label}: completed and archived projects require end_year")
        if project.get("status") == "continued" and len(project.get("cohorts", [])) < 2:
            errors.append(f"{label}: continued projects require at least two cohorts")
        if project.get("handoff_status") in {"accepted", "archived"} and not project.get("handoff_url"):
            errors.append(f"{label}: accepted or archived handoff requires handoff_url")
        if project.get("synthetic") is not True:
            errors.append(f"{label}: synthetic must be true")
        for field in URL_FIELDS:
            value = project.get(field)
            if isinstance(value, str):
                errors.extend(_check_url(value, root, f"{label}.{field}"))
    return errors, {value for value in ids if isinstance(value, str)}


def _validate_service_areas(collection: dict[str, Any], project_ids: set[str]) -> list[str]:
    errors: list[str] = []
    features = collection.get("features", [])
    feature_ids = [feature.get("id") for feature in features if isinstance(feature, dict)]
    service_ids = [feature.get("properties", {}).get("service_area_id") for feature in features if isinstance(feature, dict) and isinstance(feature.get("properties"), dict)]
    for value in sorted({item for item in feature_ids if feature_ids.count(item) > 1 and isinstance(item, str)}):
        errors.append(f"data/project-service-areas.geojson: duplicate feature id '{value}'")
    for value in sorted({item for item in service_ids if service_ids.count(item) > 1 and isinstance(item, str)}):
        errors.append(f"data/project-service-areas.geojson: duplicate service_area_id '{value}'")
    for index, feature in enumerate(features):
        if not isinstance(feature, dict):
            continue
        label = f"data/project-service-areas.geojson:features.{index}"
        properties = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        if not isinstance(properties, dict) or not isinstance(geometry, dict):
            continue
        if feature.get("id") != properties.get("service_area_id"):
            errors.append(f"{label}: feature id must equal service_area_id")
        if properties.get("project_id") not in project_ids:
            errors.append(f"{label}: project_id does not join to the registry")
        representation = properties.get("geometry_representation")
        precision = properties.get("geometry_precision")
        if representation == "representative-location" and precision != "representative":
            errors.append(f"{label}: representative-location requires representative precision")
        if representation == "generalized-location" and precision != "generalized":
            errors.append(f"{label}: generalized-location requires generalized precision")
        if representation == "broad-service-region" and precision not in {"generalized", "approximate"}:
            errors.append(f"{label}: broad-service-region requires generalized or approximate precision")
        if properties.get("synthetic") is True and representation == "exact-project-boundary":
            errors.append(f"{label}: synthetic features may not use exact-project-boundary")
        if properties.get("geometry_source") != SYNTHETIC_GEOMETRY_SOURCE:
            errors.append(f"{label}: required synthetic geometry provenance statement is missing")
        if properties.get("source_license") != SYNTHETIC_SOURCE_RIGHTS:
            errors.append(f"{label}: required synthetic source-rights statement is missing")
        for position in _positions(geometry):
            if not isinstance(position, list) or len(position) < 2:
                errors.append(f"{label}: geometry contains an invalid position")
                continue
            longitude, latitude = position[0], position[1]
            if not isinstance(longitude, (int, float)) or not -180 <= longitude <= 180:
                errors.append(f"{label}: longitude is outside -180..180")
            if not isinstance(latitude, (int, float)) or not -90 <= latitude <= 90:
                errors.append(f"{label}: latitude is outside -90..90")
        for ring in _rings(geometry):
            if not ring or ring[0] != ring[-1]:
                errors.append(f"{label}: polygon rings must be closed")
    return errors


def _validate_dependencies(root: Path) -> list[str]:
    errors: list[str] = []
    vendor = root / "assets/vendor/leaflet/1.9.4"
    version = vendor / "VERSION"
    license_path = vendor / "LICENSE"
    checksums = vendor / "SHA256SUMS"
    if not version.is_file() or version.read_text(encoding="utf-8").strip() != "1.9.4":
        errors.append("assets/vendor/leaflet/1.9.4/VERSION: expected 1.9.4")
    if not license_path.is_file():
        errors.append("assets/vendor/leaflet/1.9.4/LICENSE: missing")
    expected: dict[str, str] = {}
    if not checksums.is_file():
        errors.append("assets/vendor/leaflet/1.9.4/SHA256SUMS: missing")
    else:
        for line in checksums.read_text(encoding="utf-8").splitlines():
            digest, separator, relative_path = line.partition("  ")
            if not separator:
                errors.append("assets/vendor/leaflet/1.9.4/SHA256SUMS: invalid line")
                continue
            expected[relative_path] = digest
        if set(expected) != EXPECTED_LEAFLET_FILES:
            errors.append("assets/vendor/leaflet/1.9.4/SHA256SUMS: runtime file inventory mismatch")
        for relative_path, digest in expected.items():
            path = vendor / relative_path
            if not path.is_file():
                errors.append(f"assets/vendor/leaflet/1.9.4/{relative_path}: missing")
            elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                errors.append(f"assets/vendor/leaflet/1.9.4/{relative_path}: checksum mismatch")
    for relative_path in ("data/reference/natural-earth-land-110m.geojson", "data/reference/README.md"):
        if not (root / relative_path).is_file():
            errors.append(f"{relative_path}: missing Natural Earth provenance asset")
    return errors


def validate(root: Path = REPOSITORY_ROOT) -> list[str]:
    errors: list[str] = []
    projects_schema = _load_json(root / "schemas/projects.schema.json", root, errors)
    service_schema = _load_json(root / "schemas/project-service-areas.schema.json", root, errors)
    registry = _load_json(root / "data/projects.json", root, errors)
    service_areas = _load_json(root / "data/project-service-areas.geojson", root, errors)
    if projects_schema is not None and registry is not None:
        errors.extend(_schema_errors(registry, projects_schema, "data/projects.json"))
    if service_schema is not None and service_areas is not None:
        errors.extend(_schema_errors(service_areas, service_schema, "data/project-service-areas.geojson"))
    project_ids: set[str] = set()
    if registry is not None:
        project_errors, project_ids = _validate_projects(registry, root)
        errors.extend(project_errors)
    if service_areas is not None:
        errors.extend(_validate_service_areas(service_areas, project_ids))
    errors.extend(_validate_dependencies(root))
    return sorted(errors)


def main() -> int:
    errors = validate()
    if errors:
        print("Project-map data validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Project-map data validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
