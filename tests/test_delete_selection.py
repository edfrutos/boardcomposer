"""Delete key removes selected piece or focused board."""

from PySide6.QtWidgets import QMessageBox

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
            name="Del",
            boards=[
                StudioBoard("B1", 1000, 500, "Demo", 19, 1),
                StudioBoard("B2", 800, 400, "Demo", 19, 1),
            ],
            pieces=[StudioPiece("A", 200, 100, "Demo", 19)],
            placements=[
                StudioPlacement("A", 10, 20, False, 0, "B1", 0, 0),
            ],
        )
    )
    window = MainWindow(services)
    window.workspace.reload_project()
    window._reload_explorer()
    return window


def test_delete_still_removes_selected_piece(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    window.workspace.select_piece("A")
    monkeypatch.setattr(
        QMessageBox,
        "question",
        lambda *args, **kwargs: QMessageBox.StandardButton.Yes,
    )

    window._actions["delete_piece"].trigger()

    project = window.services.projects.current_project
    assert project is not None
    assert project.pieces == []


def test_delete_removes_focused_board(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    window.workspace.clear_piece_selection()
    window.select_explorer_board("B2")
    monkeypatch.setattr(
        QMessageBox,
        "question",
        lambda *args, **kwargs: QMessageBox.StandardButton.Yes,
    )

    window._delete_selected_piece()

    project = window.services.projects.current_project
    assert project is not None
    assert [board.board_id for board in project.boards] == ["B1"]
    assert "B2" in window.statusBar().currentMessage()


def test_delete_without_target_shows_status(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.explorer.setCurrentItem(None)
    window.workspace.clear_piece_selection()

    window._delete_selected_piece()

    assert window._tr("status.nothing_to_delete") in (
        window.statusBar().currentMessage()
    )
