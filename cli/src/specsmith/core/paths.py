"""Path discovery and helpers for the .specs/ directory."""

from pathlib import Path


def find_specs_root(start: Path | None = None) -> Path | None:
    """Walk up directories from *start* to find a .specs/ directory.

    Returns the project root (parent of .specs/) or None.
    """
    current = (start or Path.cwd()).resolve()
    while True:
        if (current / ".specs").is_dir():
            return current
        parent = current.parent
        if parent == current:
            return None
        current = parent


def specs_dir(project_root: Path) -> Path:
    return project_root / ".specs"


def specs_subdir(project_root: Path) -> Path:
    return project_root / ".specs" / "specs"


def spec_path(project_root: Path, spec_id: str) -> Path:
    return project_root / ".specs" / "specs" / spec_id / "SPEC.md"


def active_path(project_root: Path) -> Path:
    return project_root / ".specs" / "active"


def registry_path(project_root: Path) -> Path:
    return project_root / ".specs" / "registry.md"
