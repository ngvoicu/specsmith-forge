#!/usr/bin/env python3
"""Show status of the active spec or all specs.

Usage:
    python spec_status.py [--path <project-root>] [--all]

Reads the active spec and displays progress, or lists all specs.
"""

import argparse
import os
import re
import sys
import yaml


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1])
                return meta or {}, parts[2]
            except yaml.YAMLError:
                pass
    return {}, content


def parse_progress(body: str) -> dict:
    """Parse phases and tasks from spec body."""
    phases = []
    current_phase = None

    for line in body.split("\n"):
        # Match phase headings: ## Phase N: Name [status]
        phase_match = re.match(
            r"^##\s+(?:Phase\s+\d+:\s*)?(.+?)\s*\[(\w[\w-]*)\]\s*$", line
        )
        if phase_match:
            current_phase = {
                "name": phase_match.group(1).strip(),
                "status": phase_match.group(2),
                "tasks_done": 0,
                "tasks_total": 0,
                "current_task": None,
            }
            phases.append(current_phase)
            continue

        if current_phase is None:
            continue

        # Match tasks
        task_done = re.match(r"^\s*-\s*\[x\]\s+(.+)", line)
        task_todo = re.match(r"^\s*-\s*\[\s\]\s+(.+)", line)

        if task_done:
            current_phase["tasks_done"] += 1
            current_phase["tasks_total"] += 1
        elif task_todo:
            current_phase["tasks_total"] += 1
            desc = task_todo.group(1).strip()
            if "← current" in desc:
                current_phase["current_task"] = desc.replace("← current", "").strip()

    total_done = sum(p["tasks_done"] for p in phases)
    total_all = sum(p["tasks_total"] for p in phases)

    return {
        "phases": phases,
        "total_done": total_done,
        "total_all": total_all,
    }


def get_resume_context(body: str) -> str:
    """Extract the Resume Context section."""
    in_context = False
    lines = []
    for line in body.split("\n"):
        if re.match(r"^##\s+Resume Context", line):
            in_context = True
            continue
        if in_context:
            if line.startswith("## "):
                break
            stripped = line.lstrip("> ").strip()
            if stripped:
                lines.append(stripped)
    return " ".join(lines)[:200] if lines else "No resume context saved."


def show_spec_status(project_root: str, spec_id: str) -> None:
    """Display status for a single spec."""
    spec_path = os.path.join(project_root, ".specs", "specs", spec_id, "SPEC.md")
    if not os.path.exists(spec_path):
        print(f"Spec not found: {spec_id}", file=sys.stderr)
        return

    with open(spec_path) as f:
        content = f.read()

    meta, body = parse_frontmatter(content)
    progress = parse_progress(body)
    context = get_resume_context(body)

    title = meta.get("title", spec_id)
    status = meta.get("status", "unknown")
    priority = meta.get("priority", "medium")

    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"  Status: {status} | Priority: {priority}")
    print(f"  Progress: {progress['total_done']}/{progress['total_all']} tasks")
    print(f"{'='*60}")

    for phase in progress["phases"]:
        icon = {"completed": "✓", "in-progress": "→", "pending": "○", "blocked": "✕"}
        marker = icon.get(phase["status"], "?")
        print(
            f"  {marker} {phase['name']} [{phase['tasks_done']}/{phase['tasks_total']}]"
        )
        if phase["current_task"]:
            print(f"    ↳ Current: {phase['current_task']}")

    print(f"\n  Context: {context}")
    print()


def show_all_specs(project_root: str) -> None:
    """List all specs with status."""
    specs_dir = os.path.join(project_root, ".specs", "specs")
    active_path = os.path.join(project_root, ".specs", "active")

    active_id = ""
    if os.path.exists(active_path):
        with open(active_path) as f:
            active_id = f.read().strip()

    if not os.path.exists(specs_dir):
        print("No specs found. Run init_specs.py first.")
        return

    specs = []
    for entry in sorted(os.listdir(specs_dir)):
        spec_path = os.path.join(specs_dir, entry, "SPEC.md")
        if os.path.exists(spec_path):
            with open(spec_path) as f:
                content = f.read()
            meta, body = parse_frontmatter(content)
            progress = parse_progress(body)
            specs.append(
                {
                    "id": entry,
                    "title": meta.get("title", entry),
                    "status": meta.get("status", "unknown"),
                    "priority": meta.get("priority", "medium"),
                    "done": progress["total_done"],
                    "total": progress["total_all"],
                    "is_active": entry == active_id,
                }
            )

    if not specs:
        print("No specs found.")
        return

    # Group by status
    groups = {"active": [], "paused": [], "completed": [], "archived": []}
    for s in specs:
        groups.setdefault(s["status"], []).append(s)

    icons = {"active": "→", "paused": "⏸", "completed": "✓", "archived": "📦"}

    for status in ["active", "paused", "completed", "archived"]:
        if groups.get(status):
            print(f"\n{status.capitalize()}:")
            for s in groups[status]:
                icon = icons.get(status, "?")
                active_marker = " (active)" if s["is_active"] else ""
                print(
                    f"  {icon} {s['id']}: {s['title']} ({s['done']}/{s['total']} tasks){active_marker}"
                )


def main():
    parser = argparse.ArgumentParser(description="Show spec status")
    parser.add_argument("--path", default=".", help="Project root directory")
    parser.add_argument("--all", action="store_true", help="Show all specs")
    args = parser.parse_args()

    project_root = os.path.abspath(args.path)

    if args.all:
        show_all_specs(project_root)
    else:
        active_path = os.path.join(project_root, ".specs", "active")
        if not os.path.exists(active_path):
            print("No .specs/ directory found. Run init_specs.py first.")
            sys.exit(1)

        with open(active_path) as f:
            active_id = f.read().strip()

        if not active_id:
            print("No active spec. Use --all to see all specs.")
            show_all_specs(project_root)
        else:
            show_spec_status(project_root, active_id)


if __name__ == "__main__":
    main()
