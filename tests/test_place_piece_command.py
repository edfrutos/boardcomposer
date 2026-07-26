"""Place unplaced pieces onto a focused board panel."""

from __future__ import annotations

import pytest

from studio.commands import PlacePieceCommand
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.panel_compatibility import (
    incompatibility_reason,
    piece_compatible_with_board,
)
from studio.services import StudioServices


def _services_with_project() -> StudioServices:
    services = StudioServices()
    project = StudioProject(
        project_id="PRJ",
        name="Garage",
        boards=[
            StudioBoard(
                "TAB-A01", 850, 480, material="Melamina", thickness_mm=18, quantity=1
            ),
            StudioBoard("TAB-T01", 1180, 670, material="1", thickness_mm=6, quantity=1),
        ],
        pieces=[
            StudioPiece("T1", 274, 96, material="1", thickness_mm=6),
            StudioPiece("T2", 204, 60, material="Demo", thickness_mm=6),
            StudioPiece("A1", 400, 200, material="Melamina", thickness_mm=18),
        ],
        placements=[],
    )
    services.projects.new_project(project)
    return services


def test_piece_compatible_with_matching_board():
    piece = StudioPiece("T1", 100, 50, material="1", thickness_mm=6)
    board = StudioBoard("TAB-T01", 1180, 670, material="1", thickness_mm=6)
    assert piece_compatible_with_board(piece, board)
    assert incompatibility_reason(piece, board) is None


def test_piece_incompatible_thickness_and_material():
    piece = StudioPiece("T1", 100, 50, material="Demo", thickness_mm=18)
    board = StudioBoard("TAB-T01", 1180, 670, material="1", thickness_mm=6)
    assert not piece_compatible_with_board(piece, board)
    assert incompatibility_reason(piece, board) == "both"


def test_place_piece_command_round_trip():
    services = _services_with_project()
    placement = StudioPlacement(
        piece_id="T1",
        x_mm=20,
        y_mm=20,
        board_id="TAB-T01",
        board_instance=0,
        stock_panel_index=1,
    )
    command = PlacePieceCommand(services, placement)
    services.commands.execute(command)
    project = services.projects.current_project
    assert project is not None
    assert project.placement_by_piece_id("T1") is not None

    services.commands.undo()
    assert project.placement_by_piece_id("T1") is None


pytestmark = pytest.mark.usefixtures("qapp")


def test_main_window_places_unplaced_on_focused_board():
    from studio.main_window import MainWindow

    services = _services_with_project()
    window = MainWindow(services)
    window.workspace.reload_project()
    window.workspace.focus_board("TAB-T01")
    window._place_piece_on_focused_board("T1")

    project = services.projects.current_project
    assert project is not None
    placed = project.placement_by_piece_id("T1")
    assert placed is not None
    assert placed.board_id == "TAB-T01"
    assert placed.stock_panel_index == 1


def test_main_window_rejects_incompatible_piece():
    from studio.main_window import MainWindow

    services = _services_with_project()
    window = MainWindow(services)
    window.workspace.reload_project()
    window.workspace.focus_board("TAB-T01")
    window._place_piece_on_focused_board("T2")  # material Demo ≠ 1

    project = services.projects.current_project
    assert project is not None
    assert project.placement_by_piece_id("T2") is None


def test_selecting_unplaced_piece_keeps_placement_target():
    from studio.main_window import MainWindow

    services = _services_with_project()
    window = MainWindow(services)
    window.workspace.reload_project()
    window.workspace.focus_board("TAB-T01")
    assert window.workspace.focused_board_id() == "TAB-T01"

    # Same as Explorador click / context menu: select piece after board focus.
    window.workspace.select_piece("T1")
    assert window.workspace.placement_target_board_id() == "TAB-T01"
    # Highlight may remain for unplaced pieces.
    assert window.workspace.focused_board_id() == "TAB-T01"

    window._place_piece_on_focused_board("T1")
    project = services.projects.current_project
    assert project is not None
    assert project.placement_by_piece_id("T1") is not None


def test_context_menu_place_after_set_current_item():
    """Regression: setCurrentItem used to clear board focus before Place."""
    from studio.main_window import MainWindow

    services = _services_with_project()
    window = MainWindow(services)
    window.workspace.reload_project()
    window._reload_explorer()
    window.workspace.focus_board("TAB-T01")

    item = window._find_explorer_item_by_role("piece:T1")
    assert item is not None
    window.explorer.setCurrentItem(item)
    assert window.workspace.placement_target_board_id() == "TAB-T01"

    window._run_explorer_context_action("place_on_board", "piece:T1")
    project = services.projects.current_project
    assert project is not None
    placed = project.placement_by_piece_id("T1")
    assert placed is not None
    assert placed.board_id == "TAB-T01"
