"""specsmith resume — Reactivate a paused spec."""

from datetime import date
from pathlib import Path

import typer

from specsmith.core.active import get_active, set_active
from specsmith.core.parser import parse_frontmatter, update_frontmatter
from specsmith.core.paths import spec_path
from specsmith.core.registry import rebuild_registry
from specsmith.display import console


def resume(project_root: Path, spec_id: str | None = None) -> None:
    if spec_id is None:
        spec_id = get_active(project_root)
    if not spec_id:
        console.print("[yellow]No spec to resume.[/yellow] Provide a spec ID.")
        raise typer.Exit(1)

    sp = spec_path(project_root, spec_id)
    if not sp.exists():
        console.print(f"[red]Spec not found:[/red] {spec_id}")
        raise typer.Exit(1)

    content = sp.read_text()
    meta, _ = parse_frontmatter(content)

    if meta.get("status") == "active":
        console.print(f"'{spec_id}' is already active.")
        set_active(project_root, spec_id)
        return

    content = update_frontmatter(content, {
        "status": "active",
        "updated": date.today().isoformat(),
    })
    sp.write_text(content)

    set_active(project_root, spec_id)
    rebuild_registry(project_root)
    console.print(f"Resumed [bold]{spec_id}[/bold]")
