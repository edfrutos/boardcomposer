"""Click the solution index to step to the next solution (IDE-0097)."""

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from boardcomposer.domain import AssemblySolution
from tests.test_inspector_board_utilization import _window


def _mouse(event_type: QEvent.Type, x: float = 2, y: float = 2) -> QMouseEvent:
    return QMouseEvent(
        event_type,
        QPointF(x, y),
        QPointF(x, y),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )


def test_solution_label_click_steps_to_the_next(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = [
        AssemblySolution(placements=[]),
        AssemblySolution(placements=[]),
    ]
    window._select_layout_solution(0)
    label = window._solution_label
    zoom = window.workspace.zoom
    calls: list[str] = []
    window._apply_layout = lambda: calls.append("apply")
    window._copy_solution_index = lambda: calls.append("copy")

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is True
    assert calls == []
    assert window.workspace.zoom == zoom
    assert window.services.layout.selected_solution_index == 1
    assert label.text() == "2/2 sol."

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is True
    assert calls == []
    assert window.services.layout.selected_solution_index == 0
    assert label.text() == "1/2 sol."


def test_solution_label_click_keeps_a_single_solution(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = [AssemblySolution(placements=[])]
    window._select_layout_solution(0)
    label = window._solution_label
    calls: list[str] = []
    window._apply_layout = lambda: calls.append("apply")

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is True
    assert calls == []
    assert window.services.layout.selected_solution_index == 0
    assert label.text() == "1/1 sol."
    assert window.statusBar().currentMessage() == window._tr(
        "status.only_one_visible_solution"
    )


def test_solution_label_ignores_drag_and_hidden(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = [
        AssemblySolution(placements=[]),
        AssemblySolution(placements=[]),
    ]
    window._select_layout_solution(0)
    label = window._solution_label

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseMove, -10, -10)) is False
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is False
    assert window.services.layout.selected_solution_index == 0

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is False
    assert window.services.layout.selected_solution_index == 0

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is False
    assert window.services.layout.selected_solution_index == 9

    window.services.layout.solutions = []
    window._update_solution_status()
    assert label.isHidden()
    assert label.toolTip() == ""
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is False
