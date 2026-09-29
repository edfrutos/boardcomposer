"""Click the physical-board count to fit all boards (IDE-0071)."""

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
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


def test_boards_label_click_fits_all_boards(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.workspace.resize(800, 600)
    window.workspace.reload_project()
    window.workspace.fit_board()
    fitted_center = QPointF(window.workspace._camera.center)
    fitted_zoom = window.workspace.zoom
    window.workspace.zoom_in()
    assert window._boards_label.cursor().shape() == Qt.CursorShape.PointingHandCursor
    tip = window._boards_label.toolTip()
    assert "físicos" in tip.casefold()
    assert "Ctrl+0" in tip or "⌘0" in tip
    piece = window.workspace.piece_item_by_id("A")
    assert piece is not None

    assert (
        window.eventFilter(window._boards_label, _mouse(QEvent.Type.MouseButtonPress))
        is True
    )
    assert (
        window.eventFilter(window._boards_label, _mouse(QEvent.Type.MouseButtonRelease))
        is True
    )
    assert window.workspace._camera.center == fitted_center
    assert window.workspace.zoom == fitted_zoom
    assert window.workspace._camera.center != piece.sceneBoundingRect().center()


def test_boards_label_ignores_drag_and_hides_without_boards(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.workspace.resize(800, 600)
    window.workspace.reload_project()
    window.workspace.zoom_in()
    center = QPointF(window.workspace._camera.center)
    zoom = window.workspace.zoom

    assert (
        window.eventFilter(window._boards_label, _mouse(QEvent.Type.MouseButtonPress))
        is True
    )
    assert (
        window.eventFilter(
            window._boards_label, _mouse(QEvent.Type.MouseMove, -10, -10)
        )
        is False
    )
    assert (
        window.eventFilter(window._boards_label, _mouse(QEvent.Type.MouseButtonRelease))
        is False
    )
    assert window.workspace._camera.center == center
    assert window.workspace.zoom == zoom

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "prefs-empty.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    assert empty._boards_label.isHidden()
    assert empty._boards_label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert (
        empty.eventFilter(empty._boards_label, _mouse(QEvent.Type.MouseButtonPress))
        is False
    )
