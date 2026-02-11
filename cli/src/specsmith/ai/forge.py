"""Context gathering + API call + parse for spec generation."""

import os
from datetime import date
from pathlib import Path

from specsmith.ai.client import create_client
from specsmith.ai.prompts import SYSTEM_PROMPT
from specsmith.core.paths import specs_subdir


def gather_context(project_root: Path, include_paths: list[str]) -> str:
    """Gather project context for the AI prompt."""
    parts: list[str] = []

    # Directory tree (top 3 levels)
    parts.append("## Project Structure\n")
    for root, dirs, files in os.walk(project_root):
        depth = str(root).replace(str(project_root), "").count(os.sep)
        if depth >= 3:
            dirs.clear()
            continue
        # Skip hidden dirs and common noise
        dirs[:] = [d for d in sorted(dirs) if not d.startswith(".") and d not in {"node_modules", "__pycache__", "venv", ".venv", "dist", "build"}]
        indent = "  " * depth
        parts.append(f"{indent}{os.path.basename(root)}/")
        for f in sorted(files)[:20]:
            parts.append(f"{indent}  {f}")

    # Package manifests
    for manifest in ["package.json", "pyproject.toml", "Cargo.toml", "go.mod", "Gemfile", "pom.xml"]:
        mp = project_root / manifest
        if mp.exists():
            parts.append(f"\n## {manifest}\n```\n{mp.read_text()[:2000]}\n```")

    # Existing specs summary
    sdir = specs_subdir(project_root)
    if sdir.is_dir():
        spec_dirs = [d for d in sdir.iterdir() if (d / "SPEC.md").exists()]
        if spec_dirs:
            parts.append("\n## Existing Specs")
            for d in sorted(spec_dirs):
                parts.append(f"- {d.name}")

    # User-specified include files
    for p in include_paths:
        fp = project_root / p
        if fp.exists() and fp.is_file():
            content = fp.read_text()[:3000]
            parts.append(f"\n## {p}\n```\n{content}\n```")

    return "\n".join(parts)


def generate_spec(api_key: str, model: str, description: str, context: str) -> str:
    """Call the Claude API to generate a SPEC.md."""
    client = create_client(api_key)
    today = date.today().isoformat()

    message = client.messages.create(
        model=model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Create a spec for: {description}\n\n"
                    f"Today's date: {today}\n\n"
                    f"Project context:\n{context}"
                ),
            }
        ],
    )

    return message.content[0].text
