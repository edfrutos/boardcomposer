"""Status bar shows regularity score of the selected solution (IDE-0175)."""

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from boardcomposer.domain import AssemblySolution, SolutionScore
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_inspector_board_utilization import _window


def _mouse(event_type: QEvent.Type) -> QMouseEvent:
    return QMouseEvent(
        event_type,
        QPointF(2, 2),
        QPointF(2, 2),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )


def test_solution_regularity_score_follows_the_selected_solution(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    empty_label = empty._solution_regularity_score_label
    assert empty_label.objectName() == "statusSolutionRegularityScore"
    assert empty_label.isHidden()
    assert empty_label.cursor().shape() == Qt.CursorShape.ArrowCursor

    window = _window(tmp_path)
    label = window._solution_regularity_score_label
    assert label.text() == ""
    assert label.isHidden()
    assert label.toolTip() == ""
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor

    window.services.layout.solutions = [
        AssemblySolution(placements=[], score=SolutionScore()),
        AssemblySolution(
            placements=[],
            score=SolutionScore(
                waste_score=0.5,
                material_usage_score=0.25,
                cuts_score=0.75,
                regularity_score=0.40,
            ),
        ),
    ]
    window._select_layout_solution(0)
    zoom = window.workspace.zoom
    assert label.text() == "ptsr. 0.00"
    assert not label.isHidden()
    assert window._solution_score_label.text() == "pts. 0.00"
    assert window._solution_waste_score_label.text() == "ptsh. 0.00"
    assert window._solution_material_usage_score_label.text() == "ptsu. 0.00"
    assert window._solution_cuts_score_label.text() == "ptsc. 0.00"
    assert "puntuación de regularidad" in label.toolTip().casefold()
    assert "clic" not in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window._solution_label.text() == "1/2 sol."

    calls: list[str] = []
    window._step_layout_solution = lambda _delta: calls.append("step")
    window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress))
    window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease))
    assert calls == []
    assert window.services.layout.selected_solution_index == 0
    assert window.workspace.zoom == zoom

    window._select_layout_solution(1)
    assert label.text() == "ptsr. 0.40"
    assert window._solution_score_label.text() == "pts. 1.90"
    assert window._solution_waste_score_label.text() == "ptsh. 0.50"
    assert window._solution_material_usage_score_label.text() == "ptsu. 0.25"
    assert window._solution_cuts_score_label.text() == "ptsc. 0.75"
    assert "0.40" in label.toolTip()
    assert window._solution_label.text() == "2/2 sol."
    assert calls == []

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window._solution_label.isHidden()

    window.services.layout.solutions = [
        AssemblySolution(
            placements=[],
            score=SolutionScore(
                waste_score=0.5,
                material_usage_score=0.25,
                cuts_score=0.75,
                regularity_score=0.40,
            ),
        )
    ]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    window.services.preferences.update(
        window.services.preferences.current.__class__(language="en")
    )
    window._retranslate_ui()
    assert label.text() == "ptsr 0.40"
    assert "regularity score" in label.toolTip().casefold()
    assert "click" not in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
