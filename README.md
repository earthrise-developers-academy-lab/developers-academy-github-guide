# Developers Academy Platform

This repository is the v0.1 reference implementation for issue-first Developers Academy onboarding, project and deliverable tracking, accessible leadership review, repository handoff, and selective long-term Developedia knowledge preservation.

The website is intentionally static. GitHub Issues remain authoritative for active work, blockers, decisions, acceptance criteria, and recorded acceptance. GitHub Projects summarize Issue state. Google Workspace may support drafting and comments, but it does not establish completion. Pull requests gate repository changes, and accepted artifacts belong in an organization-controlled repository or approved archive. Quarto publication, leadership acceptance, Issue acceptance, artifact preservation, and Developedia curation are separate events.

All project records, people, dates, locations, findings, and feedback in the reference lifecycle are fictional and synthetic.

## Prerequisites

- [Quarto](https://quarto.org/docs/get-started/) 1.9 or a compatible newer release
- Python 3.13 or a compatible supported release
- GitHub Desktop for the default participant Git workflow; stewards and advanced contributors may use another Git client

Install the Python validation dependencies in an isolated environment:

```text
python -m pip install -r requirements.txt
```

## Preview locally

From the repository root, check Quarto and start the preview server:

```text
quarto check
quarto preview
```

The preview command prints a local address. Stop it with `Ctrl+C`. Quarto writes generated output to `_site/`; generated output is ignored and must not be committed.

## Validate changes

Run the complete local validation sequence:

```text
quarto check
quarto render
python -m pytest
python scripts/validate_projects.py
git diff --check
```

The metadata validator reads local project and deliverable front matter only. It performs no network requests and writes no files.

## Key pages

- [Home](index.qmd) explains the platform and its sources of truth.
- [Start here](start-here.qmd) guides a participant from an Issue through progress and blocker updates.
- [First pull request](first-pull-request.qmd) uses GitHub Desktop as the default participant interface.
- [Troubleshoot with Copilot](copilot-troubleshooting.qmd) demonstrates evidence-based, human-reviewed assistance.
- [Projects](projects/index.qmd) lists the synthetic reference project and its deliverables.
- [Leadership review](projects/da-eo-001/deliverables/priority-locations-decision-brief.qmd) shows a static, non-GitHub review surface.
- [Repository stewards](stewards.qmd) covers scoping, support, review, preservation, and handoff.

## Contribution workflow

Begin with an approved GitHub Issue, make the smallest change that satisfies its acceptance criteria, validate locally, and submit repository changes through a reviewed pull request. See [CONTRIBUTING.md](CONTRIBUTING.md) for the complete workflow.

## GitHub Pages publication

`.github/workflows/publish-guide.yml` validates pull requests and builds pushes to `main`. It deploys `_site` to GitHub Pages only for a push to `main` or a manual run selected from `main`. Publishing the static site neither records leadership acceptance nor changes an Issue.

Repository administrators must enable GitHub Pages with **GitHub Actions** as the source before the first deployment can succeed. This repository does not change that setting automatically.

## Migration from MkDocs

Quarto replaces the former MkDocs implementation. The useful guidance formerly stored under `docs/` is now incorporated into the `.qmd` pages above. Do not use `mkdocs.yml`, `mkdocs build`, the old batch scripts, or the legacy `site/` output. Quarto source lives at the repository root and under `projects/`; generated output lives in `_site/`.
