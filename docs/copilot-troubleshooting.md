# Copilot troubleshooting

Copilot can assist with investigation, but its suggestions are not evidence.

## Diagnose before editing

```text
Use issue #12 as the authoritative problem statement.

Do not change code yet.

Inspect the repository and provide:

1. The most likely relevant files.
2. Three ranked hypotheses.
3. The smallest test for each hypothesis.
4. Missing information in the issue.
5. Assumptions that have not been verified.

Do not claim a root cause without evidence.
```

For each hypothesis, record the proposed cause, test performed, observed result, and whether it was supported or rejected.

After evidence supports a cause, request the smallest change that satisfies the issue, avoids unrelated refactoring, adds or updates tests, and reports remaining uncertainty.

Human review and validation remain required before merging.
