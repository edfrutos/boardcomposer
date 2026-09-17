"""Core and Studio tests for suggest_gap (IDE-0036)."""

from __future__ import annotations

from boardcomposer.domain.grain import GRAIN_LOCKED
from boardcomposer.layout.suggest_gap import OccupiedRect, suggest_gap
from studio.commands import SuggestGapCommand
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.services import StudioServices
from studio.suggest_gap import suggest_gap_for_piece


def test_empty_panel_suggests_origin():
    suggestion = suggest_gap(
        panel_length_mm=300,
        panel_width_mm=200,
        piece_length_mm=80,
        piece_width_mm=50,
    )
    assert suggestion is not None
    assert (suggestion.x_mm, suggestion.y_mm) == (0.0, 0.0)
    assert suggestion.rotated is False


def test_suggests_tighter_gap_beside_occupied_piece():
    suggestion = suggest_gap(
        panel_length_mm=300,
        panel_width_mm=200,
        piece_length_mm=50,
        piece_width_mm=50,
        occupied=(OccupiedRect(0, 0, 100, 100),),
    )
    assert suggestion is not None
    assert (suggestion.x_mm, suggestion.y_mm) == (0.0, 100.0)


def test_prefer_near_picks_closer_origin():
    occupied = (OccupiedRect(400, 0, 200, 200),)
    suggestion = suggest_gap(
        panel_length_mm=1000,
        panel_width_mm=500,
        piece_length_mm=200,
        piece_width_mm=200,
        occupied=occupied,
        prefer_near=(400.0, 0.0),
    )
    assert suggestion is not None
    assert (suggestion.x_mm, suggestion.y_mm) == (400.0, 200.0)


def test_rotation_fits_when_straight_does_not():
    suggestion = suggest_gap(
        panel_length_mm=60,
        panel_width_mm=200,
        piece_length_mm=100,
        piece_width_mm=50,
        allow_rotation=True,
    )
    assert suggestion is not None
    assert suggestion.rotated is True
    assert (suggestion.length_mm, suggestion.width_mm) == (50.0, 100.0)


def test_locked_size_does_not_rotate():
    suggestion = suggest_gap(
        panel_length_mm=60,
        panel_width_mm=200,
        piece_length_mm=100,
        piece_width_mm=50,
        allow_rotation=False,
    )
    assert suggestion is None


def test_kerf_blocks_adjacent_slot():
    occupied = (OccupiedRect(0, 0, 100, 100),)
    without_kerf = suggest_gap(
        panel_length_mm=200,
        panel_width_mm=100,
        piece_length_mm=100,
        piece_width_mm=100,
        occupied=occupied,
        kerf_mm=0.0,
    )
    assert without_kerf is not None
    assert (without_kerf.x_mm, without_kerf.y_mm) == (100.0, 0.0)

    with_kerf = suggest_gap(
        panel_length_mm=200,
        panel_width_mm=100,
        piece_length_mm=100,
        piece_width_mm=100,
        occupied=occupied,
        kerf_mm=4.0,
    )
    assert with_kerf is None


def test_oversized_piece_returns_none():
    assert (
        suggest_gap(
            panel_length_mm=100,
            panel_width_mm=100,
            piece_length_mm=150,
            piece_width_mm=50,
        )
        is None
    )


def _studio_project() -> StudioProject:
    return StudioProject(
        project_id="PRJ",
        name="Gap",
        boards=[StudioBoard("TAB", 1000, 500, "Demo", 19, 1)],
        pieces=[
            StudioPiece("A", 200, 200, "Demo", 19),
            StudioPiece("B", 200, 200, "Demo", 19),
            StudioPiece("C", 100, 50, "Demo", 19, grain=GRAIN_LOCKED),
        ],
        placements=[
            StudioPlacement("B", 400, 0, False, 0, "TAB", 0, 0),
        ],
        kerf_mm=0.0,
    )


def test_studio_adapter_excludes_moving_piece():
    project = _studio_project()
    project.placements.append(StudioPlacement("A", 0, 0, False, 0, "TAB", 0, 0))
    suggestion = suggest_gap_for_piece(
        project,
        "A",
        board_id="TAB",
        board_instance=0,
        stock_panel_index=0,
        prefer_near=(400.0, 0.0),
        keep_rotation=True,
    )
    assert suggestion is not None
    assert (suggestion.x_mm, suggestion.y_mm) == (400.0, 200.0)
    assert suggestion.rotated is False


def test_studio_adapter_grain_lock_skips_rotation():
    project = _studio_project()
    project.boards[0] = StudioBoard("TAB", 60, 200, "Demo", 19, 1)
    suggestion = suggest_gap_for_piece(
        project,
        "C",
        board_id="TAB",
        board_instance=0,
        stock_panel_index=0,
    )
    assert suggestion is None


def test_suggest_gap_command_undo_restores_unplaced():
    services = StudioServices()
    project = _studio_project()
    services.projects.new_project(project)
    new = StudioPlacement("A", 0, 0, False, 0, "TAB", 0, 0)
    services.commands.execute(SuggestGapCommand(services, "A", None, new))
    assert project.placement_by_piece_id("A") is not None
    services.commands.undo()
    assert project.placement_by_piece_id("A") is None
    services.commands.redo()
    placed = project.placement_by_piece_id("A")
    assert placed is not None
    assert (placed.x_mm, placed.y_mm) == (0.0, 0.0)
