# Progress and Google Docs

| System | Use |
|---|---|
| GitHub Issue | Ownership, status, blockers, acceptance criteria, completion evidence |
| GitHub Project | Cross-project progress overview |
| Google Docs | Collaborative drafting, comments, suggestions, partner review |
| Git repository | Accepted, durable project artifacts |
| Pull request | Review of proposed repository changes |

GitHub remains the source of truth for whether a deliverable is complete.

## Link a working Google Doc

```markdown
## Working document

[Open the user-guide draft](GOOGLE_DOC_URL)
```

At the top of the Google Doc, add the GitHub issue URL.

## Post a progress update

```markdown
### Progress update

**Completed**
- Reviewed the existing requirements.
- Drafted the installation section.

**Evidence**
- Working document: <Google Doc URL>

**Current blocker**
- None.

**Next action**
- Draft the primary user workflow.

**Ready for review when**
- The installation, workflow, and known-limitations sections are complete.
```

When the document is accepted, export or convert the approved version, add it to the documented repository destination, and submit it through a linked pull request.
