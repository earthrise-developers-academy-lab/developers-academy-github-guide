# Developers Academy GitHub Guide

This repository publishes the Developers Academy onboarding guide and provides a low-risk place to practice the issue-to-branch-to-pull-request workflow.

## Local setup

```cmd
conda activate academy-admin
scripts\setup-guide.cmd
scripts\preview-guide.cmd
```

Open `http://127.0.0.1:8000`.

Validate before committing:

```cmd
scripts\validate-guide.cmd
```

## Publishing

Changes merged into `main` are built and deployed by GitHub Actions.

Configure the repository once at:

```text
Settings -> Pages -> Build and deployment -> Source -> GitHub Actions
```

This repository intentionally does not define local issue forms or a local pull-request template in v0.1. It therefore tests the defaults inherited from the organization's public `.github` repository.
