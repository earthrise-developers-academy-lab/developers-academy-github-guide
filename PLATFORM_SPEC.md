# Developers Academy Platform Specification

**Version:** v0.1
**Status:** Pilot platform contract

This document is the canonical product and operating specification for the Developers Academy platform. It defines the approved v0.1 architecture, responsibilities, workflows, status vocabulary, and exclusions.

This is a pilot specification. It may change only through an approved GitHub Issue followed by a reviewed repository change. Implementations must not silently bypass this contract or invent product behavior where the contract is incomplete. The active GitHub Issue defines the authorized task scope; `AGENTS.md` defines how coding agents execute that task.

In this document, **must** identifies a requirement, **should** identifies the expected default, and **may** identifies an allowed option.

## 1. Purpose

The Developers Academy platform supports repeated cycles of:

- new participants joining with different levels of Git and GitHub experience;
- new project teams organizing and performing useful work;
- existing projects continuing across cohorts and iterations;
- program leadership reviewing deliverables without needing GitHub expertise;
- accepted artifacts being preserved in durable, organization-controlled locations; and
- selected accepted knowledge becoming part of the long-term Developedia knowledge layer.

The platform combines GitHub, Google Workspace, Quarto, and durable repositories or approved archives. It is a workflow and knowledge system built from existing tools, not a custom application.

The platform must preserve these distinctions:

- GitHub Issues are authoritative for active work, operational status, blockers, decisions, acceptance criteria, and recorded acceptance.
- GitHub Projects provide cross-project views derived from Issues and must not become a conflicting second source of status.
- Google Workspace supports drafting and review but is not authoritative for completion.
- Pull requests are the review gate for changes entering a repository.
- Accepted artifacts must be preserved in an organization-controlled repository or approved archive.
- Only selected accepted knowledge is curated into Developedia.
- Quarto publication does not itself indicate leadership acceptance.
- Not every accepted artifact must be published in Developedia.
- GitHub Copilot and coding agents are assistive, not authoritative.
- GitHub Desktop is the default participant Git interface, not a universal technical requirement.

## 2. Problem statement

Developers Academy participants arrive with uneven experience using Git, GitHub, branches, commits, Issues, and pull requests. The platform must let participants make useful, visible progress before they can independently complete a pull-request workflow.

Repository stewards need a consistent way to support participants, review repository changes, translate external feedback into actionable work, and prepare projects for handoff. Program leadership needs to understand projects, inspect deliverables, and request changes without learning GitHub's implementation details.

Projects may continue through several cohorts. Without a durable operational record, later participants can lose the context behind decisions, repeat completed work, overlook blockers, or rely on inaccessible working documents. Working documents, accepted artifacts, operational status, and long-term knowledge therefore need explicit relationships:

- working documents may remain in Google Docs, Sheets, or Slides while drafting and review continue;
- GitHub Issues record what is happening, why it is happening, and whether it has been accepted;
- organization-controlled repositories or approved archives preserve accepted artifacts; and
- Developedia selectively summarizes and links accepted knowledge that is useful beyond the immediate project.

## 3. User groups

### Participants

Participants perform project work while progressively learning Git and GitHub. They need:

- task-oriented onboarding;
- clearly scoped Issues with acceptance criteria;
- plain distinctions among Issues, Projects, branches, commits, and pull requests;
- GitHub Desktop as the default Git interface;
- visible completion states;
- working-document links and project context;
- clear blocker-reporting instructions; and
- clear points at which to ask a repository steward for help.

Participants are responsible for keeping their assigned Issue current with progress, blockers, decisions, evidence, and next actions.

### Repository stewards

Repository stewards support participant work and protect repository quality. They are responsible for:

- helping scope work into actionable Issues;
- assisting with branches, commits, pull requests, conflicts, and handoff;
- reviewing repository changes;
- checking that Projects reflect authoritative Issue state;
- translating actionable leadership feedback into GitHub;
- verifying artifact preservation;
- maintaining durable project context; and
- escalating conflicts with this platform contract.

