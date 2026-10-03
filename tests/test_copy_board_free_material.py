"""Copy the status-bar free board material (IDE-0085)."""

from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_inspector_board_utilization import _window


def test_copy_board_free_material_uses_the_focused_board(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, placed=True)
    action = window._actions["copy_board_free_material"]
    assert "Ctrl+Alt+Shift+F" in action.shortcut().toString()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    window._copy_board_free_material()
    assert clipboard.text() == "keep-me"

    window.workspace.focus_board("B1")
    assert action.isEnabled()
    calls: list[str] = []
    window.select_explorer_board = calls.append
    action.trigger()
    assert calls == []
    assert clipboard.text() == "76.0%"
    assert window.statusBar().currentMessage() == window._tr(
        "status.board_free_material_copied", value="76.0%"
    )

    window.workspace.focus_board("B2")
    assert not action.isEnabled()
    clipboard.setText("keep-me")
    window._copy_board_free_material()
    assert clipboard.text() == "keep-me"
    assert window.statusBar().currentMessage() == window._tr(
        "status.nothing_to_copy_board_free_material"
    )


def test_copy_board_free_material_without_project_keeps_clipboard(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    action = window._actions["copy_board_free_material"]
    assert not action.isEnabled()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    window._copy_board_free_material()
    assert clipboard.text() == "keep-me"
    assert window.statusBar().currentMessage() == window._tr(
        "status.nothing_to_copy_board_free_material"
    )
