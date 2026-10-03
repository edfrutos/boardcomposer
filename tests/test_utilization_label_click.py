"""Click board utilization to select that board (IDE-0082)."""

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

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


def test_utilization_label_click_selects_the_focused_board(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, placed=True)
    window._reload_explorer()
    window.workspace.focus_board("B1")
    label = window._board_utilization_label
    assert label.cursor().shape() == Qt.CursorShape.PointingHandCursor
    assert "clic" in label.toolTip().casefold()
    window.inspector.setPlainText("otro")

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is True
    text = window.inspector.toPlainText()
    assert "Tablero: B1" in text
    assert "Aprovechamiento: 24.0%" in text
    item = window.explorer.currentItem()
    assert item is not None
    assert item.data(0, Qt.ItemDataRole.UserRole) == "board:B1"
    assert window.workspace.focused_board_id() == "B1"


def test_utilization_label_ignores_drag_and_hidden(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, placed=True)
    window._reload_explorer()
    window.workspace.focus_board("B1")
    label = window._board_utilization_label
    window.inspector.setPlainText("otro")

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseMove, -10, -10)) is False
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is False
    assert window.inspector.toPlainText() == "otro"

    window.workspace.focus_board("B2")
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is False
    assert window.inspector.toPlainText() == "otro"
