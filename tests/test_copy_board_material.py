"""Copy the status-bar board material (IDE-0077)."""

from dataclasses import replace

from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
from studio.models import StudioBoard
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_copy_selection_id import _window


def test_copy_board_material_uses_the_status_board(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    action = window._actions["copy_board_material"]
    assert "Ctrl+Alt+Shift+M" in action.shortcut().toString()
    assert "Ctrl+Shift+M" in window._actions["save_as_template"].shortcut().toString()
    assert action.isEnabled()

    project = window.services.projects.current_project
    assert project is not None
    project.boards[0] = replace(project.boards[0], quantity=3, material="  Roble  ")
    window.update_window_title()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.clear()
    action.trigger()
    assert clipboard.text() == "Roble"
    assert window.statusBar().currentMessage() == window._tr(
        "status.board_material_copied", material="Roble"
    )
    assert window._board_material_label.text() == "mat. Roble"

    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm", language="en")
    )
    window._retranslate_ui()
    action.trigger()
    assert clipboard.text() == "Roble"
    assert window.statusBar().currentMessage() == "Board material copied: Roble"

    project.boards.append(StudioBoard("B2", 800, 400, "Haya", 16, 1))
    window.workspace.reload_project()
    window.update_window_title()
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    assert window._board_material_label.isHidden()
    window._copy_board_material()
    assert clipboard.text() == "keep-me"

    window.workspace.focus_board("B2")
    assert action.isEnabled()
    action.trigger()
    assert clipboard.text() == "Haya"

    project.boards[1] = replace(project.boards[1], material="   ")
    window.workspace.reload_project()
    window.workspace.focus_board("B2")
    window.update_window_title()
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    assert window._board_thickness_label.text() == "thk. 1.6 cm"
    window._copy_board_material()
    assert clipboard.text() == "keep-me"


def test_copy_board_material_without_project_keeps_clipboard(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    action = window._actions["copy_board_material"]
    assert not action.isEnabled()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    window._copy_board_material()
    assert clipboard.text() == "keep-me"
    assert window.statusBar().currentMessage() == window._tr(
        "status.nothing_to_copy_board_material"
    )
