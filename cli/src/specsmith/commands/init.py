"""specsmith init — Initialize .specs/ in current project."""

from pathlib import Path

import typer

from specsmith.core.paths import specs_dir, specs_subdir, active_path, registry_path
from specsmith.core.registry import REGISTRY_HEADER
from specsmith.display import console


def init(project_root: Path) -> None:
    sd = specs_dir(project_root)
    ss = specs_subdir(project_root)

    if sd.exists():
        console.print(f".specs/ already exists at {sd}")
        console.print("Checking for missing files...")
    else:
        sd.mkdir(parents=True)
        console.print(f"Created {sd}/")

    if not ss.exists():
        ss.mkdir(parents=True)
        console.print(f"Created {ss}/")

    ap = active_path(project_root)
    if not ap.exists():
        ap.write_text("")
        console.print(f"Created {ap}")

    rp = registry_path(project_root)
    if not rp.exists():
        rp.write_text(REGISTRY_HEADER)
        console.print(f"Created {rp}")

    console.print("\n[green].specs/ initialized successfully.[/green]")
