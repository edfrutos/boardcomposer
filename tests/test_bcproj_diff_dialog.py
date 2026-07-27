"""Studio UI for structural .bcproj diffs."""

from __future__ import annotations

import json
from pathlib import Path

from studio.dialogs.bcproj_diff_dialog import BcprojDiffDialog
from studio.i18n import tr
from studio.keyboard_shortcuts import STUDIO_SHORTCUTS
from studio.project_serializer import project_to_dict
from studio.models import StudioBoard, StudioPiece, StudioProject

SAMPLES = Path("data/samples")
BASE = SAMPLES / "multipanel_demo.bcproj"


def test_diff_bcproj_shortcut_registered():
    assert any(
        b.action_key == "diff_bcproj" and b.sequence == "Ctrl+Shift+Y"
        for b in STUDIO_SHORTCUTS
    )
    assert "Ctrl+Shift+Y" in tr("tip.diff_bcproj", "es")
    assert "Ctrl+Shift+Y" in tr("tip.diff_bcproj", "en")


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
    dialog.use_current.setChecked(True)
    dialog.right_path.setText(str(right_path))
    dialog._run_diff()

    text = dialog.result.toPlainText()
    assert "diff:" in text
    assert "name" in text
    assert "changes:" in text
