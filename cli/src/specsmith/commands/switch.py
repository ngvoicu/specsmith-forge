"""specsmith switch — Switch active spec (pause current + resume target)."""

from pathlib import Path

import typer

from specsmith.core.active import get_active
from specsmith.core.paths import spec_path
from specsmith.commands.pause import pause
from specsmith.commands.resume import resume
from specsmith.display import console


def switch(project_root: Path, target_id: str) -> None:
    sp = spec_path(project_root, target_id)
    if not sp.exists():
        console.print(f"[red]Spec not found:[/red] {target_id}")
        raise typer.Exit(1)

    current = get_active(project_root)
    if current == target_id:
        console.print(f"'{target_id}' is already the active spec.")
        return

    if current:
        pause(project_root, current)

    resume(project_root, target_id)
    console.print(f"\nSwitched to [bold]{target_id}[/bold]")
