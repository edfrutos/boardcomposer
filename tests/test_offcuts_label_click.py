"""Click offcuts to select the boards that own them (IDE-0094)."""

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from boardcomposer.domain import AssemblySolution, Offcut, PanelReference
from tests.test_inspector_board_utilization import _window
from tests.test_offcuts_status import _offcut


def _mouse(event_type: QEvent.Type, x: float = 2, y: float = 2) -> QMouseEvent:
    return QMouseEvent(
        event_type,
        QPointF(x, y),
        QPointF(x, y),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )


def _roles(window) -> set[str]:
    return {
        item.data(0, Qt.ItemDataRole.UserRole)
        for item in window.explorer.selectedItems()
    }


def test_offcuts_label_click_selects_one_board(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window._reload_explorer()
    window.services.layout.solutions = [
        AssemblySolution(placements=[], offcuts=(_offcut(0),)),
    ]
    window._select_layout_solution(0)
    label = window._offcuts_label
    assert label.cursor().shape() == Qt.CursorShape.PointingHandCursor
    window.inspector.setPlainText("otro")
    zoom = window.workspace.zoom
    calls: list[str] = []
    window._promote_offcuts = lambda: calls.append("promote")
    window._edit_board = lambda _board_id: calls.append("edit")

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is True
    assert calls == []
    assert window.workspace.zoom == zoom
    assert "Tablero: B1" in window.inspector.toPlainText()
    assert window.workspace.focused_board_id() == "B1"
    assert _roles(window) == {"board:B1"}


def test_offcuts_label_click_selects_several_boards(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window._reload_explorer()
    window.services.layout.solutions = [
        AssemblySolution(
            placements=[],
            offcuts=(
                _offcut(0),
                Offcut(PanelReference(1, 0), 10, 0, 100, 50),
            ),
        ),
    ]
    window._select_layout_solution(0)
    label = window._offcuts_label
    zoom = window.workspace.zoom
    calls: list[str] = []
    window._promote_offcuts = lambda: calls.append("promote")
    window._edit_board = lambda _board_id: calls.append("edit")

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is True
    assert calls == []
    assert window.workspace.zoom == zoom
    assert window.workspace.focused_board_id() == "B1"
    assert _roles(window) == {"board:B1", "board:B2"}


def test_offcuts_label_ignores_drag_hidden_and_bad_index(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window._reload_explorer()
    window.services.layout.solutions = [
        AssemblySolution(placements=[], offcuts=(_offcut(0),)),
    ]
    window._select_layout_solution(0)
    label = window._offcuts_label
    window.inspector.setPlainText("otro")

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseMove, -10, -10)) is False
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is False
    assert window.inspector.toPlainText() == "otro"

    window.services.layout.solutions = [
        AssemblySolution(
            placements=[],
            offcuts=(Offcut(PanelReference(9, 0), 10, 0, 100, 50),),
        ),
    ]
    window.services.layout.selected_solution_index = 0
    window._update_offcuts_status()
    assert not label.isHidden()
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is False
    assert window.inspector.toPlainText() == "otro"

    window.services.layout.solutions = []
    window._update_offcuts_status()
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is False
    assert window.inspector.toPlainText() == "otro"
