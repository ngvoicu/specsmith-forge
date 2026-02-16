#!/usr/bin/env bash
# session-start.sh — Rich context injection for Spec Smith
# Reads the registry to find the active spec and outputs a human-readable summary.
# Called by hooks.json on SessionStart (startup, resume, clear, compact).
# Exits 0 silently if no active spec exists.

set -euo pipefail

# --- Guard clauses ---

SPECS_DIR=".specs"

# No .specs directory
[ -d "$SPECS_DIR" ] || exit 0

REGISTRY="$SPECS_DIR/registry.md"

# No registry file
[ -f "$REGISTRY" ] || exit 0

# Find the active spec ID from the registry table (Status column = active)
SPEC_ID="$(awk -F'|' '
  NR <= 2 { next }
  {
    gsub(/^[ \t]+|[ \t]+$/, "", $2)
    gsub(/^[ \t]+|[ \t]+$/, "", $4)
    if (tolower($4) == "active") { print $2; exit }
  }
' "$REGISTRY")"

# No active spec
[ -n "$SPEC_ID" ] || exit 0

SPEC_FILE="$SPECS_DIR/specs/$SPEC_ID/SPEC.md"

# SPEC.md doesn't exist
[ -f "$SPEC_FILE" ] || exit 0

# --- Parse SPEC.md ---

# Extract frontmatter field value (works on both macOS and GNU)
frontmatter_val() {
  awk -v key="$1" '
    /^---$/ { count++; next }
    count == 1 && $0 ~ "^"key":" {
      sub("^"key":[ \t]*", "")
      print
      exit
    }
    count >= 2 { exit }
  ' "$SPEC_FILE"
}

TITLE="$(frontmatter_val title)"
[ -n "$TITLE" ] || TITLE="Unknown"

STATUS="$(frontmatter_val status)"
[ -n "$STATUS" ] || STATUS="unknown"

PRIORITY="$(frontmatter_val priority)"

# Task counts — only within phase sections, stop at Resume Context
COMPLETED="$(awk '/^## Resume Context/ {exit} /^## Phase/ {in_phase=1} in_phase && /^- \[x\]/ {c++} END {print c+0}' "$SPEC_FILE")"
UNCOMPLETED="$(awk '/^## Resume Context/ {exit} /^## Phase/ {in_phase=1} in_phase && /^- \[ \]/ {c++} END {print c+0}' "$SPEC_FILE")"
TOTAL=$((COMPLETED + UNCOMPLETED))

# Current phase: first "## Phase" line containing [in-progress]
CURRENT_PHASE="$(grep -m1 '^## Phase.*\[in-progress\]' "$SPEC_FILE" | sed 's/^## //' | sed 's/ *\[in-progress\].*//' || true)"

# Current task: line containing "← current"
CURRENT_TASK="$(grep -m1 '← current' "$SPEC_FILE" | sed 's/^- \[.\] //' | sed 's/ *← current.*//' || true)"

# Resume context: blockquote lines after "## Resume Context" heading
# Capped at 10 lines to keep the session start summary concise
RESUME_CONTEXT="$(awk '
  /^## Resume Context/ { found=1; next }
  found && /^## / { exit }
  found && /^>/ { sub(/^> ?/, ""); print; count++; if (count>=10) exit }
' "$SPEC_FILE")"

# --- Build output ---

OUTPUT="Active spec: $TITLE (id: $SPEC_ID)"

if [ -n "$PRIORITY" ]; then
  OUTPUT="$OUTPUT [$PRIORITY priority]"
fi

OUTPUT="$OUTPUT
Status: $STATUS"

if [ "$TOTAL" -gt 0 ]; then
  OUTPUT="$OUTPUT
Progress: $COMPLETED/$TOTAL tasks completed"
fi

if [ -n "$CURRENT_PHASE" ]; then
  OUTPUT="$OUTPUT
Current phase: $CURRENT_PHASE"
fi

if [ -n "$CURRENT_TASK" ]; then
  OUTPUT="$OUTPUT
Current task: $CURRENT_TASK"
fi

if [ -n "$RESUME_CONTEXT" ]; then
  # Indent continuation lines for readability
  INDENTED="$(echo "$RESUME_CONTEXT" | sed '2,$s/^/  /')"
  OUTPUT="$OUTPUT
Resume context: $INDENTED"
fi

OUTPUT="$OUTPUT

Say \"resume\" to continue working on this spec, or start something new."

echo "$OUTPUT"
