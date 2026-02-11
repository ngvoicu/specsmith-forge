"""specsmith new — Create a new spec from a title."""

from datetime import date
from pathlib import Path

import typer

from specsmith.core.active import get_active, set_active
from specsmith.core.paths import specs_dir, spec_path
from specsmith.core.registry import rebuild_registry
from specsmith.core.slugify import slugify
from specsmith.core.template import render_template
from specsmith.display import console


def new(project_root: Path, title: str, priority: str = "medium") -> str:
    sd = specs_dir(project_root)
    if not sd.exists():
        console.print("[red]Error:[/red] .specs/ not found. Run [bold]specsmith init[/bold] first.")
        raise typer.Exit(1)

    spec_id = slugify(title)
    sp = spec_path(project_root, spec_id)

    if sp.parent.exists():
        console.print(f"[red]Error:[/red] Spec '{spec_id}' already exists.")
        raise typer.Exit(1)

    sp.parent.mkdir(parents=True)

    today = date.today().isoformat()
    content = render_template(spec_id, title, today, priority)
    sp.write_text(content)
    console.print(f"Created {sp}")

    rebuild_registry(project_root)

    current_active = get_active(project_root)
    if not current_active:
        set_active(project_root, spec_id)
        console.print(f"Set '{spec_id}' as active spec")
    else:
        console.print(f"Note: '{current_active}' is still the active spec")
        console.print(f"Run: [bold]specsmith switch {spec_id}[/bold] to switch")

    return spec_id
