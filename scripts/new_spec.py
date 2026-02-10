#!/usr/bin/env python3
"""Create a new spec from a title and optional description.

Usage:
    python new_spec.py <title> [--path <project-root>] [--priority high|medium|low]

Creates a new spec directory and SPEC.md, updates registry and active file.
"""

import argparse
import os
import re
import sys
from datetime import date


def slugify(title: str) -> str:
    """Convert title to a URL-safe spec ID."""
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


SPEC_TEMPLATE = """---
id: {id}
title: {title}
status: active
created: {date}
updated: {date}
priority: {priority}
tags: []
---

# {title}

## Overview

<!-- Describe what this spec accomplishes and why. -->

## Phase 1: Setup [in-progress]

- [ ] Task 1 ← current
- [ ] Task 2
- [ ] Task 3

## Phase 2: Implementation [pending]

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Phase 3: Testing & Polish [pending]

- [ ] Task 1
- [ ] Task 2

---

## Resume Context

> Spec just created. No work started yet.

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
"""


def create_spec(project_root: str, title: str, priority: str = "medium") -> str:
    specs_dir = os.path.join(project_root, ".specs")
    if not os.path.exists(specs_dir):
        print("Error: .specs/ not found. Run init_specs.py first.", file=sys.stderr)
        sys.exit(1)

    spec_id = slugify(title)
    spec_dir = os.path.join(specs_dir, "specs", spec_id)

    if os.path.exists(spec_dir):
        print(f"Error: Spec '{spec_id}' already exists.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(spec_dir)

    # Write SPEC.md
    today = date.today().isoformat()
    spec_content = SPEC_TEMPLATE.format(
        id=spec_id, title=title, date=today, priority=priority
    )
    spec_path = os.path.join(spec_dir, "SPEC.md")
    with open(spec_path, "w") as f:
        f.write(spec_content)
    print(f"Created {spec_path}")

    # Update registry
    registry_path = os.path.join(specs_dir, "registry.md")
    if os.path.exists(registry_path):
        with open(registry_path, "a") as f:
            f.write(f"| {spec_id} | {title} | active | {priority} | {today} |\n")
        print(f"Updated {registry_path}")

    # Set as active if nothing else is
    active_path = os.path.join(specs_dir, "active")
    current_active = ""
    if os.path.exists(active_path):
        with open(active_path, "r") as f:
            current_active = f.read().strip()

    if not current_active:
        with open(active_path, "w") as f:
            f.write(spec_id)
        print(f"Set '{spec_id}' as active spec")
    else:
        print(f"Note: '{current_active}' is still the active spec")
        print(f"Run: spec activate {spec_id} to switch")

    return spec_id


def main():
    parser = argparse.ArgumentParser(description="Create a new spec")
    parser.add_argument("title", help="Spec title (e.g., 'User Auth System')")
    parser.add_argument(
        "--path", default=".", help="Project root directory (default: current)"
    )
    parser.add_argument(
        "--priority",
        default="medium",
        choices=["high", "medium", "low"],
        help="Spec priority (default: medium)",
    )
    args = parser.parse_args()

    project_root = os.path.abspath(args.path)
    spec_id = create_spec(project_root, args.title, args.priority)
    print(f"\nSpec '{spec_id}' created. Edit .specs/specs/{spec_id}/SPEC.md to fill in phases and tasks.")


if __name__ == "__main__":
    main()
