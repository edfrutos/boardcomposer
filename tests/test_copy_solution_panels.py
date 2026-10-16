"""Copy the status-bar solution boards count (IDE-0113)."""

from PySide6.QtWidgets import QApplication

from boardcomposer.domain import AssemblySolution, BoardPlacement, PanelReference
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_inspector_board_utilization import _window


def test_copy_solution_panels_uses_the_count(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    action = empty._actions["copy_solution_panels"]
    assert "Ctrl+Alt+Shift+W" in action.shortcut().toString()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    empty._copy_solution_panels()
    assert clipboard.text() == "keep-me"
    assert empty.statusBar().currentMessage() == empty._tr(
        "status.nothing_to_copy_solution_panels"
    )

    window = _window(tmp_path)
    action = window._actions["copy_solution_panels"]
    assert not action.isEnabled()
    calls: list[str] = []
    window._step_layout_solution = lambda _delta: calls.append("step")
    window._copy_solution_panels()
    assert calls == []
    assert clipboard.text() == "keep-me"

    window.services.layout.solutions = [
        AssemblySolution(placements=[]),
        AssemblySolution(
            placements=[
                BoardPlacement(
                    "A", 0, 0, 100, 50, panel_reference=PanelReference(0, 0)
                ),
                BoardPlacement(
                    "B", 0, 0, 100, 50, panel_reference=PanelReference(0, 1)
                ),
            ]
        ),
    ]
    window._select_layout_solution(0)
    zoom = window.workspace.zoom
    assert window._solution_panels_label.text() == "pan. 0"
    assert action.isEnabled()
    action.trigger()
    assert calls == []
    assert clipboard.text() == "0"
    assert "pan." not in clipboard.text()
    assert window.statusBar().currentMessage() == window._tr(
        "status.solution_panels_copied", n="0"
    )
    assert window.services.layout.selected_solution_index == 0
    assert window.workspace.zoom == zoom

    window._select_layout_solution(1)
    action.trigger()
    assert calls == []
    assert clipboard.text() == "2"
    assert window.services.layout.selected_solution_index == 1

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert not action.isEnabled()
    clipboard.setText("keep-me")
    window._copy_solution_panels()
    assert calls == []
    assert clipboard.text() == "keep-me"

    window.services.layout.solutions = [
        AssemblySolution(
            placements=[
                BoardPlacement(
                    "A", 0, 0, 100, 50, panel_reference=PanelReference(0, 0)
                ),
                BoardPlacement(
                    "B", 0, 0, 100, 50, panel_reference=PanelReference(0, 1)
                ),
            ]
        )
    ]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    window.services.preferences.update(
        window.services.preferences.current.__class__(language="en")
    )
    window._retranslate_ui()
    assert window._solution_panels_label.text() == "pnl 2"
    assert action.isEnabled()
    action.trigger()
    assert clipboard.text() == "2"
    assert "pnl" not in clipboard.text()
    assert calls == []
