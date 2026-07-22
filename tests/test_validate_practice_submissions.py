from __future__ import annotations

from pathlib import Path

import yaml

from scripts.validate_practice_submissions import validate


def _write_submission(
    root: Path,
    filename: str,
    metadata: dict[str, object],
    body: str = "Synthetic practice submission.",
) -> Path:
    path = root / "practice/submissions" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    front_matter = yaml.safe_dump(metadata, sort_keys=False).strip()
    path.write_text(f"---\n{front_matter}\n---\n\n{body}\n", encoding="utf-8")
    return path


def test_valid_synthetic_submission_passes(tmp_path: Path) -> None:
    _write_submission(
        tmp_path,
        "participant-example.qmd",
        {"title": "Onboarding practice — participant-example", "synthetic": True},
    )

    assert validate(tmp_path) == []


def test_missing_title_is_rejected(tmp_path: Path) -> None:
    _write_submission(tmp_path, "missing-title.qmd", {"synthetic": True})

    assert validate(tmp_path) == [
        "practice/submissions/missing-title.qmd: field 'title' must be a nonempty string"
    ]


def test_missing_synthetic_is_rejected(tmp_path: Path) -> None:
    _write_submission(tmp_path, "missing-synthetic.qmd", {"title": "Synthetic example"})

    assert validate(tmp_path) == [
        "practice/submissions/missing-synthetic.qmd: field 'synthetic' must be true"
    ]


def test_synthetic_false_is_rejected(tmp_path: Path) -> None:
    _write_submission(
        tmp_path,
        "unsafe.qmd",
        {"title": "Unsafe example", "synthetic": False},
    )

    assert validate(tmp_path) == [
        "practice/submissions/unsafe.qmd: field 'synthetic' must be true"
    ]


def test_prohibited_metadata_field_is_rejected(tmp_path: Path) -> None:
    _write_submission(
        tmp_path,
        "contact.qmd",
        {
            "title": "Synthetic example",
            "synthetic": True,
            "real-name": "Do not collect",
        },
    )

    assert validate(tmp_path) == [
        "practice/submissions/contact.qmd: prohibited front-matter field 'real-name'"
    ]


def test_malformed_front_matter_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "practice/submissions/malformed.qmd"
    path.parent.mkdir(parents=True)
    path.write_text("---\ntitle: [unclosed\n---\n", encoding="utf-8")

    errors = validate(tmp_path)

    assert len(errors) == 1
    assert errors[0].startswith(
        "practice/submissions/malformed.qmd: invalid YAML front matter:"
    )


def test_multiple_submission_files_are_all_validated(tmp_path: Path) -> None:
    _write_submission(
        tmp_path,
        "a-valid.qmd",
        {"title": "Synthetic A", "synthetic": True},
    )
    _write_submission(
        tmp_path,
        "b-invalid.qmd",
        {"title": "Synthetic B", "synthetic": True, "email": "not-allowed"},
    )

    assert validate(tmp_path) == [
        "practice/submissions/b-invalid.qmd: prohibited front-matter field 'email'"
    ]
