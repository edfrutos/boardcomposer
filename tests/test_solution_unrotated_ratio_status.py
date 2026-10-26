"""Status bar shows unrotated piece percentage of the selected solution (IDE-0157)."""

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


def test_solution_unrotated_ratio_follows_the_selected_solution(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    empty_label = empty._solution_unrotated_ratio_label
    assert empty_label.objectName() == "statusSolutionUnrotatedRatio"
    assert empty_label.isHidden()
    assert empty_label.cursor().shape() == Qt.CursorShape.ArrowCursor

    window = _window(tmp_path)
    label = window._solution_unrotated_ratio_label
    assert label.text() == ""
    assert label.isHidden()
    assert label.toolTip() == ""
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor

    packed = AssemblySolution(
        placements=[
            BoardPlacement("B1", 0, 0, 100, 50, rotated=False),
            BoardPlacement("B2", 100, 0, 50, 100, rotated=True),
            BoardPlacement("B3", 200, 0, 100, 50, rotated=False),
            BoardPlacement("B4", 300, 0, 100, 50, rotated=False),
        ]
    )
    window.services.layout.solutions = [
        AssemblySolution(placements=[]),
        packed,
    ]
    window._select_layout_solution(0)
    zoom = window.workspace.zoom
    assert label.text() == "nrot% 0.0%"
    assert not label.isHidden()
    assert window._solution_unrotated_label.text() == "nrot. 0"
    assert "porcentaje de piezas sin rotar" in label.toolTip().casefold()
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
    assert label.text() == "nrot% 75.0%"
    assert window._solution_unrotated_label.text() == "nrot. 3"
    assert window._solution_rotated_ratio_label.text() == "rot% 25.0%"
    assert "75.0%" in label.toolTip()
    assert window._solution_label.text() == "2/2 sol."
    assert calls == []

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window._solution_label.isHidden()

    window.services.layout.solutions = [packed]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    window.services.preferences.update(
        window.services.preferences.current.__class__(language="en")
    )
    window._retranslate_ui()
    assert label.text() == "unrot% 75.0%"
    assert "unrotated pieces percentage" in label.toolTip().casefold()
    assert "click" not in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
