"""Ctrl+D duplicates the selected piece or focused board."""

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
            name="Dup",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
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


def test_ctrl_d_still_duplicates_selected_piece(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.workspace.select_piece("A")

    window._actions["duplicate_piece"].trigger()

    project = window.services.projects.current_project
    assert project is not None
    ids = [piece.piece_id for piece in project.pieces]
    assert "A" in ids
    assert any(piece_id.startswith("A-copy") for piece_id in ids)


def test_ctrl_d_duplicates_focused_board(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.workspace.clear_piece_selection()
    window.select_explorer_board("B1")

    window._duplicate_selected_piece()

    project = window.services.projects.current_project
    assert project is not None
    board_ids = [board.board_id for board in project.boards]
    assert "B1" in board_ids
    assert any(board_id.startswith("B1-copy") for board_id in board_ids)
    assert window.workspace.focused_board_id() is not None
    assert window.workspace.focused_board_id().startswith("B1-copy")


def test_ctrl_d_without_target_shows_status(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.explorer.setCurrentItem(None)
    window.workspace.clear_piece_selection()

    window._duplicate_selected_piece()

    assert window._tr("status.nothing_to_duplicate") in (
        window.statusBar().currentMessage()
    )
