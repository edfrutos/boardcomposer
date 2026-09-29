"""Status bar shows the same board's material (IDE-0076)."""

from dataclasses import replace

from PySide6.QtCore import Qt

from studio.main_window import MainWindow
from studio.models import StudioBoard
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_copy_selection_id import _window


def test_board_material_hidden_without_project(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    label = window._board_material_label
    assert label.text() == ""
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor


def test_board_material_follows_the_thickness_board(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    label = window._board_material_label
    thickness = window._board_thickness_label
    assert label.text() == "mat. Demo"
    assert not label.isHidden()
    assert "material" in label.toolTip().casefold()
    assert "clic" not in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert thickness.text() == "esp. 19 mm"

    project = window.services.projects.current_project
    assert project is not None
    project.boards[0] = replace(project.boards[0], quantity=3)
    window.workspace.reload_project()
    window.update_window_title()
    assert label.text() == "mat. Demo"

    window.workspace.select_piece("A")
    assert label.text() == "mat. Demo"

    project.boards.append(StudioBoard("B2", 800, 400, "Roble", 16, 1))
    window.workspace.reload_project()
    window.update_window_title()
    assert label.isHidden()
    assert thickness.isHidden()

    window.workspace.focus_board("B2")
    assert label.text() == "mat. Roble"
    assert thickness.text() == "esp. 16 mm"
    window.workspace.clear_board_focus()
    assert label.isHidden()

    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm", language="en")
    )
    window.workspace.focus_board("B1")
    window._retranslate_ui()
    assert label.text() == "mat. Demo"
    assert "material" in label.toolTip().casefold()
    assert "click" not in label.toolTip().casefold()
    assert thickness.text() == "thk. 1.9 cm"


def test_board_material_hides_when_blank(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    project = window.services.projects.current_project
    assert project is not None
    project.boards[0] = replace(project.boards[0], material="   ")
    window.workspace.reload_project()
    window.update_window_title()
    label = window._board_material_label
    assert label.isHidden()
    assert label.text() == ""
    assert window._board_thickness_label.text() == "esp. 19 mm"
