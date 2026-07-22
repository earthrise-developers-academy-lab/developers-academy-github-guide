"""Validate synthetic practice-submission front matter."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SUBMISSIONS_DIRECTORY = Path("practice/submissions")
PROHIBITED_FIELDS = frozenset(
    {"name", "real-name", "email", "phone", "employer", "contact", "address"}
)


def _relative(path: Path, root: Path) -> str:
    """Return a stable path for validation messages."""

    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _front_matter(path: Path) -> dict[str, Any]:
    """Read one QMD file's YAML front matter without modifying it."""

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


def _normalized_key(value: object) -> str:
    return str(value).strip().casefold().replace("_", "-")


def validate(root: Path = REPOSITORY_ROOT) -> list[str]:
    """Return deterministic errors for QMD files in practice/submissions/."""

    submissions_root = root / SUBMISSIONS_DIRECTORY
    paths = sorted(submissions_root.rglob("*.qmd"))
    errors: list[str] = []

    for path in paths:
        display_path = _relative(path, root)
        try:
            data = _front_matter(path)
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(f"{display_path}: {error}")
            continue

        title = data.get("title")
        if not isinstance(title, str) or not title.strip():
            errors.append(f"{display_path}: field 'title' must be a nonempty string")

        if data.get("synthetic") is not True:
            errors.append(f"{display_path}: field 'synthetic' must be true")

        for key in sorted(data, key=lambda item: str(item)):
            normalized = _normalized_key(key)
            if normalized in PROHIBITED_FIELDS:
                errors.append(
                    f"{display_path}: prohibited front-matter field '{key}'"
                )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Practice submission validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    count = len(list((REPOSITORY_ROOT / SUBMISSIONS_DIRECTORY).rglob("*.qmd")))
    print(f"Practice submission validation passed: {count} submission(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
