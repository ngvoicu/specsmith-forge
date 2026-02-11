"""specsmith archive — Archive a spec."""

from datetime import date
from pathlib import Path

import typer

from specsmith.core.active import get_active, clear_active
from specsmith.core.parser import update_frontmatter
from specsmith.core.paths import spec_path
from specsmith.core.registry import rebuild_registry
from specsmith.display import console


def archive(project_root: Path, spec_id: str) -> None:
    sp = spec_path(project_root, spec_id)
    if not sp.exists():
        console.print(f"[red]Spec not found:[/red] {spec_id}")
        raise typer.Exit(1)

    content = sp.read_text()
    content = update_frontmatter(content, {
        "status": "archived",
        "updated": date.today().isoformat(),
    })
    sp.write_text(content)

    active = get_active(project_root)
    if active == spec_id:
        clear_active(project_root)

    rebuild_registry(project_root)
    console.print(f"Archived [bold]{spec_id}[/bold] \U0001f4e6")
