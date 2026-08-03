"""Studio UI for structural .bcproj diffs."""

from __future__ import annotations

import json
from pathlib import Path

from boardcomposer.io.bcproj_revisions import snapshot_before_overwrite
from studio.dialogs.bcproj_diff_dialog import BcprojDiffDialog
from studio.i18n import tr
from studio.keyboard_shortcuts import STUDIO_SHORTCUTS
from studio.models import StudioBoard, StudioPiece, StudioProject
from studio.project_serializer import project_to_dict

SAMPLES = Path("data/samples")
BASE = SAMPLES / "multipanel_demo.bcproj"


def test_diff_bcproj_shortcut_registered():
    assert any(
        b.action_key == "diff_bcproj" and b.sequence == "Ctrl+Shift+Y"
        for b in STUDIO_SHORTCUTS
    )
    assert "Ctrl+Shift+Y" in tr("tip.diff_bcproj", "es")
    assert "Ctrl+Shift+Y" in tr("tip.diff_bcproj", "en")


def test_bcproj_diff_dialog_compare_is_primary(qapp):
    del qapp
    dialog = BcprojDiffDialog(language="es")
    assert dialog.compare_button.objectName() == "primaryButton"
    assert dialog.compare_button.minimumHeight() >= 36
    tip = dialog.compare_button.toolTip().lower()
    assert "diff" in tip or "estructural" in tip
    assert dialog.compare_button.statusTip() == dialog.compare_button.toolTip()
    assert dialog.compare_button.property("bcSecondaryMinHeight") == 36
    assert dialog.restore_button.minimumHeight() >= 36
    assert dialog.left_browse_button.minimumHeight() >= 36
    assert "bcproj" in dialog.left_browse_button.toolTip().lower()
    assert dialog.right_browse_button.statusTip() == dialog.left_browse_button.toolTip()


def test_bcproj_diff_dialog_compares_current_vs_file(qapp, tmp_path):
    project = StudioProject(
        project_id="ui-diff",
        name="Open",
        boards=[
            StudioBoard(
                board_id="P1",
                length_mm=1000,
                width_mm=500,
                material="Melamina",
                thickness_mm=19,
                quantity=1,
            )
        ],
        pieces=[
            StudioPiece(
                piece_id="A",
                length_mm=100,
                width_mm=50,
                material="Melamina",
                thickness_mm=19,
            )
        ],
        placements=[],
    )
    right = json.loads(BASE.read_text(encoding="utf-8"))
    right["name"] = "Other revision"
    right_path = tmp_path / "right.bcproj"
    right_path.write_text(json.dumps(right), encoding="utf-8")

    dialog = BcprojDiffDialog(
        language="es",
        current_project=project_to_dict(project),
        current_label="(open)",
    )
    dialog.use_current_left.setChecked(True)
    dialog.use_current_right.setChecked(False)
    dialog.right_path.setText(str(right_path))
    dialog._run_diff()

    text = dialog.result.toPlainText()
    assert "diff:" in text
    assert "name" in text
    assert "changes:" in text


def test_bcproj_diff_dialog_defaults_to_revision_vs_current(qapp, tmp_path):
    path = tmp_path / "live.bcproj"
    saved = {
        "version": 2,
        "project_id": "ui-rev",
        "name": "Live",
        "boards": [],
        "pieces": [],
        "placements": [],
    }
    path.write_text(json.dumps(saved), encoding="utf-8")
    snapshot_before_overwrite(path)

    dirty = StudioProject(
        project_id="ui-rev",
        name="Dirty",
        boards=[],
        pieces=[],
        placements=[],
    )
    dialog = BcprojDiffDialog(
        language="es",
        current_project=project_to_dict(dirty),
        current_label="(open)",
        project_path=str(path),
    )
    assert dialog.use_current_right.isChecked()
    assert dialog.revision_combo.currentIndex() == 1
    dialog._run_diff()
    text = dialog.result.toPlainText()
    assert "diff:" in text
    assert "name" in text


def test_bcproj_diff_dialog_restore_enabled_for_revision(qapp, tmp_path):
    path = tmp_path / "live.bcproj"
    saved = {
        "version": 2,
        "project_id": "ui-rev",
        "name": "Live",
        "boards": [],
        "pieces": [],
        "placements": [],
    }
    path.write_text(json.dumps(saved), encoding="utf-8")
    snapshot = snapshot_before_overwrite(path)
    assert snapshot is not None

    dirty = StudioProject(
        project_id="ui-rev",
        name="Dirty",
        boards=[],
        pieces=[],
        placements=[],
    )
    dialog = BcprojDiffDialog(
        language="es",
        current_project=project_to_dict(dirty),
        current_label="(open)",
        project_path=str(path),
    )
    assert dialog.restore_button.isEnabled()
    assert dialog.selected_revision_path() == snapshot
    assert dialog.restore_path is None

    dialog.revision_combo.setCurrentIndex(0)
    assert not dialog.restore_button.isEnabled()
    assert dialog.selected_revision_path() is None

    dialog.revision_combo.setCurrentIndex(1)
    dialog._request_restore()
    assert dialog.restore_path == snapshot


def test_bcproj_diff_dialog_browse_notifies_path_chosen(qapp, tmp_path, monkeypatch):
    del qapp
    chosen: list[str] = []
    target = tmp_path / "peer.bcproj"
    target.write_text("{}", encoding="utf-8")

    dialog = BcprojDiffDialog(
        language="es",
        on_path_chosen=lambda path: chosen.append(str(path)),
    )
    monkeypatch.setattr(
        "studio.dialogs.bcproj_diff_dialog.QFileDialog.getOpenFileName",
        lambda *args, **kwargs: (str(target), "bcproj"),
    )

    dialog._browse(dialog.right_path)

    assert dialog.right_path.text() == str(target)
    assert chosen == [str(target)]
