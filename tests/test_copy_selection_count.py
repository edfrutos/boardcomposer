"""Copy the status-bar selection count (IDE-0090)."""

from PySide6.QtWidgets import QApplication

from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from tests.test_copy_selection_id import _window


def test_copy_selection_count_uses_the_status_count(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    action = window._actions["copy_selection_count"]
    assert "Ctrl+Alt+Shift+S" in action.shortcut().toString()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    window._copy_selection_count()
    assert clipboard.text() == "keep-me"
    assert window.statusBar().currentMessage() == window._tr(
        "status.nothing_to_copy_selection_count"
    )

    calls: list[str] = []
    window._fit_selection = lambda: calls.append("fit")
    window.workspace.select_piece("A")
    assert action.isEnabled()
    action.trigger()
    assert calls == []
    assert clipboard.text() == "1"
    assert window.statusBar().currentMessage() == window._tr(
        "status.selection_count_copied", n="1"
    )

    project = StudioProject(
        project_id="PRJ-2",
        name="Dos",
        boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
        pieces=[
            StudioPiece("A", 200, 100, "Demo", 19),
            StudioPiece("B", 180, 90, "Demo", 19),
        ],
        placements=[
            StudioPlacement("A", 10, 20, False, 0, "B1", 0, 0),
            StudioPlacement("B", 220, 20, False, 0, "B1", 0, 0),
        ],
    )
    window.services.projects.new_project(project)
    window.workspace.reload_project()
    window.workspace.select_pieces(["A", "B"])
    action.trigger()
    assert calls == []
    assert clipboard.text() == "2"

    window.workspace.clear_piece_selection()
    assert not action.isEnabled()
    clipboard.setText("keep-me")
    window._copy_selection_count()
    assert clipboard.text() == "keep-me"
