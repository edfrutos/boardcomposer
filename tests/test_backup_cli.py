"""Tests for boardcomposer-backup CLI (DT-0006 option D)."""

from pathlib import Path

from boardcomposer.backup_cli import main
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
