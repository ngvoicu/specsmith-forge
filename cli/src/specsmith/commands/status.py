"""specsmith status — Show progress of a spec."""

from pathlib import Path

import typer

from specsmith.core.active import get_active
from specsmith.core.parser import parse_frontmatter, parse_progress, get_resume_context
from specsmith.core.paths import spec_path
from specsmith.display import console, print_spec_panel, print_phases, print_context


def status(project_root: Path, spec_id: str | None = None) -> None:
    if spec_id is None:
        spec_id = get_active(project_root)
    if not spec_id:
        console.print("[yellow]No active spec.[/yellow] Use [bold]specsmith list[/bold] to see all specs.")
        raise typer.Exit(1)

    sp = spec_path(project_root, spec_id)
    if not sp.exists():
        console.print(f"[red]Spec not found:[/red] {spec_id}")
        raise typer.Exit(1)

    content = sp.read_text()
    meta, body = parse_frontmatter(content)
    progress = parse_progress(body)
    context = get_resume_context(body)

    title = meta.get("title", spec_id)
    st = meta.get("status", "unknown")
    priority = meta.get("priority", "medium")

    print_spec_panel(title, st, priority, progress["total_done"], progress["total_all"])
    print_phases(progress["phases"])
    print_context(context)
