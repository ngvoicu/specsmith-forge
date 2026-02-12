---
description: List all specs with status, progress, and priority
disable-model-invocation: true
---

# List Specs

Show all specs grouped by status.

1. Read `.specs/registry.md`
2. For each spec, also read the SPEC.md to get accurate task counts
4. Present grouped by status:

```
Active:
  → auth-system: User Auth System (5/12 tasks, Phase 2) [high]

Paused:
  ⏸ api-refactor: API Refactoring (2/8 tasks, Phase 1) [medium]
  ⏸ dark-mode: Dark Mode Support (0/6 tasks, not started) [low]

Completed:
  ✓ ci-pipeline: CI Pipeline Setup (8/8 tasks) [high]
```

If there are no specs, suggest running `/spec-smith:forge` to create one.
