"""Copy the status-bar placed/total count (IDE-0087)."""

from PySide6.QtWidgets import QApplication

from studio.models import StudioPiece, StudioPlacement, StudioProject
from tests.test_placed_status import _window


def test_copy_placed_pieces_uses_the_status_count(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, "es")
    action = window._actions["copy_placed_pieces"]
    assert "Ctrl+Alt+Shift+P" in action.shortcut().toString()
    assert action.isEnabled()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    calls: list[str] = []
    window._fit_placed = calls.append
    action.trigger()
    assert calls == []
    assert clipboard.text() == "0/0"
    assert window.statusBar().currentMessage() == window._tr(
        "status.placed_pieces_copied", value="0/0"
    )

    project = StudioProject(
        project_id="PRJ-1",
        name="Taller",
        pieces=[
            StudioPiece("P1", 400, 300),
            StudioPiece("P2", 200, 100),
        ],
        placements=[
            StudioPlacement("P1", 0, 0),
            StudioPlacement("AJENA", 10, 10),
        ],
    )
    window.services.projects.open_project(project, None)
    window.update_window_title()
    action.trigger()
    assert calls == []
    assert clipboard.text() == "1/2"
    assert window.statusBar().currentMessage() == window._tr(
        "status.placed_pieces_copied", value="1/2"
    )
