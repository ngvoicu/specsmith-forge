# Spec Smith

**Plan mode, but actually good.**

Spec Smith replaces ephemeral AI coding plans with persistent, resumable specs built through deep research and iterative interviews. Create a spec, work through it task by task, pause, switch to another spec, come back a week later and pick up exactly where you left off.

Works with Claude Code (as a plugin), Codex, Cursor, Windsurf, Cline, and any AI coding tool that can read files.

## The Problem

Every AI coding tool has some version of "plan mode" — think before you code. But these plans are ephemeral. They live in the conversation context. Close the terminal, start a new session, and the plan is gone. There's no way to:

- **Resume** a plan you were halfway through implementing
- **Switch** between multiple plans when juggling features
- **Track** which tasks are done and which are next
- **Persist** the research and decisions that informed the plan

Spec Smith fixes all of this.

## How It Works

### The Forge Workflow

Run `/spec-smith:forge "add user authentication with OAuth"` and Spec Smith takes over:

**1. Deep Research** — Exhaustive codebase scan (reads 10-20+ actual files, not just file names), web search for best practices, Context7 library docs, UI inspection if applicable. Everything saved to `.specs/research/<id>/research-01.md`.

**2. Interview** — Presents findings, states assumptions, asks targeted questions informed by the research. Not generic questions — specific ones like "I see you're using Express middleware pattern X in `src/middleware/`. Should the auth middleware follow the same pattern?" Saves answers to `interview-01.md`.

**3. Deeper Research** — Investigates the specific directions from the interview. Checks feasibility, finds edge cases.

**4. More Interviews** — As many rounds as needed until every task in the spec can be described concretely. No ambiguous "figure out X" tasks.

**5. Write Spec** — Synthesizes all research and interviews into a structured SPEC.md with phases, tasks, a decision log, and resume context.

**6. Implement** — Works through the spec task by task, checking them off, updating progress, logging new decisions.

### Specs Are Files

Specs live in `.specs/` at your project root — plain markdown with YAML frontmatter. They diff cleanly in git, are readable in any editor, and work with any AI tool.

```
.specs/
├── active                          # Which spec is active (plain text)
├── registry.md                     # Index of all specs
├── research/
│   └── user-auth-system/
│       ├── research-01.md          # Initial codebase + web research
│       ├── interview-01.md         # First interview round
│       ├── research-02.md          # Follow-up research
│       └── interview-02.md         # Second interview round
└── specs/
    └── user-auth-system/
        └── SPEC.md                 # The spec document
```

### A SPEC.md Looks Like This

```markdown
---
id: user-auth-system
title: User Auth System
status: active
created: 2026-02-10
updated: 2026-02-11
priority: high
tags: [auth, security, backend]
---

# User Auth System

## Overview
Add JWT-based authentication with OAuth (Google, GitHub) to the Express
API. Uses the existing middleware pattern in src/middleware/.

## Phase 1: Foundation [completed]
- [x] Set up auth middleware in src/middleware/auth.ts
- [x] Create User model with Prisma schema
- [x] Implement JWT generation and verification in src/auth/tokens.ts
- [x] Add refresh token rotation

## Phase 2: OAuth Integration [in-progress]
- [x] Google OAuth provider
- [ ] GitHub OAuth provider ← current
- [ ] Token exchange flow for both providers

## Phase 3: Testing & Hardening [pending]
- [ ] Unit tests for auth middleware
- [ ] Integration tests for OAuth flow
- [ ] Rate limiting on auth endpoints

---

## Resume Context
> Finished Google OAuth. GitHub OAuth callback handler is in progress at
> `src/auth/oauth/github.ts`. The authorization URL redirect works but
> the callback endpoint at `/auth/github/callback` needs to exchange the
> code for tokens. Use the same pattern as Google in `src/auth/oauth/google.ts`
> lines 45-82. The GitHub OAuth app credentials are in `.env` as
> GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET.

## Decision Log
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-10 | JWT over sessions | Stateless, scales for microservices |
| 2026-02-10 | Refresh token rotation | Limits damage from stolen tokens |
| 2026-02-11 | Prisma over raw SQL | Already used in the project for other models |
```

## Installation

### CLI (Any Terminal)

SpecSmith CLI works standalone from any terminal, with any AI tool, or no AI at all.

```bash
# Core CLI
pipx install specsmith

# With AI-assisted spec generation
pipx install "specsmith[ai]"
```

Quick start:

```bash
specsmith init                        # Initialize .specs/ in your project
specsmith new "User Auth System"      # Create a new spec
specsmith status                      # Show progress
specsmith list                        # List all specs
specsmith pause                       # Pause current spec
specsmith switch other-spec-id        # Switch to another spec
specsmith setup cursor                # Configure a tool
specsmith forge "add auth"            # AI-assisted spec creation
```

See the full [CLI documentation](cli/README.md) for all commands and options.

