#!/usr/bin/env python3
"""Initialize the .specs directory structure for Spec Smith.

Usage:
    python init_specs.py [--path <project-root>]

Creates:
    .specs/
    .specs/active
    .specs/registry.md
    .specs/specs/
"""

import argparse
import os
import sys
from datetime import date


REGISTRY_TEMPLATE = """# Spec Registry

| ID | Title | Status | Priority | Updated |
|----|-------|--------|----------|---------|
"""

GITIGNORE_SUGGESTION = """
# Consider adding to your .gitignore if you don't want specs in version control:
# .specs/
#
# Or track them (recommended) — specs are useful project documentation.
"""


def init_specs(project_root: str) -> None:
    specs_dir = os.path.join(project_root, ".specs")
    specs_subdir = os.path.join(specs_dir, "specs")

    if os.path.exists(specs_dir):
        print(f".specs/ already exists at {specs_dir}")
        print("Checking for missing files...")
    else:
        os.makedirs(specs_dir)
        print(f"Created {specs_dir}/")

    # Create specs subdirectory
    if not os.path.exists(specs_subdir):
        os.makedirs(specs_subdir)
        print(f"Created {specs_subdir}/")

    # Create active file (empty = no active spec)
    active_path = os.path.join(specs_dir, "active")
    if not os.path.exists(active_path):
        with open(active_path, "w") as f:
            f.write("")
        print(f"Created {active_path}")

    # Create registry
    registry_path = os.path.join(specs_dir, "registry.md")
    if not os.path.exists(registry_path):
        with open(registry_path, "w") as f:
            f.write(REGISTRY_TEMPLATE.lstrip())
        print(f"Created {registry_path}")

    print("\n.specs/ initialized successfully.")
    print(GITIGNORE_SUGGESTION)


def main():
    parser = argparse.ArgumentParser(
        description="Initialize .specs directory for Spec Smith"
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Project root directory (default: current directory)",
    )
    args = parser.parse_args()

    project_root = os.path.abspath(args.path)
    if not os.path.isdir(project_root):
        print(f"Error: {project_root} is not a directory", file=sys.stderr)
        sys.exit(1)

    init_specs(project_root)


if __name__ == "__main__":
    main()
