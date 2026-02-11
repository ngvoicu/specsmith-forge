# SPEC.md Format Reference

This is the complete format specification for spec documents. Use this as
the template when creating new specs.

## Full Template

```markdown
---
id: <spec-id>
title: <Human Readable Title>
status: active | paused | completed | archived
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
priority: high | medium | low
tags: [<tag1>, <tag2>]
---

# <Title>

## Overview

<2-4 sentences describing what this spec accomplishes and why. Include
enough context that someone resuming cold can understand the goal without
reading the full conversation history.>

## Requirements

- <When X happens, the system shall Y>
- <The Z component shall do W>
- [NEEDS CLARIFICATION] <Ambiguous requirement that needs discussion>

Requirements are lightweight acceptance criteria — what "done" looks like.
Not every spec needs them (skip for small bug fixes), but for features
they prevent scope creep and make verification clear.

## Phase 1: <Phase Name> [in-progress]

- [x] <Completed task description>
- [ ] <Current task description> ← current
- [ ] <Future task description>
- [ ] <Future task description>

## Phase 2: <Phase Name> [pending]

- [ ] <Task description>
- [ ] <Task description>
- [ ] <Task description>

## Phase 3: <Phase Name> [pending]

- [ ] <Task description>
- [ ] <Task description>

---

## Resume Context

> <Detailed description of where you left off. Include:>
> - What was just completed
> - What's currently in progress
> - Specific file paths and function/component names
> - The exact next step to take
> - Any blockers or open questions
>
> Write this as if briefing a colleague picking up your work tomorrow.

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| <YYYY-MM-DD> | <What was decided> | <Why this choice was made> |
```

## Field Definitions

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | URL-safe identifier, lowercase hyphenated (e.g., `user-auth-system`) |
| `title` | Yes | Human-readable name |
| `status` | Yes | One of: `active`, `paused`, `completed`, `archived` |
| `created` | Yes | ISO date when spec was created |
| `updated` | Yes | ISO date of last modification |
| `priority` | No | `high`, `medium`, or `low` (default: medium) |
| `tags` | No | YAML array of categorization tags |

### Phase Status Markers

Phase headings include a status marker in square brackets:

| Marker | Meaning |
|--------|---------|
| `[pending]` | Not started yet |
| `[in-progress]` | Currently being worked on |
| `[completed]` | All tasks done |
| `[blocked]` | Waiting on something external |

Only **one phase** should be `[in-progress]` at a time (though this isn't
strictly enforced — sometimes parallel phases make sense).

### Task Format

Tasks use standard markdown checkboxes:

```markdown
- [ ] Unchecked task (not done)
- [x] Checked task (done)
- [ ] Current task ← current
```

The `← current` marker indicates which task the AI should work on next.
Only one task should have this marker at a time.

**Task granularity**: Each task should represent roughly one focused work
session (30 min to 2 hours of work). If a task feels like it would take a
full day, break it into subtasks.

### Uncertainty Markers

Use `[NEEDS CLARIFICATION]` for any requirement or task where ambiguity
remains after interviews:

```markdown
- [ ] [NEEDS CLARIFICATION] Handle rate limiting for uploads
```

These markers signal that the task needs more discussion before
implementation. Don't start a task with this marker — resolve it first
(run another interview round or ask the user directly).

### Resume Context

The Resume Context section is freeform markdown inside a blockquote. It
should answer these questions:

1. **What just happened?** — What was completed in the last session
2. **What's the current state?** — Which files changed, what works, what doesn't
3. **What's next?** — The specific next action to take
4. **Where exactly?** — File paths, function names, line ranges
5. **Any gotchas?** — Blockers, open questions, things that didn't work

**Good example:**
```markdown
> Finished implementing the JWT token generation in `src/auth/tokens.ts`.
> The `generateAccessToken()` and `generateRefreshToken()` functions are
> working and tested. Moved on to the refresh endpoint but hit an issue:
> the `POST /auth/refresh` handler in `src/routes/auth.ts` needs to
> validate the refresh token AND rotate it (issue new refresh token on
> each use). The validation part works but rotation isn't implemented.
>
> Next step: Add `rotateRefreshToken()` to `src/auth/tokens.ts` that
> invalidates the old token and issues a new one. Then wire it into the
> route handler. See the TODO comment at line 47 of `src/routes/auth.ts`.
```

