"""Copy the status-bar solution rotated piece percentage (IDE-0155)."""

from PySide6.QtWidgets import QApplication

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_inspector_board_utilization import _window


def test_copy_solution_rotated_ratio_uses_the_percentage(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    action = empty._actions["copy_solution_rotated_ratio"]
    assert "Ctrl+Alt+Shift+8" in action.shortcut().toString()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    empty._copy_solution_rotated_ratio()
    assert clipboard.text() == "keep-me"
    assert empty.statusBar().currentMessage() == empty._tr(
        "status.nothing_to_copy_solution_rotated_ratio"
    )

    window = _window(tmp_path)
    action = window._actions["copy_solution_rotated_ratio"]
    assert not action.isEnabled()
    calls: list[str] = []
    window._step_layout_solution = lambda _delta: calls.append("step")
    window._copy_solution_rotated_ratio()
    assert calls == []
    assert clipboard.text() == "keep-me"

    packed = AssemblySolution(
        placements=[
            BoardPlacement("B1", 0, 0, 100, 50, rotated=False),
            BoardPlacement("B2", 100, 0, 50, 100, rotated=True),
            BoardPlacement("B3", 200, 0, 50, 100, rotated=True),
            BoardPlacement("B4", 300, 0, 100, 50, rotated=False),
        ]
    )
    window.services.layout.solutions = [
        AssemblySolution(placements=[]),
        packed,
    ]
    window._select_layout_solution(0)
    zoom = window.workspace.zoom
    assert window._solution_rotated_ratio_label.text() == "rot% 0.0%"
    assert action.isEnabled()
    action.trigger()
    assert calls == []
    assert clipboard.text() == "0.0%"
    assert "rot" not in clipboard.text()
    assert window.statusBar().currentMessage() == window._tr(
        "status.solution_rotated_ratio_copied", value="0.0%"
    )
    assert window.services.layout.selected_solution_index == 0
    assert window.workspace.zoom == zoom

    window._select_layout_solution(1)
    assert window._solution_rotated_ratio_label.text() == "rot% 50.0%"
    assert window._solution_rotated_label.text() == "rot. 2"
    action.trigger()
    assert calls == []
    assert clipboard.text() == "50.0%"
    assert window.services.layout.selected_solution_index == 1

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert not action.isEnabled()
    clipboard.setText("keep-me")
    window._copy_solution_rotated_ratio()
    assert calls == []
    assert clipboard.text() == "keep-me"

    window.services.layout.solutions = [packed]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    window.services.preferences.update(
        window.services.preferences.current.__class__(language="en")
    )
    window._retranslate_ui()
    assert window._solution_rotated_ratio_label.text() == "rot% 50.0%"
    assert action.isEnabled()
    action.trigger()
    assert clipboard.text() == "50.0%"
    assert "rot" not in clipboard.text()
    assert calls == []