Stewards may use GitHub Desktop, the Git command line, or another suitable Git client.

### Program leadership

Program leadership reviews project direction and deliverables, supplies comments or decisions, and requests changes. Leadership must be able to:

- understand a project without GitHub expertise;
- see plain-language phase and deliverable status;
- identify the artifact under review;
- understand acceptance criteria;
- know what decision is requested;
- inspect prior review history and deadlines; and
- provide feedback through a non-GitHub path or an explicit placeholder for that path.

Leadership comments in Google Workspace are review input. They do not become operational status or recorded acceptance until a participant or steward translates the decision into the authoritative GitHub Issue.

### Future cohorts

Future cohorts inherit project history, accepted artifacts, open work, and maintenance obligations. They need:

- a stable project identity independent of cohort year;
- current state and next actions;
- prior decisions and rationale;
- unresolved Issues and blockers;
- working-document and artifact locations;
- acceptance history;
- ownership and maintenance expectations; and
- recommendations for continuation.

Future cohorts are responsible for reading the durable record before changing prior work and for extending the existing project record instead of recreating it.

## 4. Core principles

### Issue-first work

Active work must begin with, or be connected to, an approved GitHub Issue. The Issue defines scope, acceptance criteria, ownership, operational status, blockers, decisions, and recorded acceptance.

### Accessible leadership review

Leadership review must present project context, artifacts, acceptance criteria, and requested decisions in plain language. Leadership must not be required to understand branches, commits, pull requests, or repository structure.

### One operational source of truth

GitHub Issues are the operational source of truth. GitHub Projects may summarize and organize Issues, but a Project field must not silently override or contradict its Issue.

### Working artifacts may live outside GitHub

Drafts may live in Google Docs, Sheets, Slides, or other approved working locations when those tools best support collaboration. The authoritative Issue must link the working artifact and record its operational state.

### Accepted artifacts must be preserved

An artifact is not operationally `accepted` until its accepted version is preserved in an organization-controlled repository or approved archive and its location is recorded in the Issue.

### Knowledge must survive cohorts

Decisions, rationale, validation, limitations, ownership, and next actions must be recorded durably. Critical context must not exist only in comments, private conversations, or external working documents.

### Progressive Git onboarding

Participants should begin with Issue updates and small, supported changes before being expected to complete pull requests independently. GitHub Desktop is the default participant interface. Stewards, Codex, and advanced contributors may use other Git clients.

### Human verification of AI-assisted work

GitHub Copilot and coding agents may help interpret errors, explore solutions, draft changes, or suggest tests. A human must verify their output against the Issue, repository behavior, validation results, security boundaries, and this specification.

### Minimal infrastructure first

The pilot must validate the human workflow with GitHub, Google Workspace, Markdown, Quarto, repositories, and approved archives before adding integration or application infrastructure.

### Portable content and metadata

Durable content and metadata should use reviewable, text-based, tool-portable formats where practical. Quarto and Markdown are the default publishing formats. Metadata must not depend on a proprietary database or custom backend in v0.1.

## 5. Component responsibilities

### GitHub Issues

GitHub Issues are authoritative for:

- active tasks, bugs, decisions, and deliverables;
- authorized scope;
- assignees and supporting stewards;
- acceptance criteria;
- operational status and progress;
- blockers and next actions;
- links to working documents and artifact candidates;
- review outcomes;
- acceptance evidence and recorded acceptance; and
- unresolved follow-up work.

An Issue must contain enough durable context for another person to understand the work without relying exclusively on a Project board or private conversation.

Issues do not, by themselves, preserve an artifact's contents. They must link to the accepted version in an organization-controlled repository or approved archive.

### GitHub Projects

GitHub Projects provide cross-project and cross-deliverable views derived from Issues. They support prioritization, filtering, coordination, and status visibility.

Projects are not a second authoritative record. When a Project field and its Issue conflict, the Issue governs and the Project view must be reconciled. Project-only notes must not contain essential decisions or acceptance evidence.

