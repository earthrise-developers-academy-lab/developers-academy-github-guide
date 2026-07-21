"""Validate local synthetic project and deliverable front matter."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

ALLOWED_STATUSES = frozenset(
    {
        "not-started",
        "ready",
        "in-progress",
        "blocked",
        "internal-review",
        "leadership-review",
        "changes-requested",
        "ready-for-repository",
        "pull-request-open",
        "accepted",
        "archived",
    }
)

REQUIRED_REFERENCE_STATUSES = frozenset(
    {"leadership-review", "changes-requested", "accepted"}
)

PROJECT_FIELDS = (
    "title",
    "description",
    "project-id",
    "iteration",
    "owner",
    "steward",
    "phase",
    "synthetic",
)

DELIVERABLE_FIELDS = (
    "title",
    "description",
    "project-id",
    "deliverable-id",
    "status",
    "owner",
    "reviewer",
    "synthetic",
)


def _relative(path: Path, root: Path) -> str:
    """Return a stable path for validation messages."""

    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _front_matter(path: Path) -> dict[str, Any]:
    """Read a Quarto page's YAML front matter without modifying the file."""

    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML front-matter delimiter")

    try:
        closing_index = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration as error:
        raise ValueError("missing closing YAML front-matter delimiter") from error

    try:
        data = yaml.safe_load("\n".join(lines[1:closing_index]))
    except yaml.YAMLError as error:
        raise ValueError(f"invalid YAML front matter: {error}") from error

    if not isinstance(data, dict):
        raise ValueError("YAML front matter must be a mapping")
    return data


def _missing(data: dict[str, Any], field: str) -> bool:
    if field not in data or data[field] is None:
        return True
    return isinstance(data[field], str) and not data[field].strip()


def _load_pages(paths: list[Path], root: Path) -> tuple[list[tuple[Path, dict[str, Any]]], list[str]]:
    pages: list[tuple[Path, dict[str, Any]]] = []
    errors: list[str] = []

    for path in paths:
        try:
            pages.append((path, _front_matter(path)))
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(f"{_relative(path, root)}: {error}")

    return pages, errors


def _check_required_fields(
    pages: list[tuple[Path, dict[str, Any]]],
    required_fields: tuple[str, ...],
    root: Path,
) -> list[str]:
    errors: list[str] = []
    for path, data in pages:
        for field in required_fields:
            if _missing(data, field):
                errors.append(f"{_relative(path, root)}: missing required field '{field}'")
    return errors


def _check_unique_ids(
    pages: list[tuple[Path, dict[str, Any]]], field: str, root: Path
) -> list[str]:
    errors: list[str] = []
    first_path_by_id: dict[str, Path] = {}

    for path, data in pages:
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            if not _missing(data, field):
                errors.append(
                    f"{_relative(path, root)}: field '{field}' must be a non-empty scalar string"
                )
            continue

        if value in first_path_by_id:
            first_path = _relative(first_path_by_id[value], root)
            errors.append(
                f"{_relative(path, root)}: duplicate {field} '{value}'; first declared in {first_path}"
            )
        else:
            first_path_by_id[value] = path

    return errors


def _check_synthetic(
    pages: list[tuple[Path, dict[str, Any]]], root: Path
) -> list[str]:
    return [
        f"{_relative(path, root)}: field 'synthetic' must be true"
        for path, data in pages
        if data.get("synthetic") is not True
    ]


def _check_deliverables(
    pages: list[tuple[Path, dict[str, Any]]], root: Path
) -> list[str]:
    errors: list[str] = []
    observed_statuses: set[str] = set()

    for path, data in pages:
        display_path = _relative(path, root)
        status = data.get("status")

        if not isinstance(status, str):
            if not _missing(data, "status"):
                errors.append(f"{display_path}: field 'status' must be a scalar string")
            continue

        if status not in ALLOWED_STATUSES:
            errors.append(
                f"{display_path}: status '{status}' is not in the approved v0.1 vocabulary"
            )
            continue

        observed_statuses.add(status)

        if status == "leadership-review":
            for field in ("requested-decision", "deadline"):
                if _missing(data, field):
                    errors.append(
                        f"{display_path}: status 'leadership-review' requires field '{field}'"
                    )

        if status == "accepted":
            field = "accepted-artifact"
            target = data.get(field)
            if _missing(data, field):
                errors.append(
                    f"{display_path}: status 'accepted' requires field '{field}'"
                )
                continue
            if not isinstance(target, str):
                errors.append(f"{display_path}: field '{field}' must be a local path string")
                continue

            relative_target = Path(target)
            if relative_target.is_absolute():
                errors.append(f"{display_path}: field '{field}' must be repository-relative")
                continue

            resolved_root = root.resolve()
            resolved_target = (root / relative_target).resolve()
            try:
                resolved_target.relative_to(resolved_root)
            except ValueError:
                errors.append(f"{display_path}: field '{field}' must stay inside the repository")
                continue

            if not resolved_target.is_file():
                errors.append(
                    f"{display_path}: accepted artifact does not exist: {relative_target.as_posix()}"
                )

    for required_status in sorted(REQUIRED_REFERENCE_STATUSES - observed_statuses):
        errors.append(
            f"projects/: required synthetic deliverable status '{required_status}' was not found"
        )

    return errors


def validate(root: Path = REPOSITORY_ROOT) -> list[str]:
    """Return deterministic validation errors for the repository rooted at *root*."""

    project_paths = sorted((root / "projects").glob("*/index.qmd"))
    deliverable_paths = sorted((root / "projects").glob("*/deliverables/*.qmd"))

    projects, project_errors = _load_pages(project_paths, root)
    deliverables, deliverable_errors = _load_pages(deliverable_paths, root)

    errors = [*project_errors, *deliverable_errors]
    errors.extend(_check_required_fields(projects, PROJECT_FIELDS, root))
    errors.extend(_check_required_fields(deliverables, DELIVERABLE_FIELDS, root))
    errors.extend(_check_unique_ids(projects, "project-id", root))
    errors.extend(_check_unique_ids(deliverables, "deliverable-id", root))
    errors.extend(_check_synthetic(projects, root))
    errors.extend(_check_synthetic(deliverables, root))
    errors.extend(_check_deliverables(deliverables, root))
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Project metadata validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    project_count = len(list((REPOSITORY_ROOT / "projects").glob("*/index.qmd")))
    deliverable_count = len(
        list((REPOSITORY_ROOT / "projects").glob("*/deliverables/*.qmd"))
    )
    print(
        f"Project metadata validation passed: {project_count} project(s), "
        f"{deliverable_count} deliverable(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
