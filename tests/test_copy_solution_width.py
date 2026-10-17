"""Copy the status-bar solution total width (IDE-0125)."""

from dataclasses import replace

from PySide6.QtWidgets import QApplication

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_inspector_board_utilization import _window


def test_copy_solution_width_uses_the_formatted_width(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    action = empty._actions["copy_solution_width"]
    assert "Ctrl+Alt+Shift+X" in action.shortcut().toString()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    empty._copy_solution_width()
    assert clipboard.text() == "keep-me"
    assert empty.statusBar().currentMessage() == empty._tr(
        "status.nothing_to_copy_solution_width"
    )

    window = _window(tmp_path)
    action = window._actions["copy_solution_width"]
    assert not action.isEnabled()
    calls: list[str] = []
    window._step_layout_solution = lambda _delta: calls.append("step")
    window._copy_solution_width()
    assert calls == []
    assert clipboard.text() == "keep-me"

    window.services.layout.solutions = [
        AssemblySolution(placements=[]),
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 400, 300)]),
    ]
    window._select_layout_solution(0)
    zoom = window.workspace.zoom
    assert window._solution_width_label.text() == "anc. 0 mm"
    assert action.isEnabled()
    action.trigger()
    assert calls == []
    assert clipboard.text() == "0 mm"
    assert "anc." not in clipboard.text()
    assert window.statusBar().currentMessage() == window._tr(
        "status.solution_width_copied", length="0 mm"
    )
    assert window.services.layout.selected_solution_index == 0
    assert window.workspace.zoom == zoom

    window._select_layout_solution(1)
    action.trigger()
    assert calls == []
    assert clipboard.text() == "300 mm"
    assert window.services.layout.selected_solution_index == 1

    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm")
    )
    window._retranslate_ui()
    assert window._solution_width_label.text() == "anc. 30 cm"
    action.trigger()
    assert clipboard.text() == "30 cm"

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert not action.isEnabled()
    clipboard.setText("keep-me")
    window._copy_solution_width()
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
    assert window._solution_width_label.text() == "wid. 300 mm"
    assert action.isEnabled()
    action.trigger()
    assert clipboard.text() == "300 mm"
    assert "wid." not in clipboard.text()
    assert calls == []
