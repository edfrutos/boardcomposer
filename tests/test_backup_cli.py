"""Tests for boardcomposer-backup CLI (DT-0006 option D)."""

from pathlib import Path

from boardcomposer.backup_cli import main, resolve_project_path
from boardcomposer.io.bcproj_revisions import snapshot_before_overwrite


def test_backup_cli_writes_stamped_folder(tmp_path, capsys):
    project = tmp_path / "job.bcproj"
    project.write_text('{"name": "job"}', encoding="utf-8")
    snapshot_before_overwrite(project)

    dest = tmp_path / "remote"
    code = main([str(project), "--dest", str(dest)])
    assert code == 0
    out = capsys.readouterr().out.strip()
    folder = Path(out)
    assert folder.is_dir()
    assert (folder / "job.bcproj").is_file()
    assert (folder / ".job.bcproj.revs").is_dir()


def test_backup_cli_missing_project(tmp_path):
    code = main([str(tmp_path / "missing.bcproj"), "--dest", str(tmp_path / "out")])
    assert code == 2


def test_resolve_prefers_sibling_bcproj(tmp_path, capsys):
    bcproj = tmp_path / "caja.bcproj"
    bcproj.write_text('{"name": "caja"}', encoding="utf-8")
    legacy = tmp_path / "caja.bcstudio.json"
    legacy.write_text("{}", encoding="utf-8")

    resolved = resolve_project_path(legacy)
    assert resolved == bcproj
    err = capsys.readouterr().err.lower()
    assert "sibling" in err or "bcproj" in err


def test_backup_cli_uses_sibling_bcproj_ring(tmp_path, capsys):
    bcproj = tmp_path / "caja.bcproj"
    bcproj.write_text('{"name": "caja"}', encoding="utf-8")
    snapshot_before_overwrite(bcproj)
    legacy = tmp_path / "caja.bcstudio.json"
    legacy.write_text("{}", encoding="utf-8")

    dest = tmp_path / "remote"
    assert main([str(legacy), "--dest", str(dest)]) == 0
    captured = capsys.readouterr()
    folder = Path(captured.out.strip())
    assert (folder / "caja.bcproj").is_file()
    assert (folder / ".caja.bcproj.revs").is_dir()


def test_backup_cli_force_keeps_non_bcproj(tmp_path, capsys):
    legacy = tmp_path / "solo.bcstudio.json"
    legacy.write_text("{}", encoding="utf-8")
    dest = tmp_path / "out"
    assert main([str(legacy), "--dest", str(dest), "--force"]) == 0
    folder = Path(capsys.readouterr().out.strip())
    assert (folder / "solo.bcstudio.json").is_file()
