"""specsmith edit — Open SPEC.md in $EDITOR."""

import os
import subprocess
from pathlib import Path

import typer

from specsmith.core.active import get_active
from specsmith.core.paths import spec_path
from specsmith.display import console


def edit(project_root: Path, spec_id: str | None = None) -> None:
    if spec_id is None:
        spec_id = get_active(project_root)
    if not spec_id:
        console.print("[yellow]No active spec to edit.[/yellow] Provide a spec ID.")
        raise typer.Exit(1)

    sp = spec_path(project_root, spec_id)
    if not sp.exists():
        console.print(f"[red]Spec not found:[/red] {spec_id}")
        raise typer.Exit(1)

    editor = os.environ.get("EDITOR", "vi")
    subprocess.run([editor, str(sp)])
