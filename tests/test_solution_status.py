"""Status bar shows the selected solution index (IDE-0095)."""

from PySide6.QtCore import Qt

from boardcomposer.domain import AssemblySolution
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_inspector_board_utilization import _window


def test_solution_status_follows_the_selected_solution(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    empty_label = empty._solution_label
    assert empty_label.objectName() == "statusSolution"
    assert empty_label.isHidden()
    assert empty_label.cursor().shape() == Qt.CursorShape.ArrowCursor

    window = _window(tmp_path)
    label = window._solution_label
    assert label.text() == ""
    assert label.isHidden()
    assert label.toolTip() == ""
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor

    window.services.layout.solutions = [
        AssemblySolution(placements=[]),
        AssemblySolution(placements=[]),
    ]
    window.services.layout.selected_solution_index = 0
    window._select_layout_solution(0)
    assert label.text() == "1/2 sol."
    assert not label.isHidden()
    assert "solución" in label.toolTip().casefold()
    assert "1" in label.toolTip()
    assert "clic" in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.PointingHandCursor

    window._select_layout_solution(1)
    assert label.text() == "2/2 sol."

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor

    window.services.layout.solutions = []
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    assert label.isHidden()

    window.services.layout.solutions = [AssemblySolution(placements=[])]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    window.services.preferences.update(
        window.services.preferences.current.__class__(language="en")
    )
    window._retranslate_ui()
    assert label.text() == "1/1 sol."
    assert "solution" in label.toolTip().casefold()
    assert "click" in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.PointingHandCursor