**Bad example:**
```markdown
> Was working on authentication. Made some progress on tokens.
```

### Decision Log

Track non-obvious technical decisions so you (or another AI session) can
understand why things are the way they are:

```markdown
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-10 | JWT over sessions | Stateless auth scales better for our microservice architecture |
| 2026-02-10 | Refresh token rotation | Security best practice — limits window if a token is stolen |
| 2026-02-11 | argon2 over bcrypt | Better resistance to GPU attacks, recommended by OWASP |
```

Good decisions to log:
- Library/framework choices
- Architecture patterns
- API design decisions
- Trade-offs made (performance vs readability, etc.)
- Things you tried and rejected (and why)

## Minimal Spec Example

For small tasks, a spec can be much simpler:

```markdown
---
id: fix-upload-bug
title: Fix File Upload Bug
status: active
created: 2026-02-10
updated: 2026-02-10
priority: high
---

# Fix File Upload Bug

## Overview

Files over 10MB fail silently on upload. The multipart parser truncates
the stream. Need to fix the size limit and add proper error handling.

## Phase 1: Fix and Test [in-progress]

- [ ] Reproduce the bug with a 15MB file ← current
- [ ] Fix multipart parser size limit in `src/upload/parser.ts`
- [ ] Add proper error response for oversized files
- [ ] Write test for boundary conditions (exactly 10MB, 10.1MB, 100MB)
- [ ] Test in staging

---

## Resume Context

> Haven't started yet. Bug report is in issue #342. The upload handler
> is in `src/upload/parser.ts` and uses `busboy` for multipart parsing.
> Suspect the `limits.fileSize` option is set too low.
```

## Complex Spec Example

For larger features with multiple phases:

```markdown
---
id: real-time-collab
title: Real-Time Collaboration
status: active
created: 2026-02-01
updated: 2026-02-10
priority: high
tags: [feature, websocket, collaboration]
---

# Real-Time Collaboration

## Overview

Add real-time collaborative editing to the document editor. Multiple
users should see each other's cursors and edits in real time, with
conflict resolution handled via CRDTs.

## Phase 1: WebSocket Infrastructure [completed]

- [x] Set up WebSocket server with Socket.io
- [x] Implement room-based connections (one room per document)
- [x] Add authentication middleware for WS connections
- [x] Handle reconnection and connection state

## Phase 2: CRDT Integration [in-progress]

- [x] Integrate Yjs as the CRDT library
- [x] Create document sync provider
- [ ] Implement awareness protocol (cursors, selections) ← current
- [ ] Add undo/redo manager that works with CRDTs

## Phase 3: UI Layer [pending]

- [ ] Render remote cursors with user colors/names
- [ ] Show selection highlights for other users
- [ ] Add presence indicator (who's viewing)
- [ ] Handle offline state gracefully in UI

## Phase 4: Edge Cases and Polish [pending]

- [ ] Test with 10+ simultaneous users
- [ ] Handle large document performance
- [ ] Add rate limiting for rapid edits
- [ ] Write integration tests for conflict scenarios

---

## Resume Context

> Phase 2 is in progress. Yjs is integrated and basic document sync
> works between two browser tabs. Currently implementing the awareness
> protocol which handles cursor positions and user presence.
>
> The awareness provider is partially built in
> `src/collab/awareness-provider.ts`. The local cursor state broadcasts
> correctly but remote cursor state isn't being applied to the editor
> yet. Need to hook into CodeMirror's decoration system to render
> remote cursors.
>
> Key file: `src/collab/awareness-provider.ts` (the provider)
> Key file: `src/editor/remote-cursors.ts` (needs to be created)
> Reference: Yjs awareness docs at https://docs.yjs.dev/api/about-awareness

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-01 | Socket.io over raw WS | Built-in reconnection, rooms, and fallback to polling |
| 2026-02-03 | Yjs over Automerge | Better editor integration (ProseMirror/CodeMirror bindings) |
| 2026-02-05 | Room-per-document | Simpler than multiplexing, isolates failure domains |
| 2026-02-08 | Awareness as separate protocol | Cursor positions need higher update frequency than doc edits |
```
