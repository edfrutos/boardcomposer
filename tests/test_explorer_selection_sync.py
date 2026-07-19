"""Workspace piece selection mirrors onto the Explorador tree."""

from PySide6.QtCore import Qt

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window_with_pieces(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Sync",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[
                StudioPiece("A", 400, 300, "Demo", 19),
                StudioPiece("B", 200, 150, "Demo", 19),
            ],
            placements=[
                StudioPlacement("A", 0, 0, False, 0, "B1", 0, 0),
                StudioPlacement("B", 420, 0, False, 0, "B1", 0, 0),
            ],
        )
    )
    window = MainWindow(services)
    window.workspace.reload_project()
    window._reload_explorer()
    return window


def _current_explorer_role(window: MainWindow) -> str | None:
    item = window.explorer.currentItem()
    if item is None:
        return None
    role = item.data(0, Qt.ItemDataRole.UserRole)
    return role if isinstance(role, str) else None


def test_select_piece_highlights_explorer_item(qapp, tmp_path):
    del qapp
    window = _window_with_pieces(tmp_path)

    window.workspace.select_piece("B")

    assert _current_explorer_role(window) == "piece:B"


def test_clear_piece_selection_clears_explorer_piece(qapp, tmp_path):
    del qapp
    window = _window_with_pieces(tmp_path)
    window.workspace.select_piece("A")
    assert _current_explorer_role(window) == "piece:A"

    window.workspace.clear_piece_selection()

    assert _current_explorer_role(window) is None


def test_select_all_does_not_force_single_explorer_piece(qapp, tmp_path):
    del qapp
    window = _window_with_pieces(tmp_path)
    window.workspace.select_piece("A")
    assert _current_explorer_role(window) == "piece:A"

    window.workspace.select_all_pieces()

    assert len(window.workspace.selection.selected()) == 2
    assert _current_explorer_role(window) is None


def test_reload_explorer_restores_selected_piece(qapp, tmp_path):
    del qapp
    window = _window_with_pieces(tmp_path)
    window.workspace.select_piece("B")

    window._reload_explorer()

    assert _current_explorer_role(window) == "piece:B"


def _select_explorer_role(window: MainWindow, role: str) -> None:
    item = window._find_explorer_item_by_role(role)
    assert item is not None
    window.explorer.setCurrentItem(item)


def test_explorer_piece_selection_uses_full_inspector(qapp, tmp_path):
    del qapp
    window = _window_with_pieces(tmp_path)

    _select_explorer_role(window, "piece:A")

    text = window.inspector.toPlainText()
    assert "A" in text
    assert window._tr("inspector.position") in text
    assert window._tr("inspector.board") in text
    assert window.workspace.selection.selected() == ["A"]


def test_explorer_board_selection_clears_canvas_pieces(qapp, tmp_path):
    del qapp
    window = _window_with_pieces(tmp_path)
    window.workspace.select_piece("A")
    assert window.workspace.selection.selected() == ["A"]

    _select_explorer_role(window, "board:B1")

    assert window.workspace.selection.selected() == []
    assert _current_explorer_role(window) == "board:B1"
    assert "B1" in window.inspector.toPlainText()
    assert window._tr("inspector.quantity") in window.inspector.toPlainText()
