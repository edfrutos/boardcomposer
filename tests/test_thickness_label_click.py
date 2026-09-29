"""Click the board thickness to edit that board (IDE-0074)."""

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from studio.models import StudioBoard
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


def test_thickness_label_click_edits_the_only_board(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    calls: list[str] = []
    monkeypatch.setattr(window, "_edit_board", lambda board_id: calls.append(board_id))
    assert (
        window._board_thickness_label.cursor().shape()
        == Qt.CursorShape.PointingHandCursor
    )

    assert (
        window.eventFilter(
            window._board_thickness_label, _mouse(QEvent.Type.MouseButtonPress)
        )
        is True
    )
    assert (
        window.eventFilter(
            window._board_thickness_label, _mouse(QEvent.Type.MouseButtonRelease)
        )
        is True
    )
    assert calls == ["B1"]


def test_thickness_label_ignores_drag_and_unfocused_boards(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    calls: list[str] = []
    monkeypatch.setattr(window, "_edit_board", lambda board_id: calls.append(board_id))

    assert (
        window.eventFilter(
            window._board_thickness_label, _mouse(QEvent.Type.MouseButtonPress)
        )
        is True
    )
    assert (
        window.eventFilter(
            window._board_thickness_label, _mouse(QEvent.Type.MouseMove, -10, -10)
        )
        is False
    )
    assert (
        window.eventFilter(
            window._board_thickness_label, _mouse(QEvent.Type.MouseButtonRelease)
        )
        is False
    )
    assert calls == []

    project = window.services.projects.current_project
    assert project is not None
    project.boards.append(StudioBoard("B2", 800, 400, "Demo", 16, 1))
    window.workspace.reload_project()
    window.update_window_title()
    assert window._board_thickness_label.isHidden()
    assert window._board_thickness_label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert (
        window.eventFilter(
            window._board_thickness_label, _mouse(QEvent.Type.MouseButtonPress)
        )
        is False
    )

    window.workspace.focus_board("B2")
    assert (
        window.eventFilter(
            window._board_thickness_label, _mouse(QEvent.Type.MouseButtonPress)
        )
        is True
    )
    assert (
        window.eventFilter(
            window._board_thickness_label, _mouse(QEvent.Type.MouseButtonRelease)
        )
        is True
    )
    assert calls == ["B2"]
