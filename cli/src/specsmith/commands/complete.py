"""specsmith complete — Mark a spec as completed."""

from datetime import date
from pathlib import Path

import typer

from specsmith.core.active import get_active, clear_active
from specsmith.core.parser import parse_frontmatter, parse_progress, update_frontmatter
from specsmith.core.paths import spec_path
from specsmith.core.registry import rebuild_registry
from specsmith.display import console


def complete(project_root: Path, spec_id: str | None = None, force: bool = False) -> None:
    if spec_id is None:
        spec_id = get_active(project_root)
    if not spec_id:
        console.print("[yellow]No active spec to complete.[/yellow]")
        raise typer.Exit(1)

    sp = spec_path(project_root, spec_id)
    if not sp.exists():
        console.print(f"[red]Spec not found:[/red] {spec_id}")
        raise typer.Exit(1)

    content = sp.read_text()
    meta, body = parse_frontmatter(content)
    progress = parse_progress(body)

    if progress["total_done"] < progress["total_all"] and not force:
        remaining = progress["total_all"] - progress["total_done"]
        console.print(
            f"[yellow]Warning:[/yellow] {remaining} task(s) not completed. "
            f"Use [bold]--force[/bold] to complete anyway."
        )
        raise typer.Exit(1)

    content = update_frontmatter(content, {
        "status": "completed",
        "updated": date.today().isoformat(),
    })
    sp.write_text(content)

    active = get_active(project_root)
    if active == spec_id:
        clear_active(project_root)

    rebuild_registry(project_root)
    console.print(f"Completed [bold]{spec_id}[/bold] \u2713")
