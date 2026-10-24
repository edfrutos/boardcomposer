"""Copy the status-bar solution board utilization ratio (IDE-0146)."""

from PySide6.QtWidgets import QApplication

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_inspector_board_utilization import _window


def test_copy_solution_board_utilization_uses_the_percentage(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    action = empty._actions["copy_solution_board_utilization"]
    assert "Ctrl+Alt+Shift+5" in action.shortcut().toString()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    empty._copy_solution_board_utilization()
    assert clipboard.text() == "keep-me"
    assert empty.statusBar().currentMessage() == empty._tr(
        "status.nothing_to_copy_solution_board_utilization"
    )

    window = _window(tmp_path)
    action = window._actions["copy_solution_board_utilization"]
    assert not action.isEnabled()
    calls: list[str] = []
    window._step_layout_solution = lambda _delta: calls.append("step")
    window._copy_solution_board_utilization()
    assert calls == []
    assert clipboard.text() == "keep-me"

    window.services.layout.solutions = [
        AssemblySolution(placements=[]),
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 400, 300)]),
    ]
    window._select_layout_solution(0)
    zoom = window.workspace.zoom
    assert window._solution_board_utilization_label.text() == "aprv. 0.0%"
    assert action.isEnabled()
    action.trigger()
    assert calls == []
    assert clipboard.text() == "0.0%"
    assert "aprv." not in clipboard.text()
    assert window.statusBar().currentMessage() == window._tr(
        "status.solution_board_utilization_copied", value="0.0%"
    )
    assert window.services.layout.selected_solution_index == 0
    assert window.workspace.zoom == zoom

    window._select_layout_solution(1)
    assert window._solution_board_utilization_label.text() == "aprv. 24.0%"
    assert window._solution_board_waste_label.text() == "sbr. 76.0%"
    action.trigger()
    assert calls == []
    assert clipboard.text() == "24.0%"
    assert window.services.layout.selected_solution_index == 1

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert not action.isEnabled()
    clipboard.setText("keep-me")
    window._copy_solution_board_utilization()
    assert calls == []
    assert clipboard.text() == "keep-me"

    window.services.layout.solutions = [
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 400, 300)])
    ]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    window.services.preferences.update(
        window.services.preferences.current.__class__(language="en")
    )
    window._retranslate_ui()
    assert window._solution_board_utilization_label.text() == "util. 24.0%"
    assert action.isEnabled()
    action.trigger()
    assert clipboard.text() == "24.0%"
    assert "util." not in clipboard.text()
    assert calls == []
