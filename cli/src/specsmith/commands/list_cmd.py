"""specsmith list — List all specs grouped by status."""

from pathlib import Path

import typer

from specsmith.core.active import get_active
from specsmith.core.parser import parse_frontmatter, parse_progress
from specsmith.core.paths import specs_subdir
from specsmith.display import console, print_spec_table


def list_specs(project_root: Path) -> None:
    sdir = specs_subdir(project_root)
    active_id = get_active(project_root)

    if not sdir.is_dir():
        console.print("[yellow]No specs found.[/yellow] Run [bold]specsmith init[/bold] first.")
        raise typer.Exit(1)

    specs: list[dict] = []
    for entry in sorted(sdir.iterdir()):
        spec_file = entry / "SPEC.md"
        if spec_file.is_file():
            content = spec_file.read_text()
            meta, body = parse_frontmatter(content)
            progress = parse_progress(body)
            specs.append({
                "id": entry.name,
                "title": meta.get("title", entry.name),
                "status": meta.get("status", "unknown"),
                "priority": meta.get("priority", "medium"),
                "done": progress["total_done"],
                "total": progress["total_all"],
            })

    if not specs:
        console.print("[yellow]No specs found.[/yellow]")
        return

    print_spec_table(specs, active_id)
