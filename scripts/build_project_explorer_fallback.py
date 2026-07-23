"""Build the deterministic semantic fallback table for the project explorer."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = Path("_generated/project-explorer-table.html")
SYNTHETIC_STATEMENT = "Synthetic demonstration record — not an actual Developers Academy project."


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.as_posix()}: top-level value must be an object")
    return data


def _text(value: object) -> str:
    return html.escape(str(value), quote=True)


def _year_range(project: dict[str, Any]) -> str:
    start = project["start_year"]
    end = project.get("end_year")
    if end is None:
        return f"{start}–ongoing"
    if end == start:
        return str(start)
    return f"{start}–{end}"


def _geography_by_project(service_areas: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    summaries: dict[str, list[dict[str, Any]]] = {}
    for feature in service_areas.get("features", []):
        properties = feature.get("properties", {})
        project_id = properties.get("project_id")
        label = properties.get("label")
        if not isinstance(project_id, str) or not isinstance(label, str) or not label:
            raise ValueError("service-area feature requires string project_id and label")
        summaries.setdefault(project_id, []).append(properties)
    return summaries


def _detail_link(project: dict[str, Any]) -> str:
    target = project.get("developedia_url") or project.get("handoff_url")
    if not target:
        return "Not available"
    return f'<a href="{_text(target)}">Open local project record</a>'


def render_fallback(root: Path = REPOSITORY_ROOT) -> str:
    registry = _load_json(root / "data/projects.json")
    service_areas = _load_json(root / "data/project-service-areas.geojson")
    projects = registry.get("projects")
    if not isinstance(projects, list):
        raise ValueError("data/projects.json: projects must be an array")
    geography = _geography_by_project(service_areas)

    lines = [
        '<table id="project-explorer-table" class="project-explorer-table">',
        '<caption>All synthetic project records; this table remains available without JavaScript.</caption>',
        '<thead><tr>',
        '<th scope="col">Project</th><th scope="col">Years</th><th scope="col">Cohorts</th>',
        '<th scope="col">Topics</th><th scope="col">Status</th><th scope="col">Type</th>',
        '<th scope="col">Handoff</th><th scope="col">Geography summary</th>',
        '<th scope="col">Representation</th><th scope="col">Precision</th>',
        '<th scope="col">Local record</th><th scope="col">Record notice</th>',
        '</tr></thead><tbody>',
    ]
    for project in sorted(projects, key=lambda item: item["project_id"]):
        project_id = project["project_id"]
        areas = geography.get(project_id, [])
        geography_summary = "; ".join(area["label"] for area in areas) if areas else "No mapped service area"
        representations = ", ".join(sorted({area["geometry_representation"] for area in areas})) if areas else "None"
        precisions = ", ".join(sorted({area["geometry_precision"] for area in areas})) if areas else "None"
        lines.extend(
            [
                f'<tr id="project-row-{_text(project_id.lower())}" data-project-id="{_text(project_id)}">',
                f'<th scope="row"><span class="project-id">{_text(project_id)}</span><br>{_text(project["title"])} '
                f'<button type="button" class="project-detail-button" data-project-id="{_text(project_id)}" hidden>View details</button></th>',
                f'<td>{_text(_year_range(project))}</td>',
                f'<td>{_text(", ".join(project["cohorts"]))}</td>',
                f'<td>{_text(", ".join(project["topics"]))}</td>',
                f'<td>{_text(project["status"])}</td>',
                f'<td>{_text(project["project_type"])}</td>',
                f'<td>{_text(project["handoff_status"])}</td>',
                f'<td>{_text(geography_summary)}</td>',
                f'<td>{_text(representations)}</td>',
                f'<td>{_text(precisions)}</td>',
                f'<td>{_detail_link(project)}</td>',
                f'<td>{_text(SYNTHETIC_STATEMENT)}</td>',
                '</tr>',
            ]
        )
    lines.append('</tbody></table>')
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None, root: Path = REPOSITORY_ROOT) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    output_path = root / OUTPUT_PATH
    try:
        expected = render_fallback(root)
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"Fallback generation failed: {error}", file=sys.stderr)
        return 1

    if args.check:
        if not output_path.is_file():
            print(f"Fallback is missing: {OUTPUT_PATH.as_posix()}", file=sys.stderr)
            return 1
        if output_path.read_text(encoding="utf-8") != expected:
            print(f"Fallback is stale: {OUTPUT_PATH.as_posix()}", file=sys.stderr)
            return 1
        print("Project explorer fallback is current.")
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(expected, encoding="utf-8", newline="\n")
    print(f"Generated {OUTPUT_PATH.as_posix()}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
