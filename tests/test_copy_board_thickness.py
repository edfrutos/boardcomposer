"""Copy the status-bar board thickness (IDE-0075)."""

from dataclasses import replace

from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
from studio.models import StudioBoard
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_copy_selection_id import _window


def test_copy_board_thickness_uses_the_status_board(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    action = window._actions["copy_board_thickness"]
    assert "Ctrl+Alt+Shift+T" in action.shortcut().toString()
    assert action.isEnabled()

    project = window.services.projects.current_project
    assert project is not None
    project.boards[0] = StudioBoard("B1", 1000, 500, "Demo", 19, 3)
    window.update_window_title()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.clear()
    action.trigger()
    assert clipboard.text() == "19 mm"
    assert window.statusBar().currentMessage() == window._tr(
        "status.board_thickness_copied", length="19 mm"
    )

    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm")
    )
    action.trigger()
    assert clipboard.text() == "1.9 cm"

    project.boards.append(StudioBoard("B2", 800, 400, "Demo", 16, 1))
    window.workspace.reload_project()
    window.update_window_title()
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    window._copy_board_thickness()
    assert clipboard.text() == "keep-me"

    window.workspace.focus_board("B2")
    assert action.isEnabled()
    action.trigger()
    assert clipboard.text() == "1.6 cm"


def test_copy_board_thickness_without_project_keeps_clipboard(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    action = window._actions["copy_board_thickness"]
    assert not action.isEnabled()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    window._copy_board_thickness()
    assert clipboard.text() == "keep-me"
    assert window.statusBar().currentMessage() == window._tr(
        "status.nothing_to_copy_board_thickness"
    )
