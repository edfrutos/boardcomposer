"""Click omitted pieces to select them and fit any canvas geometry (IDE-0080)."""

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from studio.main_window import MainWindow
from studio.models import StudioPiece, StudioPlacement, StudioProject
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


def _open(window: MainWindow, project: StudioProject) -> None:
    window.services.projects.open_project(project, None)
    window.workspace.resize(800, 600)
    window.workspace.reload_project()
    window.update_window_title()


def test_omitted_label_click_selects_unplaced_inventory(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    project = StudioProject(
        project_id="PRJ-1",
        name="Taller",
        pieces=[
            StudioPiece("P1", 400, 300),
            StudioPiece("P2", 200, 100),
            StudioPiece("P3", 150, 80),
        ],
        placements=[StudioPlacement("P1", 0, 0)],
    )
    _open(window, project)
    label = window._omitted_label
    assert label.cursor().shape() == Qt.CursorShape.PointingHandCursor
    assert "clic" in label.toolTip().casefold()
    center = QPointF(window.workspace._camera.center)
    zoom = window.workspace.zoom

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is True
    assert set(window.workspace.selection.selected()) == {"P2", "P3"}
    assert window.workspace._camera.center == center
    assert window.workspace.zoom == zoom
    assert "seleccionadas" in window.statusBar().currentMessage().casefold()


def test_omitted_label_ignores_drag_and_zero(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    project = StudioProject(
        project_id="PRJ-1",
        name="Taller",
        pieces=[StudioPiece("P1", 100, 50), StudioPiece("P2", 80, 40)],
        placements=[StudioPlacement("P1", 0, 0)],
    )
    _open(window, project)
    label = window._omitted_label
    center = QPointF(window.workspace._camera.center)
    zoom = window.workspace.zoom

    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is True
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseMove, -10, -10)) is False
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is False
    assert window.workspace.selection.selected() == []
    assert window.workspace._camera.center == center
    assert window.workspace.zoom == zoom

    project.placements.append(StudioPlacement("P2", 20, 20))
    window.workspace.reload_project()
    window.update_window_title()
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is False
    assert window.workspace.selection.selected() == []


def test_omitted_label_without_project_keeps_selection(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    label = window._omitted_label
    assert label.isHidden()
    window._select_and_fit_omitted()
    assert window.workspace.selection.selected() == []
    assert window.statusBar().currentMessage() == window._tr(
        "status.nothing_to_select_omitted"
    )


def test_fit_piece_ids_frames_a_placed_piece(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.workspace.resize(800, 600)
    window.workspace.reload_project()
    window.workspace.fit_board()
    window.workspace.zoom_in()
    board_center = window.workspace._camera.center
    piece = window.workspace.piece_item_by_id("A")
    assert piece is not None
    assert window.workspace.fit_piece_ids(["A"]) is True
    assert window.workspace._camera.center == piece.sceneBoundingRect().center()
    assert window.workspace._camera.center != board_center
    assert window.workspace.fit_piece_ids(["missing"]) is False
