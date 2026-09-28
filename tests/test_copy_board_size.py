"""Copy one board sheet's length × width in Preferences units (IDE-0068)."""

from dataclasses import replace

from PySide6.QtWidgets import QApplication

from studio.models import StudioBoard
from tests.test_copy_selection_id import _window


def test_copy_board_size_uses_display_units_not_quantity(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    action = window._actions["copy_board_size"]
    assert "Ctrl+Alt+Shift+B" in action.shortcut().toString()
    assert not action.isEnabled()

    project = window.services.projects.current_project
    assert project is not None
    project.boards[0] = StudioBoard("B1", 1000, 500, "Demo", 19, 3)
    window.workspace.focus_board("B1")
    assert action.isEnabled()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.clear()
    action.trigger()
    assert clipboard.text() == "1000 x 500 mm"
    assert window.statusBar().currentMessage() == window._tr(
        "status.board_size_copied", size="1000 x 500 mm"
    )

    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm")
    )
    action.trigger()
    assert clipboard.text() == "100 x 50 cm"


def test_copy_board_size_rejects_a_piece_and_keeps_clipboard(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.explorer.setCurrentItem(None)
    window.workspace.select_piece("A")
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not window._actions["copy_board_size"].isEnabled()
    window._copy_board_size()
    assert clipboard.text() == "keep-me"
    assert window.statusBar().currentMessage() == window._tr(
        "status.nothing_to_copy_board_size"
    )


def test_copy_board_size_from_explorer_context(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.clear()
    window._run_explorer_context_action("copy_board_size", "board:B1")
    assert clipboard.text() == "1000 x 500 mm"
