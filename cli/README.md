# SpecSmith CLI

**Spec-driven development from the terminal.**

SpecSmith turns ephemeral AI coding plans into persistent, resumable specs. Create a spec, work through it task by task, pause, switch to another spec, come back a week later and pick up exactly where you left off.

Works with any AI coding tool — or no AI at all.

## Installation

```bash
# Core CLI
pipx install specsmith

# With AI-assisted spec generation
pipx install "specsmith[ai]"
```

## Quick Start

```bash
# Initialize specs in your project
specsmith init

# Create a new spec
specsmith new "User Auth System"

# Check progress
specsmith status

# List all specs
specsmith list

# Pause current spec
specsmith pause

# Switch to another spec
specsmith switch other-spec-id

# Resume a spec
specsmith resume my-spec-id

# Complete a spec
specsmith complete

# Archive a spec
specsmith archive old-spec-id

# Open spec in your editor
specsmith edit

# Configure a tool (cursor, codex, windsurf, cline, aider, gemini)
specsmith setup cursor

# AI-assisted spec creation (requires ANTHROPIC_API_KEY)
specsmith forge "add user authentication with OAuth"
```

## Commands

| Command | Description |
|---------|-------------|
| `specsmith init` | Initialize `.specs/` in the current project |
| `specsmith new <title>` | Create a new spec from a title |
| `specsmith status [spec-id]` | Show progress (default: active spec) |
| `specsmith list` | List all specs grouped by status |
| `specsmith switch <spec-id>` | Switch active spec |
| `specsmith pause [spec-id]` | Mark spec as paused |
| `specsmith resume [spec-id]` | Reactivate a spec |
| `specsmith complete [spec-id]` | Mark spec as completed |
| `specsmith archive <spec-id>` | Archive a spec |
| `specsmith edit [spec-id]` | Open SPEC.md in `$EDITOR` |
| `specsmith setup <tool>` | Auto-configure a coding tool |
| `specsmith forge <description>` | AI-assisted spec creation |
| `specsmith version` | Show version |

### Global Flags

- `--path / -p <dir>` — Project root directory
- `--no-color` — Disable colour output
- `--json` — Output as JSON
- `--verbose / -v` — Verbose output

## Tool Setup

SpecSmith works with any AI coding tool. Use `specsmith setup <tool>` to auto-configure:

- **Cursor** — appends to `.cursor/rules` or `.cursorrules`
- **Windsurf** — appends to `.windsurfrules`
- **Cline** — appends to `.clinerules`
- **Codex** — appends to `AGENTS.md`
- **Aider** — appends to `.aider/conventions.md`
- **Gemini** — appends to `GEMINI.md`
- **Claude Code** — prints plugin install instructions

## AI Forge

The `forge` command uses the Anthropic API to generate specs from a description:

```bash
export ANTHROPIC_API_KEY=your-key
specsmith forge "add real-time collaboration"
```

Options:
- `--model` — Claude model (default: `claude-sonnet-4-20250514`)
- `--include <path>` — Add files to context
- `--edit` — Open in `$EDITOR` after creation
- `--dry-run` — Print to stdout
- `--api-key` — API key (alternative to env var)

## License

MIT