### Git repositories

Organization-controlled Git repositories are the durable home for accepted code, documentation, configuration, metadata, and Git-suitable artifacts. They provide version history, review history, ownership context, and a stable location for continued development.

Repository content does not independently prove operational or leadership acceptance. The authoritative Issue must record acceptance and link the accepted version.

Repository creation is a manual, authorized action in v0.1. Repository provisioning automation is excluded.

### Pull requests

Pull requests are the review gate for changes entering a repository. They provide a reviewable diff, discussion, validation evidence, and a merge decision.

A pull request may implement all or part of an Issue, but an open or merged pull request does not by itself establish leadership acceptance or Issue acceptance. Closing keywords should be used only when the Issue is fully resolved.

### GitHub Desktop

GitHub Desktop is the default participant Git interface because it exposes cloning, branches, commits, synchronization, and pull-request entry points without requiring command-line fluency.

It is not a universal technical requirement. Stewards, Codex, and advanced contributors may use other Git clients while following the same Issue scope, branch, review, validation, and preservation rules.

### Other Git clients

The Git command line and other Git clients are permitted for stewards, Codex, and advanced contributors. Their use must not create a separate workflow or bypass participant support, pull-request review, repository protections, or Issue authority.

### GitHub Copilot

GitHub Copilot may assist with issue-based troubleshooting, explanations, drafts, and code suggestions. The Issue should provide the problem statement, reproduction details, constraints, and relevant evidence used for troubleshooting.

Copilot output is not authoritative. Suggested changes must be reviewed, tested, checked for security and privacy problems, and recorded in the Issue when they affect the resolution or rationale.

### Google Workspace

Google Docs, Sheets, and Slides support collaborative drafting, comments, suggestions, and leadership review. They may hold active working artifacts and review history.

Google Workspace is not authoritative for completion, operational status, or recorded acceptance. A participant or steward must manually translate actionable feedback, decisions, blockers, and requested changes into the applicable GitHub Issue during v0.1.

Restricted Google Workspace links must not be exposed in public synthetic examples or published content.

### Quarto

Quarto is the static rendering and publication layer for participant onboarding, leadership-review context, and Developedia content. It may render repository-controlled Markdown and structured metadata, provide navigation and search, and link to authoritative Issues and artifacts.

Quarto is not a task database, feedback store, authentication system, or evidence of acceptance. Publication does not create GitHub work, persist leadership edits, harvest content across repositories, or prove leadership approval.

### Developedia

Developedia is the curated long-term knowledge layer published through Quarto. It preserves selected, reusable knowledge from accepted work and helps future cohorts understand a project's purpose, history, methods, decisions, limitations, ownership, and continuation needs.

Developedia does not duplicate every repository file and is not the authoritative operational status system. A project may be registered before its deliverables are accepted, but registration does not imply acceptance. Not every accepted artifact must be published in Developedia.

### Approved archives

An approved archive is an organization-controlled durable location for accepted artifacts that are unsuitable for Git because of format, size, retention requirements, or another approved constraint.

An approved archive must have clear organizational ownership, stable access expectations, and a link or identifier recorded in the authoritative Issue. An archive preserves artifacts but does not replace Issues for operational status or recorded acceptance.

## 6. Project lifecycle

A v0.1 project follows this lifecycle:

1. **Project proposal**
   Record the problem, intended users, expected value, initial scope, sponsor or partner context, known constraints, and proposed ownership.

2. **Stable project identifier**
   Assign an identifier that remains stable across cohorts, teams, and iterations.

3. **Repository creation**
   An authorized person manually creates or designates the organization-controlled repository. No provisioning automation is used in v0.1.

4. **Developedia registration**
   Register the stable project identity, purpose, ownership, and principal links. Registration provides discoverability but does not imply deliverable or leadership acceptance.

5. **Deliverable creation**
   Create Issues for bounded deliverables with owners, acceptance criteria, dependencies, working-document locations, and initial status.

