"""specsmith pause — Mark a spec as paused."""

from datetime import date
from pathlib import Path

import typer

from specsmith.core.active import get_active, clear_active
from specsmith.core.parser import parse_frontmatter, update_frontmatter
from specsmith.core.paths import spec_path
from specsmith.core.registry import rebuild_registry
from specsmith.display import console


def pause(project_root: Path, spec_id: str | None = None, context_msg: str | None = None) -> None:
    if spec_id is None:
        spec_id = get_active(project_root)
    if not spec_id:
        console.print("[yellow]No active spec to pause.[/yellow]")
        raise typer.Exit(1)

    sp = spec_path(project_root, spec_id)
    if not sp.exists():
        console.print(f"[red]Spec not found:[/red] {spec_id}")
        raise typer.Exit(1)

    content = sp.read_text()
    meta, _ = parse_frontmatter(content)

    if meta.get("status") == "paused":
        console.print(f"'{spec_id}' is already paused.")
        return

    content = update_frontmatter(content, {
        "status": "paused",
        "updated": date.today().isoformat(),
    })

    if context_msg:
        # Append to Resume Context section
        lines = content.split("\n")
        new_lines: list[str] = []
        in_context = False
        inserted = False
        for line in lines:
            new_lines.append(line)
            if line.startswith("## Resume Context") and not inserted:
                in_context = True
                continue
            if in_context and not inserted:
                if line.startswith("## ") or (line.strip() == "" and new_lines[-2].startswith("## Resume Context")):
                    new_lines.insert(-1, f"> {context_msg}")
                    new_lines.insert(-1, "")
                    inserted = True
                    in_context = False
        if not inserted:
            # Append at the end of Resume Context
            for i, line in enumerate(new_lines):
                if line.startswith("## Resume Context"):
                    # Find the next section or end
                    j = i + 1
                    while j < len(new_lines) and not new_lines[j].startswith("## "):
                        j += 1
                    new_lines.insert(j, f"> {context_msg}")
                    new_lines.insert(j + 1, "")
                    break
        content = "\n".join(new_lines)

    sp.write_text(content)

    # Clear active if this was the active spec
    active = get_active(project_root)
    if active == spec_id:
        clear_active(project_root)

    rebuild_registry(project_root)
    console.print(f"Paused [bold]{spec_id}[/bold]")
