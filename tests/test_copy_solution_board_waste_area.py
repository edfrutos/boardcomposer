"""Copy the status-bar solution unused board area (IDE-0140)."""

from dataclasses import replace

from PySide6.QtWidgets import QApplication

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_inspector_board_utilization import _window


def test_copy_solution_board_waste_area_uses_the_formatted_area(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    action = empty._actions["copy_solution_board_waste_area"]
    assert "Ctrl+Alt+Shift+3" in action.shortcut().toString()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    empty._copy_solution_board_waste_area()
    assert clipboard.text() == "keep-me"
    assert empty.statusBar().currentMessage() == empty._tr(
        "status.nothing_to_copy_solution_board_waste_area"
    )

    window = _window(tmp_path)
    action = window._actions["copy_solution_board_waste_area"]
    assert not action.isEnabled()
    calls: list[str] = []
    window._step_layout_solution = lambda _delta: calls.append("step")
    window._copy_solution_board_waste_area()
    assert calls == []
    assert clipboard.text() == "keep-me"

    window.services.layout.solutions = [
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 1000, 500)]),
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 400, 300)]),
    ]
    window._select_layout_solution(0)
    zoom = window.workspace.zoom
    assert window._solution_board_waste_area_label.text() == "sbrár. 0 mm²"
    assert action.isEnabled()
    action.trigger()
    assert calls == []
    assert clipboard.text() == "0 mm²"
    assert "sbrár." not in clipboard.text()
    assert window.statusBar().currentMessage() == window._tr(
        "status.solution_board_waste_area_copied", area="0 mm²"
    )
    assert window.services.layout.selected_solution_index == 0
    assert window.workspace.zoom == zoom

    window._select_layout_solution(1)
    assert window._solution_board_waste_area_label.text() == "sbrár. 380000 mm²"
    assert window._solution_board_waste_label.text() == "sbr. 76.0%"
    action.trigger()
    assert calls == []
    assert clipboard.text() == "380000 mm²"
    assert window.services.layout.selected_solution_index == 1

    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm")
    )
    window._retranslate_ui()
    assert window._solution_board_waste_area_label.text() == "sbrár. 3800 cm²"
    action.trigger()
    assert clipboard.text() == "3800 cm²"

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert not action.isEnabled()
    clipboard.setText("keep-me")
    window._copy_solution_board_waste_area()
    assert calls == []
    assert clipboard.text() == "keep-me"

    window.services.layout.solutions = [
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 400, 300)])
    ]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    window.services.preferences.update(
        replace(window.services.preferences.current, language="en", units="mm")
    )
    window._retranslate_ui()
    assert window._solution_board_waste_area_label.text() == "remar. 380000 mm²"
    assert action.isEnabled()
    action.trigger()
    assert clipboard.text() == "380000 mm²"
    assert "remar." not in clipboard.text()
    assert calls == []
