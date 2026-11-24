"""Click maximum offcut aspect ratio to select that solution (IDE-0246)."""

import pytest
from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from boardcomposer.domain import AssemblySolution, Offcut, PanelReference
from tests.test_inspector_board_utilization import _window


def _mouse(
    event_type: QEvent.Type,
    x: float = 2,
    y: float = 2,
    button: Qt.MouseButton = Qt.MouseButton.LeftButton,
) -> QMouseEvent:
    return QMouseEvent(
        event_type,
        QPointF(x, y),
        QPointF(x, y),
        button,
        button,
        Qt.KeyboardModifier.NoModifier,
    )


def _current_role(window) -> str | None:
    current = window.explorer.currentItem()
    if current is None:
        return None
    return current.data(0, Qt.ItemDataRole.UserRole)


def _focus_board(window) -> None:
    board = window._find_explorer_item_by_role("board:B1")
    assert board is not None
    window.explorer.setCurrentItem(board)


@pytest.fixture
def window(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = [
        AssemblySolution(placements=[], offcuts=()),
        AssemblySolution(
            placements=[],
            offcuts=(
                Offcut(PanelReference(0, 0), 400, 0, 100, 10),
                Offcut(PanelReference(0, 0), 400, 0, 200, 100),
            ),
        ),
    ]
    window._reload_explorer()
    window._select_layout_solution(1)
    _focus_board(window)
    return window


def test_offcut_aspect_max_label_click_selects_the_solution(window):
    label = window._solution_offcut_aspect_max_label
    assert label.text() == "xrel. 10.00"
    assert label.cursor().shape() == Qt.CursorShape.PointingHandCursor
    zoom = window.workspace.zoom
    calls: list[str] = []
    window._apply_layout = lambda: calls.append("apply")
    window._step_layout_solution = lambda _delta: calls.append("step")
    window._copy_solution_offcut_aspect_max = lambda: calls.append("copy")

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is True
    assert _current_role(window) == "solution:1"
    assert calls == []
    assert window.workspace.zoom == zoom
    assert window.services.layout.selected_solution_index == 1
    assert label.text() == "xrel. 10.00"


@pytest.mark.parametrize(
    "cancel",
    [_mouse(QEvent.Type.MouseMove, -10, -10), QEvent(QEvent.Type.Leave)],
    ids=["drag-out", "leave"],
)
def test_offcut_aspect_max_label_cancelled_press_does_not_select(window, cancel):
    label = window._solution_offcut_aspect_max_label
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, cancel) is False
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is False
    assert _current_role(window) == "board:B1"


def test_offcut_aspect_max_label_ignores_right_click(window):
    label = window._solution_offcut_aspect_max_label
    right = Qt.MouseButton.RightButton
    press = _mouse(QEvent.Type.MouseButtonPress, button=right)
    release = _mouse(QEvent.Type.MouseButtonRelease, button=right)
    assert window.eventFilter(label, press) is False
    assert window.eventFilter(label, release) is False
    assert _current_role(window) == "board:B1"


def test_offcut_aspect_max_label_ignores_click_when_hidden(window):
    label = window._solution_offcut_aspect_max_label
    window._select_layout_solution(0)
    _focus_board(window)
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is False
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is False
    assert _current_role(window) == "board:B1"


def test_offcut_aspect_max_label_without_explorer_item_does_not_select(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = [
        AssemblySolution(
            placements=[],
            offcuts=(Offcut(PanelReference(0, 0), 400, 0, 50, 50),),
        )
    ]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    _focus_board(window)
    assert window._find_explorer_item_by_role("solution:0") is None
    label = window._solution_offcut_aspect_max_label
    assert not label.isHidden()

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is False
    assert _current_role(window) == "board:B1"
