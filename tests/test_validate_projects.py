from __future__ import annotations

from pathlib import Path

import yaml

from scripts.validate_projects import ALLOWED_STATUSES, validate


PROJECT = {
    "title": "Synthetic project",
    "description": "A test-only project.",
    "project-id": "TEST-001",
    "iteration": "Synthetic pilot",
    "owner": "Fictional Owner",
    "steward": "Fictional Steward",
    "phase": "Synthetic review",
    "synthetic": True,
}


def _write_page(path: Path, metadata: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    front_matter = yaml.safe_dump(metadata, sort_keys=False).strip()
    path.write_text(f"---\n{front_matter}\n---\n\nSynthetic test page.\n", encoding="utf-8")


def _deliverable(identifier: str, status: object) -> dict[str, object]:
    data: dict[str, object] = {
        "title": f"Synthetic deliverable {identifier}",
        "description": "A test-only deliverable.",
        "project-id": "TEST-001",
        "deliverable-id": identifier,
        "status": status,
        "owner": "Fictional Owner",
        "reviewer": "Fictional Reviewer",
        "synthetic": True,
    }
    if status == "leadership-review":
        data["requested-decision"] = "Choose a fictional option."
        data["deadline"] = "2030-01-15 (fictional)"
    if status == "accepted":
        data["accepted-artifact"] = (
            "projects/test-001/deliverables/test-001-d03.qmd"
        )
    return data


def _valid_tree(root: Path) -> None:
    _write_page(root / "projects/test-001/index.qmd", PROJECT)
    _write_page(
        root / "projects/test-001/deliverables/test-001-d01.qmd",
        _deliverable("TEST-001-D01", "leadership-review"),
    )
    _write_page(
        root / "projects/test-001/deliverables/test-001-d02.qmd",
        _deliverable("TEST-001-D02", "changes-requested"),
    )
    _write_page(
        root / "projects/test-001/deliverables/test-001-d03.qmd",
        _deliverable("TEST-001-D03", "accepted"),
    )


def test_status_allowlist_is_exact() -> None:
    assert ALLOWED_STATUSES == {
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


def test_valid_reference_metadata_passes(tmp_path: Path) -> None:
    _valid_tree(tmp_path)

    assert validate(tmp_path) == []


def test_reports_missing_field_and_duplicate_id(tmp_path: Path) -> None:
    _valid_tree(tmp_path)
    duplicate = _deliverable("TEST-001-D02", "in-progress")
    duplicate.pop("reviewer")
    duplicate_path = tmp_path / "projects/test-001/deliverables/zz-duplicate.qmd"
    _write_page(duplicate_path, duplicate)

    errors = validate(tmp_path)

    assert any("zz-duplicate.qmd: missing required field 'reviewer'" in error for error in errors)
    assert any("zz-duplicate.qmd: duplicate deliverable-id 'TEST-001-D02'" in error for error in errors)


def test_rejects_non_scalar_and_unapproved_statuses(tmp_path: Path) -> None:
    _valid_tree(tmp_path)
    first_path = tmp_path / "projects/test-001/deliverables/test-001-d01.qmd"
    second_path = tmp_path / "projects/test-001/deliverables/test-001-d02.qmd"
    _write_page(first_path, _deliverable("TEST-001-D01", ["leadership-review"]))
    _write_page(second_path, _deliverable("TEST-001-D02", "reviewing"))

    errors = validate(tmp_path)

    assert any("test-001-d01.qmd: field 'status' must be a scalar string" in error for error in errors)
    assert any("test-001-d02.qmd: status 'reviewing' is not in the approved" in error for error in errors)


def test_requires_synthetic_true(tmp_path: Path) -> None:
    _valid_tree(tmp_path)
    unsafe_project = {**PROJECT, "synthetic": False}
    _write_page(tmp_path / "projects/test-001/index.qmd", unsafe_project)

    errors = validate(tmp_path)

    assert any("projects/test-001/index.qmd: field 'synthetic' must be true" == error for error in errors)


def test_leadership_review_requires_conditional_fields(tmp_path: Path) -> None:
    _valid_tree(tmp_path)
    incomplete = _deliverable("TEST-001-D01", "leadership-review")
    incomplete.pop("requested-decision")
    incomplete.pop("deadline")
    _write_page(
        tmp_path / "projects/test-001/deliverables/test-001-d01.qmd", incomplete
    )

    errors = validate(tmp_path)

    assert any("requires field 'requested-decision'" in error for error in errors)
    assert any("requires field 'deadline'" in error for error in errors)


def test_accepted_artifact_must_be_local_and_exist(tmp_path: Path) -> None:
    _valid_tree(tmp_path)
    accepted = _deliverable("TEST-001-D03", "accepted")
    accepted["accepted-artifact"] = "projects/test-001/missing.qmd"
    _write_page(
        tmp_path / "projects/test-001/deliverables/test-001-d03.qmd", accepted
    )

    errors = validate(tmp_path)

    assert any("accepted artifact does not exist: projects/test-001/missing.qmd" in error for error in errors)


def test_requires_all_three_reference_states(tmp_path: Path) -> None:
    _valid_tree(tmp_path)
    changed = _deliverable("TEST-001-D02", "in-progress")
    _write_page(
        tmp_path / "projects/test-001/deliverables/test-001-d02.qmd", changed
    )

    errors = validate(tmp_path)

    assert "projects/: required synthetic deliverable status 'changes-requested' was not found" in errors
