"""Click placed/total to fit placed pieces (IDE-0070)."""

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from studio.models import StudioPiece, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from studio.main_window import MainWindow
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


def test_placed_label_click_fits_placed_pieces(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.workspace.resize(800, 600)
    window.workspace.reload_project()
    window.workspace.fit_board()
    window.workspace.zoom_in()
    assert window._placed_label.cursor().shape() == Qt.CursorShape.PointingHandCursor
    tip = window._placed_label.toolTip()
    assert "colocadas" in tip.casefold()
    assert "clic" in tip.casefold()
    piece = window.workspace.piece_item_by_id("A")
    assert piece is not None
    board_center = window.workspace._camera.center

    assert (
        window.eventFilter(window._placed_label, _mouse(QEvent.Type.MouseButtonPress))
        is True
    )
    assert (
        window.eventFilter(window._placed_label, _mouse(QEvent.Type.MouseButtonRelease))
        is True
    )
    assert window.workspace._camera.center == piece.sceneBoundingRect().center()
    assert window.workspace._camera.center != board_center


def test_placed_label_ignores_drag_and_zero_placed(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.workspace.resize(800, 600)
    window.workspace.reload_project()
    window.workspace.zoom_in()
    center = QPointF(window.workspace._camera.center)
    zoom = window.workspace.zoom

    assert (
        window.eventFilter(window._placed_label, _mouse(QEvent.Type.MouseButtonPress))
        is True
    )
    assert (
        window.eventFilter(
            window._placed_label, _mouse(QEvent.Type.MouseMove, -10, -10)
        )
        is False
    )
    assert (
        window.eventFilter(window._placed_label, _mouse(QEvent.Type.MouseButtonRelease))
        is False
    )
    assert window.workspace._camera.center == center
    assert window.workspace.zoom == zoom

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "prefs-empty.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    empty.services.projects.new_project(
        StudioProject(
            project_id="PRJ-0",
            name="Vacio",
            pieces=[StudioPiece("U", 100, 50)],
        )
    )
    empty.update_window_title()
    assert empty._placed_label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert "clic" not in empty._placed_label.toolTip().casefold()
    assert (
        empty.eventFilter(empty._placed_label, _mouse(QEvent.Type.MouseButtonPress))
        is False
    )
