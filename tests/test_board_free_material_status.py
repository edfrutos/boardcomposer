"""Status bar shows free material of the focused board (IDE-0084)."""

from dataclasses import replace

from PySide6.QtCore import Qt

from boardcomposer.domain import AssemblySolution, BoardPlacement, PanelReference
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_inspector_board_utilization import _window


def test_board_free_material_hidden_without_focus(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    label = window._board_free_material_label
    assert label.objectName() == "statusBoardFreeMaterial"
    assert label.text() == ""
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor

    window = _window(tmp_path, placed=True)
    label = window._board_free_material_label
    assert label.isHidden()
    window.workspace.focus_board("B2")
    assert label.isHidden()
    window.workspace.clear_board_focus()
    assert label.isHidden()


def test_board_free_material_follows_focus_and_layout(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, placed=True)
    label = window._board_free_material_label
    window.workspace.focus_board("B1")
    assert label.text() == "libre 76.0%"
    assert not label.isHidden()
    assert "material libre" in label.toolTip().casefold()
    assert "clic" not in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    window._show_board_inspector("B1")
    assert "Material libre: 76.0%" in window.inspector.toPlainText()

    window.workspace.select_piece("A")
    assert label.isHidden()

    window.services.layout.solutions = [
        AssemblySolution(
            placements=[
                BoardPlacement(
                    "A",
                    0,
                    0,
                    400,
                    300,
                    panel_reference=PanelReference(0, 0),
                )
            ]
        )
    ]
    window.services.layout.selected_solution_index = 0
    window.workspace.focus_board("B2")
    window._reload_explorer()
    assert label.isHidden()
    window.workspace.focus_board("B1")
    assert label.text() == "libre 76.0%"

    window.services.preferences.update(
        replace(window.services.preferences.current, language="en")
    )
    window._retranslate_ui()
    assert label.text() == "free 76.0%"
    assert "free" in label.toolTip().casefold()
    assert "click" not in label.toolTip().casefold()
