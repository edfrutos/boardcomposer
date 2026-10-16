"""Copy the status-bar solution score (IDE-0116)."""

from PySide6.QtWidgets import QApplication

from boardcomposer.domain import AssemblySolution, SolutionScore
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_inspector_board_utilization import _window


def test_copy_solution_score_uses_the_value(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    action = empty._actions["copy_solution_score"]
    assert "Ctrl+Alt+Shift+V" in action.shortcut().toString()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    empty._copy_solution_score()
    assert clipboard.text() == "keep-me"
    assert empty.statusBar().currentMessage() == empty._tr(
        "status.nothing_to_copy_solution_score"
    )

    window = _window(tmp_path)
    action = window._actions["copy_solution_score"]
    assert not action.isEnabled()
    calls: list[str] = []
    window._step_layout_solution = lambda _delta: calls.append("step")
    window._copy_solution_score()
    assert calls == []
    assert clipboard.text() == "keep-me"

    window.services.layout.solutions = [
        AssemblySolution(placements=[], score=SolutionScore()),
        AssemblySolution(
            placements=[],
            score=SolutionScore(waste_score=0.5, material_usage_score=0.25),
        ),
    ]
    window._select_layout_solution(0)
    zoom = window.workspace.zoom
    assert window._solution_score_label.text() == "pts. 0.00"
    assert action.isEnabled()
    action.trigger()
    assert calls == []
    assert clipboard.text() == "0.00"
    assert "pts." not in clipboard.text()
    assert window.statusBar().currentMessage() == window._tr(
        "status.solution_score_copied", value="0.00"
    )
    assert window.services.layout.selected_solution_index == 0
    assert window.workspace.zoom == zoom

    window._select_layout_solution(1)
    action.trigger()
    assert calls == []
    assert clipboard.text() == "0.75"
    assert window.services.layout.selected_solution_index == 1

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert not action.isEnabled()
    clipboard.setText("keep-me")
    window._copy_solution_score()
    assert calls == []
    assert clipboard.text() == "keep-me"

    window.services.layout.solutions = [
        AssemblySolution(
            placements=[],
            score=SolutionScore(waste_score=0.5, material_usage_score=0.25),
        )
    ]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    window.services.preferences.update(
        window.services.preferences.current.__class__(language="en")
    )
    window._retranslate_ui()
    assert window._solution_score_label.text() == "pts 0.75"
    assert action.isEnabled()
    action.trigger()
    assert clipboard.text() == "0.75"
    assert "pts" not in clipboard.text()
    assert calls == []