6. **Participant and steward assignment**
   Identify the participant owner and the steward responsible for workflow support and repository review.

7. **Active work**
   Participants work from Issues, update progress, link working artifacts, record decisions, and report blockers.

8. **Internal review**
   Participants and stewards check correctness, completeness, validation, security, privacy, and readiness for any required leadership review.

9. **Leadership review where required**
   Leadership receives a plain-language review page, the artifact, acceptance criteria, requested decision, history, and feedback path.

10. **Feedback translation**
    A participant or steward manually translates actionable leadership feedback into the authoritative Issue and records resulting status changes.

11. **Repository or archive preservation**
    Preserve the accepted candidate in an organization-controlled repository through a reviewed pull request, or place it in an approved archive and record the stable location.

12. **Developedia update**
    Curate selected accepted knowledge when it has continuing value. This step is optional for any individual accepted artifact.

13. **Continuation, completion, maintenance, or archival**
    Record the project's disposition, ownership, unresolved work, maintenance expectations, and recommendations for a future cohort.

Projects must not be identified only by cohort year. A stable project may contain multiple cohort or iteration records so later work extends, rather than fragments, project history.

## 7. Deliverable lifecycle

The v0.1 deliverable-status vocabulary is:

- `not-started`
- `ready`
- `in-progress`
- `blocked`
- `internal-review`
- `leadership-review`
- `changes-requested`
- `ready-for-repository`
- `pull-request-open`
- `accepted`
- `archived`

### Status definitions

| Status | Definition |
|---|---|
| `not-started` | The deliverable is known, but work has not begun or its prerequisites are not yet sufficient. |
| `ready` | Scope, acceptance criteria, ownership, and prerequisites are sufficient for work to begin. |
| `in-progress` | Active work is underway and the Issue records current progress and next action. |
| `blocked` | Work cannot proceed. The Issue identifies the blocker, its impact, the assistance or decision needed, and the next owner. |
| `internal-review` | A participant, peer, or steward is reviewing the deliverable for correctness, completeness, validation, security, privacy, and readiness for the next stage. |
| `leadership-review` | Leadership review is required and the artifact, criteria, requested decision, history, deadline, and non-GitHub feedback path are available. |
| `changes-requested` | Review identified required revisions. The Issue records the requested changes, source of the feedback, owner, and next action. |
| `ready-for-repository` | Required review is complete and the accepted candidate is ready for durable repository or archive preservation. |
| `pull-request-open` | A pull request preserving or changing the artifact is open and awaiting required review, validation, or merge. |
| `accepted` | Acceptance criteria and required decisions are satisfied and recorded in the Issue, and the accepted artifact is preserved in an organization-controlled repository or approved archive. |
| `archived` | The deliverable is no longer active and is retained with its disposition and durable history. Archival does not imply acceptance unless acceptance was separately recorded. |

Not every deliverable must traverse every status. For example, an internal documentation change may not require leadership review, and an archive-only artifact may not require a repository pull request.

`blocked` can interrupt any active stage. When the blocker is removed, the Issue returns to the appropriate lifecycle status with the resolution recorded.

`changes-requested` may return work to an earlier stage, including `in-progress`, `internal-review`, or `leadership-review`.

GitHub Issues remain authoritative for deliverable status. GitHub Projects must reflect the Issue state and must not create an independent status decision.

This vocabulary may be revised after the pilot. Implementations must not invent additional statuses without an approved Issue.

### Conditions for `accepted`

A deliverable may be marked `accepted` only when:

1. its acceptance criteria are satisfied, or an authorized exception is explicitly recorded in the Issue;
2. required validation evidence is recorded or linked;
3. any required leadership decision has been manually recorded in the Issue;
4. required review changes have been resolved or explicitly dispositioned;
5. the accepted version is preserved in an organization-controlled repository or approved archive;
6. repository changes, when applicable, entered through a reviewed pull request;
7. the Issue identifies the durable artifact location and accepted version; and
8. the person authorized to record acceptance has done so in the Issue.

