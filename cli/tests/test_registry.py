"""Tests for core/registry.py."""

from pathlib import Path

from specsmith.core.registry import rebuild_registry


def test_rebuild_registry(tmp_path: Path):
    specs_dir = tmp_path / ".specs" / "specs" / "my-spec"
    specs_dir.mkdir(parents=True)
    (specs_dir / "SPEC.md").write_text(
        "---\nid: my-spec\ntitle: My Spec\nstatus: active\npriority: high\nupdated: 2026-01-01\n---\n# My Spec\n"
    )
    registry = tmp_path / ".specs" / "registry.md"
    registry.write_text("")

    rebuild_registry(tmp_path)

    content = registry.read_text()
    assert "my-spec" in content
    assert "My Spec" in content
    assert "active" in content
    assert "high" in content


def test_rebuild_registry_empty(tmp_path: Path):
    (tmp_path / ".specs" / "specs").mkdir(parents=True)
    registry = tmp_path / ".specs" / "registry.md"
    registry.write_text("")

    rebuild_registry(tmp_path)

    content = registry.read_text()
    assert "Spec Registry" in content