## Plan Mode

SpecSmith **bypasses** Claude Code's built-in plan mode. The `/forge`
command IS your planning phase — deep research, interviews, spec writing.
You don't need plan mode at all.

If you happen to be in plan mode when you run `/forge`, it still works:
- Research and interviews are read-only and run fine
- When it's time to write the spec, you'll be asked to exit plan mode
  (Shift+Tab) so files can be created

### Claude Code (Full Plugin — Recommended)

Installs everything: `/forge`, `/resume`, `/pause`, `/switch`, `/list`, `/status` commands, the researcher agent, session hooks, and the core skill.

```bash
# In Claude Code, run:
/plugin marketplace add ngvoicu/specsmith-forge
/plugin install spec-smith
```

Or manually:
```bash
git clone https://github.com/ngvoicu/specsmith-forge.git ~/.claude/plugins/spec-smith
```

### Claude Code (Skill Only via npx)

Installs just the SKILL.md — you get auto-triggers (session start detection, "resume", "what was I working on") but **not** the `/forge`, `/resume`, `/pause` commands or the researcher agent.

```bash
npx skills add ngvoicu/specsmith-forge -a claude-code
```

This is the lightweight option. Good if you just want spec tracking without the full research-interview workflow.

### What's the Difference?

| Feature | Plugin (full) | Skill only (npx) |
|---------|:---:|:---:|
| Spec tracking (create, resume, pause, switch) | Yes | Yes |
| `/spec-smith:forge` research-interview workflow | Yes | No |
| `/spec-smith:resume`, `/pause`, `/switch` commands | Yes | No |
| Researcher subagent (Opus, deep codebase analysis) | Yes | No |
| Session start hook (detects active spec) | Yes | No |
| Auto-triggers on "resume", "what was I working on" | Yes | Yes |
| Works with Codex, Cursor, Windsurf | — | — |

For other tools, both paths produce the same result since they rely on the SKILL.md instructions and `.specs/` files.

### Codex

Add the snippet from `references/tool-setup.md` to your `AGENTS.md`. This teaches Codex how to read, update, and resume specs.

### Cursor / Windsurf / Cline

Add the snippet from `references/tool-setup.md` to `.cursorrules`, `.windsurfrules`, or `.clinerules` respectively.

## Commands

| Command | What it does |
|---------|-------------|
| `/spec-smith:forge <description>` | **The main workflow.** Research → interview → spec → implement |
| `/spec-smith:resume` | Resume the active spec from where you left off |
| `/spec-smith:pause` | Pause with detailed resume context |
| `/spec-smith:switch <id>` | Switch to a different spec (pauses current) |
| `/spec-smith:list` | List all specs grouped by status |
| `/spec-smith:status` | Detailed progress of the active spec |

You can also use natural language — "resume", "what was I working on", "show my specs", "switch to the auth spec", "pause this".

## Multi-Tool Support

The spec format is pure markdown. If you use Claude Code for complex features and Codex for batch tasks, they share the same `.specs/` directory. The `← current` marker and resume context keep them in sync.

One rule: don't run two tools on the same spec simultaneously. Different specs in parallel is fine.

## Plugin Structure

```
specsmith-forge/
├── .claude-plugin/
│   ├── plugin.json                 # Plugin metadata
│   └── marketplace.json            # Marketplace registration
├── commands/
│   ├── forge.md                    # Research → interview → spec → implement
│   ├── resume.md                   # Resume active spec
│   ├── pause.md                    # Pause with context
│   ├── switch.md                   # Switch between specs
│   ├── list.md                     # List all specs
│   └── status.md                   # Detailed progress
├── agents/
│   └── researcher.md               # Deep research subagent
├── hooks/
│   └── hooks.json                  # SessionStart detection
├── SKILL.md                        # Core skill (auto-triggers)
├── references/
│   ├── spec-format.md              # SPEC.md template and format spec
│   └── tool-setup.md               # Setup snippets for Codex, Cursor, etc.
└── scripts/
    ├── init_specs.py               # Initialize .specs/ directory
    ├── new_spec.py                 # Create a spec from CLI
    └── spec_status.py              # Show progress from CLI
```

## Why Not Just Use Plan Mode?

Plan mode is a good idea with a bad implementation. It restricts Claude to read-only tools and asks for a plan. That's it. No persistence, no research depth, no interviews, no progress tracking.

Spec Smith's `/forge` command does what plan mode should do:

- **Research depth**: Reads 10-20+ files, searches the web, pulls library docs. Not a quick scan.
- **Interviews**: Asks you targeted questions based on what it found. Multiple rounds until there's no ambiguity.
- **Persistence**: Everything is saved to files. Research notes, interviews, the spec itself. Nothing lives only in context.
- **Resumability**: Close the terminal, come back next week. The spec remembers exactly where you were.
- **Multi-spec**: Juggle multiple features. Switch between them with one command.

## License

MIT
