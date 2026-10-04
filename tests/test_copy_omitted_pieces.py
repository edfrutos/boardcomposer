"""Copy the status-bar omitted-piece count (IDE-0088)."""

from PySide6.QtWidgets import QApplication

from studio.models import StudioPiece, StudioPlacement, StudioProject
from tests.test_placed_status import _window


def test_copy_omitted_pieces_uses_the_status_count(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, "es")
    action = window._actions["copy_omitted_pieces"]
    assert "Ctrl+Alt+Shift+O" in action.shortcut().toString()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    window._copy_omitted_pieces()
    assert clipboard.text() == "keep-me"
    assert window.statusBar().currentMessage() == window._tr(
        "status.nothing_to_copy_omitted_pieces"
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
    assert action.isEnabled()
    calls: list[str] = []
    window._select_and_fit_omitted = calls.append
    action.trigger()
    assert calls == []
    assert clipboard.text() == "1"
    assert window.statusBar().currentMessage() == window._tr(
        "status.omitted_pieces_copied", n="1"
    )

    project.placements.append(StudioPlacement("P2", 20, 20))
    window.update_window_title()
    assert not action.isEnabled()
    clipboard.setText("keep-me")
    window._copy_omitted_pieces()
    assert clipboard.text() == "keep-me"
