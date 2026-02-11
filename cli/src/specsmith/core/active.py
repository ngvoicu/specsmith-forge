"""Read/write the .specs/active file."""

from pathlib import Path

from specsmith.core.paths import active_path


def get_active(project_root: Path) -> str:
    """Return the active spec ID, or empty string if none."""
    path = active_path(project_root)
    if path.exists():
        return path.read_text().strip()
    return ""


def set_active(project_root: Path, spec_id: str) -> None:
    """Set the active spec ID."""
    active_path(project_root).write_text(spec_id)


def clear_active(project_root: Path) -> None:
    """Clear the active spec."""
    active_path(project_root).write_text("")
