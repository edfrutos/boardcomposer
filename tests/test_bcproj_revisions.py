"""Local .bcproj revision ring."""

from __future__ import annotations

import json
from pathlib import Path

from boardcomposer.io.bcproj_revisions import (
    MAX_REVISIONS,
    latest_revision,
    list_revisions,
    revisions_dir,
    snapshot_before_overwrite,
)
from studio.models import StudioBoard, StudioPiece, StudioProject
from studio.project_serializer import project_to_dict, save_project

SAMPLES = Path("data/samples")
BASE = SAMPLES / "multipanel_demo.bcproj"


def test_snapshot_before_overwrite_creates_ring(tmp_path):
    path = tmp_path / "demo.bcproj"
    path.write_text(BASE.read_text(encoding="utf-8"), encoding="utf-8")

    first = snapshot_before_overwrite(path)
    assert first is not None
    assert first.parent == revisions_dir(path)
    assert first.read_text(encoding="utf-8") == path.read_text(encoding="utf-8")

    path.write_text('{"version": 2, "name": "v2"}', encoding="utf-8")
    second = snapshot_before_overwrite(path)
    assert second is not None
    assert second != first
    assert len(list_revisions(path)) == 2
    assert latest_revision(path) == second


def test_snapshot_prunes_to_max(tmp_path):
    path = tmp_path / "demo.bcproj"
    path.write_text("{}", encoding="utf-8")
    for index in range(MAX_REVISIONS + 3):
        path.write_text(json.dumps({"n": index}), encoding="utf-8")
        snapshot_before_overwrite(path)
    assert len(list_revisions(path)) == MAX_REVISIONS


def test_save_project_snapshots_previous(tmp_path):
    path = tmp_path / "proj.bcproj"
    project = StudioProject(
        project_id="r1",
        name="One",
        boards=[
            StudioBoard(
                board_id="B1",
                length_mm=1000,
                width_mm=500,
                material="M",
                thickness_mm=18,
                quantity=1,
            )
        ],
        pieces=[
            StudioPiece(
                piece_id="P1",
                length_mm=100,
                width_mm=50,
                material="M",
                thickness_mm=18,
            )
        ],
        placements=[],
    )
    save_project(project, path)
    assert list_revisions(path) == []

    project.name = "Two"
    snapshot = save_project(project, path)
    revs = list_revisions(path)
    assert len(revs) == 1
    assert snapshot == revs[0]
    assert json.loads(revs[0].read_text(encoding="utf-8"))["name"] == "One"
    assert project_to_dict(project)["name"] == "Two"


def test_export_project_backup_copies_file_and_ring(tmp_path):
    from boardcomposer.io.bcproj_revisions import export_project_backup

    path = tmp_path / "demo.bcproj"
    path.write_text(BASE.read_text(encoding="utf-8"), encoding="utf-8")
    snapshot_before_overwrite(path)
    path.write_text('{"version": 2, "name": "v2"}', encoding="utf-8")
    snapshot_before_overwrite(path)

    dest = tmp_path / "backups"
    folder = export_project_backup(path, dest)
    assert folder.is_dir()
    assert folder.parent == dest
    assert (folder / "demo.bcproj").is_file()
    assert (folder / "demo.bcproj").read_text(encoding="utf-8") == path.read_text(
        encoding="utf-8"
    )
    ring_copy = folder / ".demo.bcproj.revs"
    assert ring_copy.is_dir()
    assert len(list(ring_copy.glob("*.bcproj"))) == 2


def test_export_project_backup_without_ring(tmp_path):
    from boardcomposer.io.bcproj_revisions import export_project_backup

    path = tmp_path / "solo.bcproj"
    path.write_text("{}", encoding="utf-8")
    folder = export_project_backup(path, tmp_path / "out")
    assert (folder / "solo.bcproj").is_file()
    assert not (folder / ".solo.bcproj.revs").exists()
