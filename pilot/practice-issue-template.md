# Synthetic onboarding practice

> **Synthetic practice only.** Use the assigned fictional alias or public GitHub username. Do not add private participant, employer, partner, project, contact, health, accessibility, demographic, credential, or restricted-link information.

## Objective

Complete one small Issue-to-pull-request practice contribution through GitHub Desktop and request repository-steward review.

## Assignment

- **Assigned alias:** `<assigned-alias>`
- **Supporting steward:** `<steward>`
- **Destination:** `practice/submissions/<assigned-alias>.qmd`

This body must be copied into a manually created practice Issue. It does not create an Issue or provision repository access.

## Steps

1. Read this objective and the acceptance criteria.
2. Assign yourself when permitted, or claim the Issue with a comment.
3. Post a starting-work update.
4. Create an Issue-linked branch from `main` and open it in GitHub Desktop.
5. Copy `pilot/submission-template.qmd` to the exact destination above.
6. Replace only approved synthetic fields.
7. Review the complete diff.
8. Run the required validation.
9. Commit and push the branch.
10. Open a pull request against `main` containing `Fixes #<issue-number>`.
11. Request review from the supporting steward.
12. Respond to one simulated review comment.
13. After authorized merge and publication, locate the rendered submission.

## Allowed content

- Assigned fictional alias or public GitHub username
- Fictional project role
- One sentence describing the completed exercise
- Onboarding-step checklist
- Optional one-sentence reflection about workflow friction

## Prohibited content

Do not add private or legal names unless separately approved, email addresses, telephone numbers, employer information, demographic, medical, or accessibility information, real project or partner information, private links, credentials, restricted screenshots, or sensitive narratives.

## Acceptance criteria

- [ ] The file is at `practice/submissions/<assigned-alias>.qmd`.
- [ ] Its front matter has a nonempty title and `synthetic: true`.
- [ ] It contains only allowed fields and synthetic content.
- [ ] The participant reviewed the complete diff and posted an accurate progress update.
- [ ] The branch contains only the bounded practice contribution.
- [ ] Required validation passes.
- [ ] The pull request targets `main` and contains `Fixes #<issue-number>` for this Issue.
- [ ] Steward review was requested and the simulated review comment received a response.

## Validation

Run, or work with the steward to run:

```text
quarto render
python scripts/validate_practice_submissions.py
git diff --check
```

Record only checks that actually ran.

## Request steward help when

Ask before continuing if access is missing; the Issue is unclear; sensitive content may be present; the wrong repository, base, or branch is selected; unexpected files appear; validation fails; a conflict occurs; or review feedback is unclear.
