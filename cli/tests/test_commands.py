"""CLI integration tests using typer.testing.CliRunner."""

from pathlib import Path

from typer.testing import CliRunner

from specsmith.cli import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "specsmith" in result.output


def test_init(tmp_path: Path):
    result = runner.invoke(app, ["init", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert (tmp_path / ".specs").is_dir()
    assert (tmp_path / ".specs" / "specs").is_dir()
    assert (tmp_path / ".specs" / "active").exists()
    assert (tmp_path / ".specs" / "registry.md").exists()


def test_init_idempotent(tmp_path: Path):
    runner.invoke(app, ["init", "--path", str(tmp_path)])
    result = runner.invoke(app, ["init", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert "already exists" in result.output


def test_new(tmp_path: Path):
    runner.invoke(app, ["init", "--path", str(tmp_path)])
    result = runner.invoke(app, ["new", "My Feature", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert (tmp_path / ".specs" / "specs" / "my-feature" / "SPEC.md").exists()
    assert (tmp_path / ".specs" / "active").read_text().strip() == "my-feature"


def test_new_duplicate(tmp_path: Path):
    runner.invoke(app, ["init", "--path", str(tmp_path)])
    runner.invoke(app, ["new", "My Feature", "--path", str(tmp_path)])
    result = runner.invoke(app, ["new", "My Feature", "--path", str(tmp_path)])
    assert result.exit_code == 1


def test_status(tmp_path: Path):
    runner.invoke(app, ["init", "--path", str(tmp_path)])
    runner.invoke(app, ["new", "My Feature", "--path", str(tmp_path)])
    result = runner.invoke(app, ["status", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert "My Feature" in result.output


def test_list(tmp_path: Path):
    runner.invoke(app, ["init", "--path", str(tmp_path)])
    runner.invoke(app, ["new", "Feature A", "--path", str(tmp_path)])
    runner.invoke(app, ["new", "Feature B", "--path", str(tmp_path)])
    result = runner.invoke(app, ["list", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert "feature-a" in result.output
    assert "feature-b" in result.output


def test_pause_resume(tmp_path: Path):
    runner.invoke(app, ["init", "--path", str(tmp_path)])
    runner.invoke(app, ["new", "My Feature", "--path", str(tmp_path)])

    result = runner.invoke(app, ["pause", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert "Paused" in result.output
    assert (tmp_path / ".specs" / "active").read_text().strip() == ""

    result = runner.invoke(app, ["resume", "my-feature", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert "Resumed" in result.output
    assert (tmp_path / ".specs" / "active").read_text().strip() == "my-feature"


def test_switch(tmp_path: Path):
    runner.invoke(app, ["init", "--path", str(tmp_path)])
    runner.invoke(app, ["new", "Feature A", "--path", str(tmp_path)])
    runner.invoke(app, ["new", "Feature B", "--path", str(tmp_path)])

    result = runner.invoke(app, ["switch", "feature-b", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert (tmp_path / ".specs" / "active").read_text().strip() == "feature-b"


def test_complete_force(tmp_path: Path):
    runner.invoke(app, ["init", "--path", str(tmp_path)])
    runner.invoke(app, ["new", "My Feature", "--path", str(tmp_path)])

    # Without force, should fail (tasks unchecked)
    result = runner.invoke(app, ["complete", "--path", str(tmp_path)])
    assert result.exit_code == 1

    # With force, should succeed
    result = runner.invoke(app, ["complete", "--force", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert "Completed" in result.output


def test_archive(tmp_path: Path):
    runner.invoke(app, ["init", "--path", str(tmp_path)])
    runner.invoke(app, ["new", "My Feature", "--path", str(tmp_path)])
    result = runner.invoke(app, ["archive", "my-feature", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert "Archived" in result.output


def test_setup_dry_run(tmp_path: Path):
    result = runner.invoke(app, ["setup", "cursor", "--dry-run", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert "Spec Management" in result.output


def test_setup_creates_file(tmp_path: Path):
    result = runner.invoke(app, ["setup", "cursor", "--path", str(tmp_path)])
    assert result.exit_code == 0
    config = tmp_path / ".cursor" / "rules"
    assert config.exists()
    assert "Spec Management" in config.read_text()


def test_setup_idempotent(tmp_path: Path):
    runner.invoke(app, ["setup", "cursor", "--path", str(tmp_path)])
    result = runner.invoke(app, ["setup", "cursor", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert "already configured" in result.output


def test_setup_unknown_tool(tmp_path: Path):
    result = runner.invoke(app, ["setup", "unknown-tool", "--path", str(tmp_path)])
    assert result.exit_code == 1


def test_setup_claude_code(tmp_path: Path):
    result = runner.invoke(app, ["setup", "claude-code", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert "plugin" in result.output