Implementation completion, a merged pull request, leadership approval, artifact preservation, and Quarto publication are distinct events. None should be reported as another without evidence.

## 8. Core workflows

### Starting and scoping work

1. Begin from an approved Issue or create one through the authorized human process.
2. Record the intended outcome, boundaries, owner, steward, acceptance criteria, dependencies, and relevant links.
3. Check the Issue against this platform contract and its v0.1 exclusions.
4. Resolve material ambiguity before implementation.
5. Set `ready` only when the work is actionable.

### Claiming and updating an Issue

1. Assign or record the participant owner and supporting steward.
2. Confirm the next action before changing status to `in-progress`.
3. Add concise progress updates with evidence, decisions, links, and remaining work.
4. Keep the Issue authoritative if the Project view becomes stale.
5. Reconcile the Project view so it reflects the Issue.

### Participant work using GitHub Desktop by default

1. Use GitHub Desktop to obtain the repository and create or select an Issue-specific branch.
2. Make the smallest changes that satisfy the Issue.
3. Review changed files and create focused commits.
4. Publish the branch and open a pull request when repository preservation is required.
5. Ask a steward for help with repository access, branch confusion, conflicts, validation failures, unclear review feedback, or uncertainty about the correct artifact location.

Stewards, Codex, and advanced contributors may use other Git clients without changing the workflow's authority or review requirements.

### Reporting blockers

1. Change the authoritative Issue to `blocked`.
2. Describe the blocker, evidence, impact, attempted actions, and assistance or decision needed.
3. Identify the next owner and follow-up point.
4. Reflect the blocked state in the Project view.
5. Record the resolution before returning to the appropriate active status.

### Copilot-assisted troubleshooting from an Issue

1. Start with the Issue's problem statement, reproduction steps, constraints, and relevant non-sensitive evidence.
2. Use Copilot to explain errors, propose hypotheses, or suggest bounded changes and validation.
3. Do not supply credentials, restricted data, or unnecessary private content.
4. Review and validate every suggestion.
5. Record the verified resolution and relevant rationale in the Issue.

### Internal review

1. Move the deliverable to `internal-review`.
2. Compare it with acceptance criteria and applicable validation requirements.
3. Check privacy, security, accessibility, correctness, maintainability, and handoff context.
4. Record requested revisions as `changes-requested`, or advance to the next required stage.

### Leadership review

1. Prepare the leadership-facing review information defined in Section 9.
2. Move the Issue to `leadership-review`.
3. Provide the artifact and a non-GitHub feedback path or explicit placeholder.
4. Keep the operational Issue current while review occurs.
5. Do not interpret publication or a Google Workspace comment alone as recorded acceptance.

### Manual translation of actionable leadership feedback into GitHub

1. A participant or steward reviews leadership comments or decisions.
2. Summarize actionable feedback in the authoritative Issue.
3. Link the review source when access and privacy permit.
4. Record the requested changes, decision, owner, and next action.
5. Move the Issue to `changes-requested` or the appropriate next status.
6. Do not create Issues automatically from leadership feedback in v0.1.

### Repository preservation through a reviewed pull request

1. Confirm required review is complete.
2. Move the Issue to `ready-for-repository`.
3. Prepare a focused branch and pull request linked to the Issue.
4. Run applicable validation and record the results.
5. Obtain required repository review.
6. Merge through the repository's approved process.
7. Record the preserved version or location in the Issue.

Artifacts stored in an approved archive follow the organization's manual archive process and must have their stable location recorded in the Issue.

### Acceptance and archival

1. Verify every `accepted` condition in Section 7.
2. Record acceptance and artifact location in the Issue.
3. Reconcile the Project view.
4. Record unresolved follow-up work as separate approved Issues.
5. Use `archived` when a deliverable is no longer active, preserving its disposition and history.

### Selective Developedia publication

