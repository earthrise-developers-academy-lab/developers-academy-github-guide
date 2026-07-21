# Contributing

Every change begins with an approved GitHub Issue. The Issue defines the authorized scope and acceptance criteria; `AGENTS.md` defines how coding agents work; `PLATFORM_SPEC.md` defines the platform contract. Report conflicts instead of expanding scope.

## Make a contribution

1. Open or claim the approved Issue and read its acceptance criteria and discussion.
2. Confirm the intended files, current repository state, constraints, and smallest useful change.
3. Create or select an Issue-specific branch. GitHub Desktop is the default participant interface; stewards and advanced contributors may use another Git client.
4. Edit the relevant `.qmd`, metadata, validation, or configuration files. Use synthetic information in examples.
5. Review the changed-file list and diff so unrelated work is not included.
6. Run the validation commands below.
7. Create focused commits and publish the branch.
8. Open a pull request linked to the Issue and include the validation results.
9. Address review feedback, then merge only through the repository's approved human process.

Use a closing keyword such as `Fixes #123` only when merging the pull request will fully resolve that Issue. Codex must not merge pull requests.

## Preview and validate

Install dependencies once in an isolated Python environment:

```text
python -m pip install -r requirements.txt
```

Preview content during drafting:

```text
quarto preview
```

Before requesting review, run:

```text
quarto check
quarto render
python -m pytest
python scripts/validate_projects.py
git diff --check
```

Also inspect navigation, internal links, listings, and the rendered site at desktop and narrow widths. Report any command that was unavailable or not run.

## Content and review boundaries

- GitHub Issues are authoritative for operational and acceptance status; GitHub Projects must reflect them.
- Google Workspace supports drafts and comments but is not authoritative for completion.
- Pull requests are the review gate for repository changes.
- Accepted artifacts must be preserved in an organization-controlled repository or approved archive.
- Quarto publication does not establish leadership acceptance.
- Developedia contains selected accepted knowledge, not every accepted artifact.
- Copilot and coding agents provide assistance that a human must verify.
- Never add credentials, restricted links, or real participant or partner data.

Keep each pull request limited to one issue.
