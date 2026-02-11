"""Registry rebuild from SPEC.md files."""

from pathlib import Path

from specsmith.core.parser import parse_frontmatter
from specsmith.core.paths import registry_path, specs_subdir


REGISTRY_HEADER = """\
# Spec Registry

| ID | Title | Status | Priority | Updated |
|----|-------|--------|----------|---------|
"""


def rebuild_registry(project_root: Path) -> None:
    """Regenerate registry.md from all SPEC.md frontmatters."""
    sdir = specs_subdir(project_root)
    rows: list[str] = []

    if sdir.is_dir():
        for entry in sorted(sdir.iterdir()):
            spec_file = entry / "SPEC.md"
            if spec_file.is_file():
                content = spec_file.read_text()
                meta, _ = parse_frontmatter(content)
                sid = meta.get("id", entry.name)
                title = meta.get("title", entry.name)
                status = meta.get("status", "unknown")
                priority = meta.get("priority", "medium")
                updated = meta.get("updated", "")
                rows.append(f"| {sid} | {title} | {status} | {priority} | {updated} |")

    registry = REGISTRY_HEADER + "\n".join(rows) + "\n"
    registry_path(project_root).write_text(registry)
