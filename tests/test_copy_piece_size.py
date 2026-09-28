"""Copy one piece's length × width in Preferences units (IDE-0064)."""

from dataclasses import replace

from PySide6.QtWidgets import QApplication

from studio.models import StudioPiece, StudioPlacement
from tests.test_copy_selection_id import _window


def test_copy_piece_size_uses_display_units(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    action = window._actions["copy_piece_size"]
    assert "Ctrl+Alt+Shift+D" in action.shortcut().toString()
    assert not action.isEnabled()

    window.workspace.select_piece("A")
    assert action.isEnabled()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.clear()
    action.trigger()
    assert clipboard.text() == "200 x 100 mm"
    assert window.statusBar().currentMessage() == window._tr(
        "status.piece_size_copied", size="200 x 100 mm"
    )

    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm")
    )
    action.trigger()
    assert clipboard.text() == "20 x 10 cm"


def test_copy_piece_size_rejects_many_and_keeps_clipboard(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    project = window.services.projects.current_project
    assert project is not None
    project.pieces.append(StudioPiece("B", 180, 90, "Demo", 19))
    project.placements.append(StudioPlacement("B", 220, 20, False, 0, "B1", 0, 0))
    window.workspace.reload_project()
    window.explorer.setCurrentItem(None)
    window.workspace.select_pieces(["A", "B"])
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not window._actions["copy_piece_size"].isEnabled()
    window._copy_piece_size()
    assert clipboard.text() == "keep-me"
    assert window.statusBar().currentMessage() == window._tr(
        "status.nothing_to_copy_piece_size"
    )
