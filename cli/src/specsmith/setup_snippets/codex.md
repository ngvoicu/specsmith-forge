## Spec Management (Spec Smith)

This project uses structured specs for task tracking in `.specs/`.

### On session start
1. Check if `.specs/active` exists and contains a spec ID
2. If yes, read `.specs/specs/<id>/SPEC.md`
3. Find the current phase (`[in-progress]`) and current task (`← current`)
4. Read the "Resume Context" section for where you left off
5. Begin working on the current task

### While working
- Check off tasks as you complete them: `- [ ]` → `- [x]`
- Move the `← current` marker to the next task
- When a phase is done: change `[in-progress]` → `[completed]`, next phase
  `[pending]` → `[in-progress]`

### Before finishing
- Update the "Resume Context" section with:
  - What you just completed
  - What files you modified (specific paths, function names)
  - The exact next step someone should take
  - Any blockers or open questions
- Update the `updated` date in the YAML frontmatter
- Update `.specs/registry.md` if status changed

### Creating a new spec
When asked to plan or spec out work, create a SPEC.md in
`.specs/specs/<id>/SPEC.md` with this structure:

- YAML frontmatter: id, title, status, created, updated, priority, tags
- Overview section (2-4 sentences on what and why)
- Phases with `[pending]`/`[in-progress]`/`[completed]` markers
- Tasks as markdown checkboxes within each phase
- Resume Context section (blockquote)
- Decision Log table
