"""Status bar shows board utilization ratio of the selected solution (IDE-0145)."""

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from boardcomposer.domain import AssemblySolution, BoardPlacement
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


def test_solution_board_utilization_follows_the_selected_solution(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    empty_label = empty._solution_board_utilization_label
    assert empty_label.objectName() == "statusSolutionBoardUtilization"
    assert empty_label.isHidden()
    assert empty_label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert empty._board_utilization_label.objectName() == "statusBoardUtilization"

    window = _window(tmp_path)
    label = window._solution_board_utilization_label
    board_util = window._board_utilization_label
    assert label.text() == ""
    assert label.isHidden()
    assert label.toolTip() == ""
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor

    window.services.layout.solutions = [
        AssemblySolution(placements=[]),
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 400, 300)]),
    ]
    window._select_layout_solution(0)
    zoom = window.workspace.zoom
    assert label.text() == "aprv. 0.0%"
    assert not label.isHidden()
    assert window._solution_board_waste_label.text() == "sbr. 100.0%"
    assert "aprovechamiento de tableros" in label.toolTip().casefold()
    assert "clic" not in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window._solution_label.text() == "1/2 sol."
    assert label.text() != board_util.text()
    assert "uso" not in label.text()

    calls: list[str] = []
    window._step_layout_solution = lambda _delta: calls.append("step")
    window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress))
    window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease))
    assert calls == []
    assert window.services.layout.selected_solution_index == 0
    assert window.workspace.zoom == zoom

    window._select_layout_solution(1)
    assert label.text() == "aprv. 24.0%"
    assert window._solution_board_waste_label.text() == "sbr. 76.0%"
    assert "24.0%" in label.toolTip()
    assert window._solution_label.text() == "2/2 sol."
    assert calls == []
    assert "uso" not in label.text()

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window._solution_label.isHidden()

    window.services.layout.solutions = [
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 400, 300)])
    ]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    window.services.preferences.update(
        window.services.preferences.current.__class__(language="en")
    )
    window._retranslate_ui()
    assert label.text() == "util. 24.0%"
    assert "board utilization" in label.toolTip().casefold()
    assert "click" not in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert "use" not in label.text()
