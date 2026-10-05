"""Copy the status-bar physical board count (IDE-0089)."""

from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
from studio.models import StudioBoard
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_copy_selection_id import _window


def test_copy_physical_boards_uses_the_status_count(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    action = empty._actions["copy_physical_boards"]
    assert "Ctrl+Alt+Shift+N" in action.shortcut().toString()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    empty._copy_physical_boards()
    assert clipboard.text() == "keep-me"
    assert empty.statusBar().currentMessage() == empty._tr(
        "status.nothing_to_copy_physical_boards"
    )

    window = _window(tmp_path)
    action = window._actions["copy_physical_boards"]
    assert action.isEnabled()
    calls: list[str] = []
    window._fit_board = lambda: calls.append("fit")
    action.trigger()
    assert calls == []
    assert clipboard.text() == "1"
    assert window.statusBar().currentMessage() == window._tr(
        "status.physical_boards_copied", n="1"
    )

    project = window.services.projects.current_project
    assert project is not None
    project.boards[0] = StudioBoard("B1", 1000, 500, "Demo", 19, 3)
    project.boards.append(StudioBoard("B2", 800, 400, "Demo", 19, 2))
    window.update_window_title()
    action.trigger()
    assert calls == []
    assert clipboard.text() == "5"
