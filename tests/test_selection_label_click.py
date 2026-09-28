"""Click the selection count to fit the view (IDE-0066)."""

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from tests.test_copy_selection_id import _window


def _mouse(event_type: QEvent.Type, x: float = 2, y: float = 2) -> QMouseEvent:
    return QMouseEvent(
        event_type,
        QPointF(x, y),
        QPointF(x, y),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )


def test_selection_label_click_fits_the_piece(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.workspace.resize(800, 600)
    window.workspace.reload_project()
    window.workspace.fit_board()
    window.workspace.select_piece("A")
    window.workspace.zoom_in()
    assert window._selection_label.cursor().shape() == Qt.CursorShape.PointingHandCursor
    tip = window._selection_label.toolTip()
    assert "seleccionadas" in tip.casefold()
    assert "Ctrl+Shift+0" in tip or "⇧⌘0" in tip
    piece = window.workspace.piece_item_by_id("A")
    assert piece is not None

    assert (
        window.eventFilter(
            window._selection_label, _mouse(QEvent.Type.MouseButtonPress)
        )
        is True
    )
    assert (
        window.eventFilter(
            window._selection_label, _mouse(QEvent.Type.MouseButtonRelease)
        )
        is True
    )
    assert window.workspace._camera.center == piece.sceneBoundingRect().center()


def test_selection_label_ignores_drag_and_empty_selection(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.workspace.resize(800, 600)
    window.workspace.reload_project()
    window.workspace.select_piece("A")
    window.workspace.zoom_in()
    center = QPointF(window.workspace._camera.center)
    zoom = window.workspace.zoom

    assert (
        window.eventFilter(
            window._selection_label, _mouse(QEvent.Type.MouseButtonPress)
        )
        is True
    )
    assert (
        window.eventFilter(
            window._selection_label, _mouse(QEvent.Type.MouseMove, -10, -10)
        )
        is False
    )
    assert (
        window.eventFilter(
            window._selection_label, _mouse(QEvent.Type.MouseButtonRelease)
        )
        is False
    )
    assert window.workspace._camera.center == center
    assert window.workspace.zoom == zoom

    window.workspace.clear_piece_selection()
    assert window._selection_label.isHidden()
    assert window._selection_label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert (
        window.eventFilter(
            window._selection_label, _mouse(QEvent.Type.MouseButtonPress)
        )
        is False
    )
    assert window.workspace.zoom == zoom
