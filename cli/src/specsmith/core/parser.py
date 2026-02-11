"""YAML frontmatter + markdown parsing for SPEC.md files."""

import re

import yaml


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content.

    Returns (metadata_dict, body_string).
    """
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1])
                return meta or {}, parts[2]
            except yaml.YAMLError:
                pass
    return {}, content


def update_frontmatter(content: str, updates: dict) -> str:
    """Update YAML frontmatter fields without disturbing the markdown body.

    Merges *updates* into existing frontmatter. Uses sort_keys=False to
    preserve field order.
    """
    meta, body = parse_frontmatter(content)
    meta.update(updates)
    yaml_str = yaml.dump(meta, default_flow_style=False, sort_keys=False, allow_unicode=True).strip()
    return f"---\n{yaml_str}\n---{body}"


def parse_progress(body: str) -> dict:
    """Parse phases and tasks from spec body.

    Returns dict with keys: phases (list), total_done (int), total_all (int).
    """
    phases: list[dict] = []
    current_phase: dict | None = None

    for line in body.split("\n"):
        phase_match = re.match(
            r"^##\s+(?:Phase\s+\d+:\s*)?(.+?)\s*\[(\w[\w-]*)\]\s*$", line
        )
        if phase_match:
            current_phase = {
                "name": phase_match.group(1).strip(),
                "status": phase_match.group(2),
                "tasks_done": 0,
                "tasks_total": 0,
                "current_task": None,
            }
            phases.append(current_phase)
            continue

        if current_phase is None:
            continue

        task_done = re.match(r"^\s*-\s*\[x\]\s+(.+)", line)
        task_todo = re.match(r"^\s*-\s*\[\s\]\s+(.+)", line)

        if task_done:
            current_phase["tasks_done"] += 1
            current_phase["tasks_total"] += 1
        elif task_todo:
            current_phase["tasks_total"] += 1
            desc = task_todo.group(1).strip()
            if "\u2190 current" in desc:
                current_phase["current_task"] = desc.replace("\u2190 current", "").strip()

    total_done = sum(p["tasks_done"] for p in phases)
    total_all = sum(p["tasks_total"] for p in phases)

    return {
        "phases": phases,
        "total_done": total_done,
        "total_all": total_all,
    }


def get_resume_context(body: str) -> str:
    """Extract the Resume Context section from a spec body."""
    in_context = False
    lines: list[str] = []
    for line in body.split("\n"):
        if re.match(r"^##\s+Resume Context", line):
            in_context = True
            continue
        if in_context:
            if line.startswith("## "):
                break
            stripped = line.lstrip("> ").strip()
            if stripped:
                lines.append(stripped)
    return " ".join(lines)[:200] if lines else "No resume context saved."
