| description | Resume the active spec — read progress, load context, pick up where you left off |
| disable-model-invocation | true |

# Resume Spec

Read the spec-smith skill and follow the "Resuming a Spec" workflow.

1. Read `.specs/active` to find the active spec ID
2. If empty, read `.specs/registry.md` and show the user their specs so
   they can choose one
3. Load `.specs/specs/<id>/SPEC.md`
4. Parse progress — count completed vs total tasks per phase
5. Find the current phase and current task (`← current` marker)
6. Read the Resume Context section
7. Check if there are research notes in `.specs/research/<id>/` that
   provide additional context
8. Present a compact summary and begin working on the current task

If there are no specs at all, suggest running `/spec-smith:forge` to
create one.
