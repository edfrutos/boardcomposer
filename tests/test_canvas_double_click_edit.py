"""Double-click on canvas piece/board opens the edit dialog."""

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="DblClick",
            boards=[
                StudioBoard("B1", 1000, 500, "Demo", 19, 1),
                StudioBoard("B2", 800, 400, "Demo", 19, 1),
            ],
            pieces=[StudioPiece("A", 200, 150, "Demo", 19)],
            placements=[
                StudioPlacement("A", 10, 20, False, 0, "B1", 0, 0),
            ],
        )
    )
    window = MainWindow(services)
    window.workspace.resize(800, 600)
    window.workspace.reload_project()
    return window


def _left_double_click(workspace, point):
    event = QMouseEvent(
        QEvent.Type.MouseButtonDblClick,
        QPointF(point),
        QPointF(workspace.mapToGlobal(point)),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    workspace.mouseDoubleClickEvent(event)


def test_double_click_piece_opens_edit(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    called: list[str] = []
    monkeypatch.setattr(
        window,
        "_edit_piece",
        lambda piece_id: called.append(piece_id),
    )
    fit_calls: list[bool] = []
    monkeypatch.setattr(
        window.workspace,
        "fit_board",
        lambda: fit_calls.append(True),
    )

    piece = window.workspace.piece_item_by_id("A")
    assert piece is not None
    point = window.workspace.mapFromScene(piece.sceneBoundingRect().center())
    _left_double_click(window.workspace, point)

    assert called == ["A"]
    assert fit_calls == []


def test_double_click_board_opens_edit(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    called: list[str] = []
    monkeypatch.setattr(
        window,
        "_edit_board",
        lambda board_id: called.append(board_id),
    )
    fit_calls: list[bool] = []
    monkeypatch.setattr(
        window.workspace,
        "fit_board",
        lambda: fit_calls.append(True),
    )

    b2_slot = next(
        slot for slot in window.workspace._panel_slots.values() if slot.board_id == "B2"
    )
    point = window.workspace.mapFromScene(QPointF(b2_slot.x_mm + 40, b2_slot.y_mm + 40))
    _left_double_click(window.workspace, point)

    assert called == ["B2"]
    assert fit_calls == []


def test_double_click_empty_fits_board(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    fit_calls: list[bool] = []
    monkeypatch.setattr(
        window.workspace,
        "fit_board",
        lambda: fit_calls.append(True),
    )
    edit_piece: list[str] = []
    monkeypatch.setattr(
        window,
        "_edit_piece",
        lambda piece_id: edit_piece.append(piece_id),
    )

    _left_double_click(window.workspace, window.workspace.rect().topLeft())

    assert fit_calls == [True]
    assert edit_piece == []