1. Decide whether accepted knowledge has durable onboarding, reference, methodological, or continuation value.
2. Create an approved Issue for the curation work.
3. Summarize and link the accepted source rather than copying every file.
4. Review the Quarto change through a pull request.
5. Preserve the distinction between publication and acceptance.

An accepted artifact may remain unpublished. A published page may describe work that is not leadership-accepted if its status is clear.

### Cohort handoff

1. Review all active and unresolved Issues.
2. Confirm owners, stewards, blockers, next actions, decisions, working-document links, acceptance history, and artifact locations.
3. Preserve durable rationale in GitHub or repository content.
4. Record maintenance expectations and continuation recommendations.
5. Introduce the next cohort to the stable project record rather than creating a cohort-year replacement.

## 9. Leadership review

A leadership-facing review page must include:

- a plain-language project summary;
- the project phase and authoritative deliverable status;
- the deliverable title and owner;
- an artifact link or rendering;
- the acceptance criteria;
- the specific requested decision;
- prior review history;
- the review deadline; and
- a non-GitHub feedback mechanism or an explicit placeholder.

The page should minimize repository implementation detail and explain any unavoidable technical terms. It must identify whether leadership is being asked to approve, reject, prioritize, select an option, or request changes.

Quarto is static. It does not persist edits, store comments, authenticate reviewers, synchronize Google Workspace, or create GitHub work without a separate integration. A placeholder must not be presented as a functioning feedback form.

Automatic Google Workspace synchronization and automatic GitHub Issue creation from leadership feedback are excluded from v0.1. Feedback translation is manual. The Issue becomes authoritative only after the relevant decision or requested change is recorded there.

## 10. Artifact lifecycle

The artifact lifecycle contains distinct concepts:

1. **Draft**
   Work is being created and may change substantially. It may live in Google Workspace or a repository branch.

2. **Reviewed draft**
   Participants, peers, or stewards have reviewed the draft, but required revisions, leadership decisions, or preservation may remain.

3. **Leadership decision**
   Leadership approves, rejects, defers, prioritizes, or requests changes where leadership review is required. The decision must be manually translated into the Issue before it affects authoritative status.

4. **Accepted artifact**
   The artifact version satisfies the Issue's acceptance conditions. Operational `accepted` status also requires durable preservation and a recorded artifact location.

5. **Repository or archive preservation**
   The accepted version is stored in an organization-controlled repository through a reviewed pull request or in an approved archive.

6. **Developedia curation**
   Selected accepted knowledge is summarized, contextualized, and linked for long-term reuse.

Drafting does not imply completion. Leadership acceptance does not itself preserve the artifact. Repository preservation does not require Developedia publication. Developedia publication does not imply leadership acceptance. Accepted artifacts may remain unpublished in Developedia.

## 11. Developedia knowledge model

A durable project record in Developedia should contain, when applicable and safe to publish:

- stable project identity;
- purpose and intended users;
- approved, non-restricted partner context;
- cohort and iteration history;
- repository and application links;
- methods and data descriptions;
- decisions and rationale;
- validation performed and evidence;
- limitations and known risks;
- accepted deliverables and their durable locations;
- current ownership and stewardship;
- maintenance expectations; and
- continuation recommendations.

Developedia summarizes and links rather than duplicating every repository file. Operational detail remains in Issues, accepted source material remains in repositories or approved archives, and working drafts may remain in Google Workspace.

Developedia content must state the status and provenance of the knowledge it presents. Project registration, Quarto publication, leadership acceptance, Issue acceptance, and artifact preservation must not be conflated.

## 12. Cohort continuity and handoff

Before a project changes cohorts, pauses, or changes owners, its durable record must preserve:

- current state;
- owner and steward;
- blockers;
- next action;
- decisions;
- working-document links;
- acceptance history;
- artifact location;
- unresolved Issues;
- maintenance or continuation expectations.

The handoff must also identify the stable project identifier, current iteration, applicable repositories, relevant Developedia entry, and any access dependency requiring steward support.

