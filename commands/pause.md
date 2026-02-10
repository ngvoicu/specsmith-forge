| description | Pause the active spec — save detailed resume context for next session |
| disable-model-invocation | true |

# Pause Spec

Read the spec-smith skill and follow the "Pausing a Spec" workflow.

1. Read `.specs/active` to find the active spec
2. Load the SPEC.md
3. Capture everything about the current state:
   - Which task was in progress
   - What files were modified (specific paths, function names, line ranges)
   - Key decisions made this session
   - Blockers or open questions
   - The exact next step someone should take
4. Write all of this to the Resume Context section in SPEC.md
5. Update checkboxes to reflect actual progress
6. Move `← current` to the correct task
7. Add session decisions to Decision Log
8. Set status to `paused`, update the `updated` date
9. Update `.specs/registry.md`
10. Confirm to the user that context was saved

Be extremely specific in the Resume Context. Write it as if briefing a
colleague who has never seen this code and will pick up tomorrow.
