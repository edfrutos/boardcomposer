"""Click solution internal gap area to select that solution (IDE-0138)."""

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from boardcomposer.domain import AssemblySolution, BoardPlacement
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


def _current_role(window) -> str | None:
    current = window.explorer.currentItem()
    if current is None:
        return None
    return current.data(0, Qt.ItemDataRole.UserRole)


def test_waste_area_label_click_selects_the_solution(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = [
        AssemblySolution(placements=[]),
        AssemblySolution(
            placements=[
                BoardPlacement("A", 0, 0, 200, 100),
                BoardPlacement("B", 200, 100, 100, 100),
            ]
        ),
    ]
    window._reload_explorer()
    window._select_layout_solution(1)
    board = window._find_explorer_item_by_role("board:B1")
    assert board is not None
    window.explorer.setCurrentItem(board)
    label = window._solution_waste_area_label
    assert label.text() == "hueár. 30000 mm²"
    assert label.cursor().shape() == Qt.CursorShape.PointingHandCursor
    zoom = window.workspace.zoom
    calls: list[str] = []
    window._apply_layout = lambda: calls.append("apply")
    window._step_layout_solution = lambda _delta: calls.append("step")
    window._copy_solution_waste_area = lambda: calls.append("copy")

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is True
    assert calls == []
    assert window.workspace.zoom == zoom
    assert window.services.layout.selected_solution_index == 1
    assert _current_role(window) == "solution:1"
    assert label.text() == "hueár. 30000 mm²"


def test_waste_area_label_ignores_drag_and_hidden(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = [AssemblySolution(placements=[])]
    window._reload_explorer()
    window._select_layout_solution(0)
    board = window._find_explorer_item_by_role("board:B1")
    assert board is not None
    window.explorer.setCurrentItem(board)
    label = window._solution_waste_area_label
    assert label.text() == "hueár. 0 mm²"

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseMove, -10, -10)) is False
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is False
    assert window.services.layout.selected_solution_index == 0
    assert _current_role(window) == "board:B1"

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is False


def test_waste_area_label_release_without_explorer_item_does_not_select(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = [AssemblySolution(placements=[])]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    board = window._find_explorer_item_by_role("board:B1")
    assert board is not None
    assert window._find_explorer_item_by_role("solution:0") is None
    window.explorer.setCurrentItem(board)
    label = window._solution_waste_area_label
    assert label.text() == "hueár. 0 mm²"
    assert not label.isHidden()

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is False
    assert window.services.layout.selected_solution_index == 0
    assert _current_role(window) == "board:B1"