Durable rationale must be preserved in GitHub Issues, pull-request discussion when appropriate, or repository content rather than only in external working documents. External documents may supply supporting detail, but a later cohort must be able to understand the operational decision even if an external link becomes unavailable.

## 13. MVP vertical slice

The v0.1 MVP must implement one entirely synthetic reference lifecycle. It must contain:

- participant onboarding that starts with finding and understanding an Issue;
- at least one synthetic project with a stable identifier and fictitious context;
- at least three deliverables in distinct lifecycle states;
- one leadership-review example;
- one changes-requested example;
- one accepted artifact example;
- one non-GitHub feedback placeholder;
- one steward feedback-translation example; and
- one cohort-handoff example.

A suitable reference set would include:

- an accepted synthetic project brief preserved in this organization-controlled repository;
- a synthetic findings presentation in `leadership-review`; and
- a synthetic methods note in `changes-requested`.

The example must show how a steward translates a fictitious leadership comment into an Issue update and how a later cohort finds current state, decisions, blockers, artifact locations, and next actions.

No real participant, partner, project, production, private, or restricted information may be used. Names, documents, comments, links, metadata, and datasets must be clearly synthetic.

## 14. Functional requirements

### Website navigation

The Quarto website must provide clear navigation among participant onboarding, project and deliverable guidance, leadership review, steward guidance, and Developedia content once those pages are implemented. Navigation must not reference nonexistent pages.

### Search

The website must provide search across published Quarto content. Search does not extend to private Google Workspace content, GitHub Issues, approved archives, or other repositories unless a future approved Issue changes the platform contract.

### Participant onboarding

The site must provide task-oriented onboarding for participants with limited Git experience. It must explain how to find work, read an Issue, understand status, update progress, report blockers, use working-document links, make a supported repository change, and ask a steward for help.

### Issues and deliverables guidance

The site must explain that Issues are authoritative and must describe the v0.1 status vocabulary, acceptance criteria, ownership, updates, blockers, evidence, decisions, and completion states.

### GitHub Desktop guidance

The site must provide GitHub Desktop guidance for the default participant workflow, including obtaining a repository, using an Issue-specific branch, reviewing changes, committing, publishing a branch, and beginning a pull request. It must not imply that GitHub Desktop is mandatory for every contributor.

### Copilot troubleshooting guidance

The site must explain how to begin troubleshooting from an Issue, provide safe context, evaluate Copilot suggestions, validate changes, avoid sensitive data, and record verified outcomes.

### Steward guidance

The site must provide steward guidance for Issue scoping, participant support, review, feedback translation, artifact preservation, status reconciliation, and handoff.

### Synthetic project catalog

The site must contain a catalog of synthetic projects or the synthetic MVP project. Each entry must show stable identity, purpose, phase, authoritative links, and continuation context without using restricted information.

### Project detail page

The synthetic project must have a detail page containing its purpose, intended users, current phase, cohort or iteration history, deliverables, authoritative Issues, repositories or approved archives, decisions, limitations, ownership, and next actions.

### Leadership review page

The MVP must include a leadership review page satisfying Section 9. It must identify its example data as synthetic and must not claim that a placeholder persists feedback.

### Local preview and validation

The repository must document a local workflow for checking and previewing the Quarto site. The baseline future validation includes `quarto check`, `quarto render`, and `git diff --check`, with any additional repository validators documented alongside them.

### Automated site validation

The implemented site must have automated validation in GitHub Actions for rendering and applicable deterministic checks. Automation must not publish restricted content or mutate Issues.

### GitHub Pages deployment

The implemented site must support deployment to the approved GitHub Pages location through a separately reviewed and authorized configuration. The initial `_quarto.yml` does not itself define deployment automation.

## 15. Nonfunctional requirements

### Accessibility

Published content must use semantic structure, descriptive link text, keyboard-accessible navigation, sufficient contrast, useful alternative text, and understandable language. Leadership and participant workflows must be tested for usability, not only technical rendering.

### Maintainability

Content, metadata, configuration, and validation should remain small, documented, and reviewable. Repeated structures should use clear conventions without introducing unnecessary application code.

