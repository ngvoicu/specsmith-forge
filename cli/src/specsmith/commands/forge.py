"""specsmith forge — AI-assisted spec creation (requires ANTHROPIC_API_KEY)."""

import os
from datetime import date
from pathlib import Path

import typer

from specsmith.core.active import set_active
from specsmith.core.paths import specs_dir, spec_path
from specsmith.core.registry import rebuild_registry
from specsmith.core.slugify import slugify
from specsmith.display import console


def forge(
    project_root: Path,
    description: str,
    model: str = "claude-sonnet-4-20250514",
    include: list[str] | None = None,
    edit_after: bool = False,
    dry_run: bool = False,
    api_key: str | None = None,
) -> None:
    try:
        from specsmith.ai.forge import generate_spec  # noqa: WPS433
    except ImportError:
        console.print(
            "[red]AI dependencies not installed.[/red]\n\n"
            "Install with: [bold]pip install specsmith\\[ai][/bold]"
        )
        raise typer.Exit(1)

    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        console.print(
            "[red]ANTHROPIC_API_KEY not set.[/red]\n\n"
            "Set it via environment variable or --api-key flag."
        )
        raise typer.Exit(1)

    sd = specs_dir(project_root)
    if not sd.exists():
        console.print("[red]Error:[/red] .specs/ not found. Run [bold]specsmith init[/bold] first.")
        raise typer.Exit(1)

    console.print(f"[bold]Forging spec:[/bold] {description}\n")

    with console.status("Gathering project context..."):
        from specsmith.ai.forge import gather_context
        context = gather_context(project_root, include or [])

    with console.status(f"Calling {model}..."):
        spec_content = generate_spec(key, model, description, context)

    if dry_run:
        console.print("\n[bold]Generated SPEC.md:[/bold]\n")
        console.print(spec_content)
        return

    # Extract id from generated frontmatter
    from specsmith.core.parser import parse_frontmatter
    meta, _ = parse_frontmatter(spec_content)
    spec_id = meta.get("id") or slugify(description)

    sp = spec_path(project_root, spec_id)
    if sp.parent.exists():
        console.print(f"[yellow]Warning:[/yellow] Spec '{spec_id}' already exists, overwriting.")
    sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text(spec_content)

    set_active(project_root, spec_id)
    rebuild_registry(project_root)

    console.print(f"\n[green]Created spec:[/green] {spec_id}")
    console.print(f"  {sp}")

    if edit_after:
        from specsmith.commands.edit import edit
        edit(project_root, spec_id)
