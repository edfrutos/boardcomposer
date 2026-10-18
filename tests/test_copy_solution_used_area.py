"""Copy the status-bar solution used area (IDE-0128)."""

from dataclasses import replace

from PySide6.QtWidgets import QApplication

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_inspector_board_utilization import _window


def test_copy_solution_used_area_uses_the_formatted_area(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    action = empty._actions["copy_solution_used_area"]
    assert "Ctrl+Alt+Shift+A" in action.shortcut().toString()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    empty._copy_solution_used_area()
    assert clipboard.text() == "keep-me"
    assert empty.statusBar().currentMessage() == empty._tr(
        "status.nothing_to_copy_solution_used_area"
    )

    window = _window(tmp_path)
    action = window._actions["copy_solution_used_area"]
    assert not action.isEnabled()
    calls: list[str] = []
    window._step_layout_solution = lambda _delta: calls.append("step")
    window._copy_solution_used_area()
    assert calls == []
    assert clipboard.text() == "keep-me"

    window.services.layout.solutions = [
        AssemblySolution(placements=[]),
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 200, 100)]),
    ]
    window._select_layout_solution(0)
    zoom = window.workspace.zoom
    assert window._solution_used_area_label.text() == "ár. 0 mm²"
    assert action.isEnabled()
    action.trigger()
    assert calls == []
    assert clipboard.text() == "0 mm²"
    assert "ár." not in clipboard.text()
    assert window.statusBar().currentMessage() == window._tr(
        "status.solution_used_area_copied", area="0 mm²"
    )
    assert window.services.layout.selected_solution_index == 0
    assert window.workspace.zoom == zoom

    window._select_layout_solution(1)
    action.trigger()
    assert calls == []
    assert clipboard.text() == "20000 mm²"
    assert window.services.layout.selected_solution_index == 1

    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm")
    )
    window._retranslate_ui()
    assert window._solution_used_area_label.text() == "ár. 200 cm²"
    action.trigger()
    assert clipboard.text() == "200 cm²"

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert not action.isEnabled()
    clipboard.setText("keep-me")
    window._copy_solution_used_area()
    assert calls == []
    assert clipboard.text() == "keep-me"

    window.services.layout.solutions = [
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 200, 100)])
    ]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    window.services.preferences.update(
        replace(window.services.preferences.current, language="en", units="mm")
    )
    window._retranslate_ui()
    assert window._solution_used_area_label.text() == "area 20000 mm²"
    assert action.isEnabled()
    action.trigger()
    assert clipboard.text() == "20000 mm²"
    assert "area" not in clipboard.text()
    assert calls == []