### Reproducibility

An authorized contributor must be able to build and validate the site from repository content using documented tooling and commands. Generated output must not be the only copy of durable source content.

### Privacy

The MVP must use synthetic information. It must not publish production participant or partner data, restricted project information, or private Google Workspace links.

### Security

The platform must not require browser-delivered credentials or secrets. Repository protections, organization ownership, least-privilege access, human review, and explicit authorization boundaries must be preserved.

### Portability

Primary content and metadata should use Markdown, YAML, and other broadly supported formats. Quarto source content must remain useful as repository-controlled text even if the publication environment changes.

### Deterministic metadata validation

When structured metadata is introduced, its schema and validation rules must be deterministic. The same valid input must produce the same validation result locally and in automation, with actionable failures and no dependency on private external state.

## 16. Explicit v0.1 non-goals

- a database;
- a custom backend;
- authentication;
- a JavaScript frontend framework;
- automatic Google Workspace synchronization;
- automatic GitHub Issue creation from leadership feedback;
- cross-repository content harvesting;
- production participant or partner data;
- repository provisioning automation.

These exclusions may change only through an approved Issue that explicitly revises the platform contract. A deferred decision is not authorization to implement an excluded capability.

## 17. Success criteria

The pilot succeeds when the following scenarios produce observable results:

1. **Issue discovery**
   Given a published synthetic project entry, a participant can reach the authoritative Issue, identify its owner, status, acceptance criteria, and next action, and distinguish it from the Project view.

2. **Progress updates**
   A participant can add a useful Issue update containing completed work, evidence or a working-document link, remaining work, and next action. The Project view can then be reconciled to match the Issue.

3. **Blocker reporting**
   A participant can record a blocker with its impact, attempted actions, requested assistance, and next owner, and a steward can identify what is needed without a separate conversation.

4. **Working-document linking**
   A participant can link a synthetic working document from an Issue and correctly explain that the document supports drafting while the Issue remains authoritative for status and completion.

5. **Guided pull-request completion**
   A Git-inexperienced participant, with documented steward support, can use GitHub Desktop to work on an Issue-specific branch, review and commit a bounded change, publish the branch, and begin a pull request without being required to use the command line.

6. **Leadership review without GitHub**
   A reviewer without GitHub expertise can identify the project, deliverable, artifact, status, criteria, requested decision, review history, deadline, and non-GitHub feedback path from the synthetic leadership-review page.

7. **Feedback translation**
   A steward can translate synthetic leadership feedback into the authoritative Issue, preserving the decision, requested changes, owner, next action, and source context without automatic integration.

8. **Accepted artifact preservation**
   An `accepted` example links from its authoritative Issue to a specific accepted version in an organization-controlled repository or approved archive and shows required review and acceptance evidence.

9. **Future-cohort continuation**
   A person unfamiliar with the synthetic project can locate its current state, owners, blockers, decisions, working documents, acceptance history, artifacts, unresolved Issues, and next action from the durable record.

Pilot usability review must include both a Git-confident user and a Git-inexperienced user. Observed friction must be recorded in Issues before expanding automation.

## 18. Deferred decisions

The following decisions are intentionally deferred:

- whether the guide and Developedia later split;
- leadership-feedback integration choice;
- centralized versus repository-sourced metadata;
- issue-seeding automation;
- artifact archival rules;
- ownership review;
- future developer-portal adoption.

Deferral does not authorize implementation. Each decision requires an approved Issue, evidence from the pilot, review against privacy and security constraints, and an explicit update to this contract when necessary.

## 19. Development sequence

1. Approve the platform contract.
2. Create a bounded Quarto bootstrap Issue.
3. Plan before editing.
4. Implement one vertical slice.
5. Validate locally and through GitHub Actions.
6. Review participant and leadership usability.
7. Test with both a Git-confident and Git-inexperienced user.
8. Revise based on observed friction.
9. Add automation only after the workflow is validated.
