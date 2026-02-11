## Spec Management (Spec Smith)

This project tracks work in `.specs/`. When starting a task:

1. Check `.specs/active` for the current spec ID
2. Read `.specs/specs/<id>/SPEC.md` to understand context and progress
3. Find the task marked `← current` — that's what to work on
4. Read the "Resume Context" section for detailed state from last session

While working:
- Check off completed tasks: `- [ ]` → `- [x]`
- Move `← current` to the next unchecked task
- When a phase completes, mark it `[completed]` and start the next

Before finishing:
- Update "Resume Context" with specific files, functions, and next steps
- Update the `updated` date in frontmatter
- Be specific: "implementing verifyToken() in src/auth/tokens.ts" not
  "working on auth"
