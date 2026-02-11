"""Rich output helpers for the SpecSmith CLI."""

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table

console = Console()

STATUS_ICONS = {
    "active": "\u2192",
    "in-progress": "\u2192",
    "paused": "\u23f8",
    "completed": "\u2713",
    "archived": "\U0001f4e6",
    "pending": "\u25cb",
    "blocked": "\u2715",
}


def status_icon(status: str) -> str:
    return STATUS_ICONS.get(status, "?")


def print_spec_panel(title: str, status: str, priority: str, done: int, total: int) -> None:
    pct = (done / total * 100) if total else 0
    content = (
        f"[bold]Status:[/bold] {status}  |  "
        f"[bold]Priority:[/bold] {priority}  |  "
        f"[bold]Progress:[/bold] {done}/{total} tasks ({pct:.0f}%)"
    )
    console.print(Panel(content, title=f"[bold]{title}[/bold]", border_style="cyan"))


def print_phases(phases: list[dict]) -> None:
    for phase in phases:
        icon = status_icon(phase["status"])
        label = f"  {icon} {phase['name']} [{phase['tasks_done']}/{phase['tasks_total']}]"
        console.print(label)
        if phase.get("current_task"):
            console.print(f"    \u21b3 Current: {phase['current_task']}", style="dim")


def print_context(context: str) -> None:
    console.print(f"\n  [bold]Context:[/bold] {context}", style="dim")
    console.print()


def print_spec_table(specs: list[dict], active_id: str) -> None:
    """Print a grouped table of specs."""
    groups: dict[str, list[dict]] = {}
    for s in specs:
        groups.setdefault(s["status"], []).append(s)

    for status in ["active", "paused", "completed", "archived"]:
        items = groups.get(status, [])
        if not items:
            continue
        console.print(f"\n[bold]{status.capitalize()}:[/bold]")
        for s in items:
            icon = status_icon(status)
            marker = " [cyan](active)[/cyan]" if s["id"] == active_id else ""
            console.print(
                f"  {icon} {s['id']}: {s['title']} "
                f"({s['done']}/{s['total']} tasks){marker}"
            )
    console.print()


def print_progress_bar(done: int, total: int) -> None:
    with Progress(
        TextColumn("[bold blue]Progress"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total} tasks"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Progress", total=total, completed=done)
