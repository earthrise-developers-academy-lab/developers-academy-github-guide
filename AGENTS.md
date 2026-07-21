# Agent operating instructions

## Repository purpose

This repository is the reference implementation for issue-first participant onboarding, project and deliverable tracking, accessible leadership review, repository handoff, and long-term Developedia knowledge preservation.

These instructions govern Codex and other coding agents. They are not a participant or repository-steward handbook. Human workflows belong in `PLATFORM_SPEC.md` and later Quarto content. Agents must read `PLATFORM_SPEC.md` before planning or editing.

## Authority and scope

Follow these authorities from highest to lowest:

1. System, developer, execution-environment, and explicit user instructions.
2. Applicable scoped `AGENTS.md` instructions, with the most specific file governing its directory tree.
3. The approved GitHub Issue for the task.
4. `PLATFORM_SPEC.md`.
5. Existing repository documentation, conventions, and tests.

The Issue defines what is authorized for implementation. This file defines how agents conduct that implementation. `PLATFORM_SPEC.md` defines the approved platform architecture, product contract, and exclusions. An Issue does not silently bypass those exclusions. Report conflicts before proceeding rather than choosing an interpretation that expands scope. If Issue context or acceptance criteria cannot be inspected, report that limitation and do not invent them.

## Required reading

Before making a nontrivial change, inspect:

- the applicable `AGENTS.md`;
- the active Issue, its acceptance criteria, and relevant discussion;
- `PLATFORM_SPEC.md`;
- repository files relevant to the change;
- existing tests and validation; and
- current uncommitted changes.

Read only as broadly as needed to understand the authorized change, its dependencies, and existing patterns. Preserve work already present in the repository.

## Planning

Prepare a concise implementation plan before nontrivial edits. Identify:

- files affected;
- existing patterns to follow;
- architectural constraints;
- risks and assumptions;
- validation commands; and
- the smallest implementation that satisfies the Issue.

Revise the plan when inspection changes the expected work. Trivial corrections do not require elaborate planning.

## Scope discipline

- Remain within the active Issue.
- Do not add adjacent features, unrelated cleanup, or speculative refactoring.
- Preserve unrelated user-authored changes.
- Make assumptions, limitations, and unresolved questions visible.
- Do not invent missing product decisions or silently broaden acceptance criteria.
- Request direction when a missing decision would materially change the result.

## Architecture constraints

Use Quarto and Markdown as the default publishing implementation. Prefer static content and structured metadata before custom application code. GitHub Issues are the operational source of truth. Pull requests are the review gate for repository changes. Organization-controlled repositories or approved archives are the durable source for accepted artifacts.

Google Workspace supports drafting and review but is not authoritative for completion. Quarto is a rendering and publication layer, not a task database, and publication does not establish leadership acceptance. Only selected accepted knowledge belongs in Developedia; accepted artifacts do not all require Developedia publication. GitHub Copilot and coding agents are assistive, not authoritative.

Use synthetic data in fixtures and demonstrations. During the initial MVP, translate actionable leadership feedback into GitHub manually.

Unless an approved later Issue explicitly changes the platform contract, do not introduce:

- databases;
- custom backends;
- authentication;
- JavaScript frontend frameworks;
- automatic Google Workspace synchronization;
- automatic GitHub Issue creation from leadership feedback;
- cross-repository content harvesting;
- production participant or partner data; or
- repository provisioning automation.

Report any requested conflict with these constraints before implementation.

## Human-facing implementation constraints

Participant-facing content must:

- assume limited Git experience;
- be task-oriented;
- distinguish Issues, Projects, branches, commits, and pull requests;
- use GitHub Desktop as the default participant interface;
- include clear completion states; and
- explain when to ask a steward for help.

GitHub Desktop is not a universal technical requirement. Stewards, Codex, and advanced contributors may use other Git clients while preserving the same Issue, branch, review, and handoff expectations.

Leadership-facing content must:

- be understandable without GitHub experience;
- show plain-language project and deliverable status;
- identify the artifact under review;
- show acceptance criteria;
- identify the requested decision;
- provide a non-GitHub feedback path or an explicit placeholder; and
- avoid unnecessary repository implementation detail.

## Validation

Use validation proportionate to the change. For a future Quarto implementation, the baseline is:

```text
quarto check
quarto render
git diff --check
```

When Python validation exists, run:

```text
python -m pytest
python scripts/validate_projects.py
```

Report unavailable validation. Never claim that a check passed when it was not run. Review the full diff before completion. Inspect navigation and rendered output whenever they are relevant.

For the initial three-file population task, the only required executable checks are parsing `_quarto.yml` with Python and PyYAML and running `git diff --check`. Also review the complete diff and confirm that no other file changed. Do not render Quarto because content pages do not yet exist.

## Security boundaries

Do not introduce or perform any of the following:

- credentials, tokens, private keys, or service-account files;
- production participant, partner, or restricted project data;
- private Google Workspace links in public synthetic fixtures;
- credentials in browser-delivered JavaScript;
- unauthorized external mutations;
- repository creation or deletion;
- repository visibility changes;
- automatic publishing of GitHub Issues; or
- weakening repository permissions.

## Git behavior

Preserve existing work. Do not use destructive resets, force pushes, or rewrites of unrelated history. When implementation branch work is authorized, use an Issue-specific branch. Keep authorized commits focused and use closing keywords only when the Issue is fully resolved.

Codex must not merge pull requests. Codex must not create branches, commits, pushes, or pull requests unless explicitly authorized for that task.

## Completion report

Report:

1. **Summary**
2. **Files added, modified, or removed**
3. **Commands run**
4. **Validation results**
5. **Acceptance-criteria status**
6. **Known limitations**
7. **Unverified assumptions**
8. **Suggested follow-up Issues**

Explicitly distinguish implementation completion, GitHub Issue acceptance, leadership acceptance, artifact preservation, and Quarto publication. None of these states implies another unless the authoritative record explicitly says so.
