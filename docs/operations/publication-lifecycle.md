# Website publication lifecycle

## Operating states

The default state is **stored and unpublished**: source and validated build evidence may exist in GitHub, but the GitHub Pages URL should be offline. Ordinary visual development is **local-only** and uses:

```text
quarto preview
```

A **temporary remote preview** is a deliberate public GitHub Pages deployment used only for Pages-path verification, Actions-built output verification, remote browser or device testing, or a specifically authorized review session. It must be unpublished as soon as that test ends.

These access models are distinct:

- A **private repository** restricts repository source access but does not, by itself, make a GitHub Pages deployment private.
- A conventional **public Pages deployment** is public even when its source repository is private.
- **GitHub Enterprise Cloud private Pages** can restrict a site to people with repository read access when that feature is configured and verified.
- **Local-only development** publishes nothing remotely and is the normal development mode.

Do not describe the current site as private unless its Pages access control has been explicitly configured and verified. Private access control does not replace keyboard, screen-reader, responsive, contrast, or semantic accessibility requirements. Requiring repository-read authentication may also exclude leadership reviewers who do not use GitHub, so an approved non-GitHub review path may still be necessary.

## Test before temporary publication

Run the repository validation sequence documented in `README.md`, review the rendered site locally, and record the authorized remote-test purpose and owner. Pull requests and pushes to `main` build and validate but cannot deploy.

## Publish temporarily

1. In GitHub Actions, open the **Publish guide** workflow.
2. Choose **Run workflow** and select the `main` branch.
3. Enter the exact confirmation value `PUBLISH`.
4. Run the workflow and confirm that its build and deploy jobs succeed.
5. Verify only the authorized rendering, interaction, browser, or device behavior.
6. Record findings in the applicable Issue or review record without adding sensitive information.

A dispatch from another branch or with any other confirmation value cannot run the deployment job.

## Unpublish immediately after testing

1. When testing ends, open the repository **Settings**.
2. Open **Pages**.
3. Select **Unpublish site** and confirm the action.
4. Open the former Pages URL in a signed-out or private browser session.
5. Confirm that the site is unavailable. Allow for documented GitHub or browser caching, refresh after the expected propagation interval, and do not declare the site offline until the public URL no longer serves it.
6. Record that unpublishing and offline verification were completed.

Unpublishing is a manual administrator or maintainer action. Do not store a personal access token solely to automate it, and do not add a Pages-deletion API call to this repository.

## Republish for a future test

Obtain fresh authorization, rerun current validation, then repeat the manual `main` plus `PUBLISH` workflow. Every temporary publication ends with the same manual unpublishing and offline verification procedure.

## Private canonical data and public-safe exports

Canonical internal or restricted project data belongs in a separate private organization-controlled repository or another approved secure organizational data store. This website repository may contain only schemas, synthetic fixtures, reviewed public-safe exports, publication and validation scripts, and non-sensitive provenance.

Browser-delivered JavaScript may consume only public-safe exports. Credentials, tokens, deploy keys, private URLs, and canonical private records must never enter JavaScript, rendered HTML, static assets, workflow artifacts intended for Pages, or the Pages deployment. A difficult-to-guess URL is not access control.

A future private-to-public exporter is a separate bounded Issue. It must use an explicit publication-field allowlist, geometry generalization, deterministic validation, publication-status checks, local-link and privacy checks, and a reviewable generated public dataset. This repository does not implement private-data ingestion or that exporter.
