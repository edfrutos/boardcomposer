"""Status bar shows the focused board thickness (IDE-0073)."""

from dataclasses import replace

from PySide6.QtCore import Qt

from studio.main_window import MainWindow
from studio.models import StudioBoard
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_copy_selection_id import _window


def test_board_thickness_hidden_without_project(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    assert window._board_thickness_label.text() == ""
    assert window._board_thickness_label.isHidden()


def test_board_thickness_follows_focus_units_and_language(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    label = window._board_thickness_label
    assert label.text() == "esp. 19 mm"
    assert not label.isHidden()
    assert "espesor" in label.toolTip().casefold()
    assert "clic" in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.PointingHandCursor

    window.workspace.select_piece("A")
    assert label.text() == "esp. 19 mm"

    project = window.services.projects.current_project
    assert project is not None
    project.boards.append(StudioBoard("B2", 800, 400, "Demo", 16, 1))
    window.workspace.reload_project()
    window.update_window_title()
    assert label.isHidden()

    window.workspace.focus_board("B2")
    assert label.text() == "esp. 16 mm"
    window.workspace.clear_board_focus()
    assert label.isHidden()

    window.workspace.focus_board("B1")
    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm")
    )
    window._retranslate_ui()
    assert label.text() == "esp. 1.9 cm"

    window.services.preferences.update(
        replace(window.services.preferences.current, language="en", units="mm")
    )
    window._retranslate_ui()
    assert label.text() == "thk. 19 mm"
    assert "thickness" in label.toolTip().casefold()
