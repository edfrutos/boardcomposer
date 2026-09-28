"""Click the status-bar zoom label to return to 100% (IDE-0062)."""

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from tests.test_zoom_limit_enablement import _window


def _click() -> QMouseEvent:
    return QMouseEvent(
        QEvent.Type.MouseButtonRelease,
        QPointF(2, 2),
        QPointF(2, 2),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )


def test_zoom_label_click_resets_to_100_without_moving_center(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.workspace.zoom_in()
    assert window.workspace.can_zoom_100
    assert window._zoom_label.cursor().shape() == Qt.CursorShape.PointingHandCursor
    center = window.workspace._camera.center
    cx, cy = center.x(), center.y()

    assert window.eventFilter(window._zoom_label, _click()) is True
    assert window.workspace.zoom == 1.0
    assert abs(window.workspace._camera.center.x() - cx) < 1e-6
    assert abs(window.workspace._camera.center.y() - cy) < 1e-6
    assert window._zoom_label.cursor().shape() == Qt.CursorShape.ArrowCursor

    window._zoom_100()
    assert window.workspace.zoom == 1.0
    assert window.statusBar().currentMessage() == window._tr("status.zoom_already_100")
    assert window.eventFilter(window._zoom_label, _click()) is True
    assert window.workspace.zoom == 1.0
