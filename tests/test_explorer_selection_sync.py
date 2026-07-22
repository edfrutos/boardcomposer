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
    assert window.workspace.focused_board_id() == "B1"
    assert _current_explorer_role(window) == "board:B1"
    assert "B1" in window.inspector.toPlainText()
    assert window._tr("inspector.quantity") in window.inspector.toPlainText()


def test_explorer_board_focus_centers_and_clears_on_piece(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-2",
            name="Boards",
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
    window._reload_explorer()

    _select_explorer_role(window, "board:B2")

    assert window.workspace.focused_board_id() == "B2"
    b2_slots = [
        slot for slot in window.workspace._panel_slots.values() if slot.board_id == "B2"
    ]
    assert len(b2_slots) == 1
    expected_center = window.workspace._board_items[b2_slots[0].key].sceneBoundingRect()
    assert window.workspace._camera.center == expected_center.center()

    _select_explorer_role(window, "piece:A")

    assert window.workspace.focused_board_id() is None
    assert window.workspace.selection.selected() == ["A"]
    piece = window.workspace.piece_item_by_id("A")
    assert piece is not None
    assert window.workspace._camera.center == piece.sceneBoundingRect().center()


def test_click_board_on_canvas_focuses_and_syncs_explorer(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-3",
            name="ClickBoard",
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
    window._reload_explorer()
    window.workspace.select_piece("A")

    b2_slot = next(
        slot for slot in window.workspace._panel_slots.values() if slot.board_id == "B2"
    )
    hit = window.workspace.select_board_at(
        b2_slot.x_mm + 40,
        b2_slot.y_mm + 40,
    )

    assert hit is True
    assert window.workspace.selection.selected() == []
    assert window.workspace.focused_board_id() == "B2"
    assert _current_explorer_role(window) == "board:B2"
    assert "B2" in window.inspector.toPlainText()

    miss = window.workspace.select_board_at(-1000, -1000)
    assert miss is False


def test_undo_reloads_explorer_so_stale_piece_roles_disappear(qapp, tmp_path):
    """Undo must refresh Explorador; otherwise piece:ID clicks KeyError."""
    del qapp
    from studio.commands.duplicate_piece_command import DuplicatePieceCommand

    window = _window_with_pieces(tmp_path)
    project = window.services.projects.current_project
    assert project is not None
    source = next(piece for piece in project.pieces if piece.piece_id == "A")
    clone = StudioPiece(
        "A1",
        source.length_mm,
        source.width_mm,
        source.material,
        source.thickness_mm,
    )
    placement = StudioPlacement("A1", 50, 50, False, 0, "B1", 0, 0)
    window.services.commands.execute(
        DuplicatePieceCommand(window.services, clone, placement)
    )
    window.workspace.reload_project()
    window._reload_explorer()
    assert window._find_explorer_item_by_role("piece:A1") is not None

    window._undo()

    assert window._find_explorer_item_by_role("piece:A1") is None
    assert {piece.piece_id for piece in project.pieces} == {"A", "B"}
    window.refresh_inspector_for_piece("A1")
    assert window._tr("inspector.none") in window.inspector.toPlainText()
