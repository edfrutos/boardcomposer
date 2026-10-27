"""Copy the status-bar solution bounding utilization (IDE-0161)."""

from PySide6.QtWidgets import QApplication

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_inspector_board_utilization import _window


def test_copy_solution_bounding_utilization_uses_the_percentage(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    action = empty._actions["copy_solution_bounding_utilization"]
    assert "Ctrl+Alt+Shift+0" in action.shortcut().toString()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    empty._copy_solution_bounding_utilization()
    assert clipboard.text() == "keep-me"
    assert empty.statusBar().currentMessage() == empty._tr(
        "status.nothing_to_copy_solution_bounding_utilization"
    )

    window = _window(tmp_path)
    action = window._actions["copy_solution_bounding_utilization"]
    assert not action.isEnabled()
    calls: list[str] = []
    window._step_layout_solution = lambda _delta: calls.append("step")
    window._copy_solution_bounding_utilization()
    assert calls == []
    assert clipboard.text() == "keep-me"

    gapped = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 200, 100),
            BoardPlacement("B", 200, 100, 100, 100),
        ]
    )
    window.services.layout.solutions = [
        AssemblySolution(placements=[]),
        gapped,
    ]
    window._select_layout_solution(0)
    zoom = window.workspace.zoom
    assert window._solution_bounding_utilization_label.text() == "env% 0.0%"
    assert action.isEnabled()
    action.trigger()
    assert calls == []
    assert clipboard.text() == "0.0%"
    assert "env" not in clipboard.text()
    assert window.statusBar().currentMessage() == window._tr(
        "status.solution_bounding_utilization_copied", value="0.0%"
    )
    assert window.services.layout.selected_solution_index == 0
    assert window.workspace.zoom == zoom

    window._select_layout_solution(1)
    assert window._solution_bounding_utilization_label.text() == "env% 50.0%"
    assert window._solution_waste_label.text() == "hueco 50.0%"
    action.trigger()
    assert calls == []
    assert clipboard.text() == "50.0%"
    assert window.services.layout.selected_solution_index == 1

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert not action.isEnabled()
    clipboard.setText("keep-me")
    window._copy_solution_bounding_utilization()
    assert calls == []
    assert clipboard.text() == "keep-me"

    window.services.layout.solutions = [gapped]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    window.services.preferences.update(
        window.services.preferences.current.__class__(language="en")
    )
    window._retranslate_ui()
    assert window._solution_bounding_utilization_label.text() == "bnd% 50.0%"
    assert action.isEnabled()
    action.trigger()
    assert clipboard.text() == "50.0%"
    assert "bnd" not in clipboard.text()
    assert calls == []
