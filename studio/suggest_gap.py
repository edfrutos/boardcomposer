"""Studio adapter for Core ``suggest_gap`` (IDE-0036)."""

from __future__ import annotations

from boardcomposer.domain.grain import grain_allows_rotation
from boardcomposer.layout.suggest_gap import (
    GapSuggestion,
    OccupiedRect,
    suggest_gap,
)
from studio.models import StudioPiece, StudioPlacement, StudioProject


def placement_is_rotated(placement: StudioPlacement) -> bool:
    """True when the placement uses the swapped L×W orientation."""
    return bool(placement.rotated) or placement.rotation % 180 == 90


def placed_size(piece: StudioPiece, placement: StudioPlacement) -> tuple[float, float]:
    """Return the on-panel length×width of ``piece`` at ``placement``."""
    if placement_is_rotated(placement):
        return piece.width_mm, piece.length_mm
    return piece.length_mm, piece.width_mm


def suggest_gap_for_piece(
    project: StudioProject,
    piece_id: str,
    *,
    board_id: str,
    board_instance: int = 0,
    stock_panel_index: int | None = None,
    prefer_near: tuple[float, float] | None = None,
    keep_rotation: bool = False,
) -> GapSuggestion | None:
    """Suggest a MaxRects origin on one physical panel for ``piece_id``.

    Occupied placements on that panel exclude ``piece_id``. Grain lock
    blocks rotation unless ``keep_rotation`` (drop keeps current L×W).
    """
    try:
        piece = project.piece_by_id(piece_id)
    except KeyError:
        return None

    board = _board_for(project, board_id, stock_panel_index)
    if board is None:
        return None

    placement = project.placement_by_piece_id(piece_id)
    if keep_rotation:
        if placement is None:
            piece_length, piece_width = piece.length_mm, piece.width_mm
        else:
            piece_length, piece_width = placed_size(piece, placement)
        allow_rotation = False
    else:
        piece_length, piece_width = piece.length_mm, piece.width_mm
        allow_rotation = grain_allows_rotation(piece.grain)

    occupied = occupied_rects_on_panel(
        project,
        board_id=board_id,
        board_instance=board_instance,
        stock_panel_index=stock_panel_index,
        exclude_piece_id=piece_id,
    )
    suggestion = suggest_gap(
        panel_length_mm=board.length_mm,
        panel_width_mm=board.width_mm,
        piece_length_mm=piece_length,
        piece_width_mm=piece_width,
        occupied=occupied,
        kerf_mm=project.kerf_mm,
        allow_rotation=allow_rotation,
        prefer_near=prefer_near,
    )
    if suggestion is None:
        return None
    if keep_rotation and placement is not None:
        return GapSuggestion(
            x_mm=suggestion.x_mm,
            y_mm=suggestion.y_mm,
            length_mm=suggestion.length_mm,
            width_mm=suggestion.width_mm,
            rotated=placement_is_rotated(placement),
        )
    return suggestion


def occupied_rects_on_panel(
    project: StudioProject,
    *,
    board_id: str,
    board_instance: int,
    stock_panel_index: int | None,
    exclude_piece_id: str | None = None,
) -> list[OccupiedRect]:
    """Occupied AABBs on one physical panel, excluding ``exclude_piece_id``."""
    occupied: list[OccupiedRect] = []
    for placement in project.placements:
        if exclude_piece_id is not None and placement.piece_id == exclude_piece_id:
            continue
        if not _same_panel(
            placement,
            board_id=board_id,
            board_instance=board_instance,
            stock_panel_index=stock_panel_index,
        ):
            continue
        try:
            other = project.piece_by_id(placement.piece_id)
        except KeyError:
            continue
        length, width = placed_size(other, placement)
        occupied.append(
            OccupiedRect(
                x_mm=placement.x_mm,
                y_mm=placement.y_mm,
                length_mm=length,
                width_mm=width,
            )
        )
    return occupied


def _same_panel(
    placement: StudioPlacement,
    *,
    board_id: str,
    board_instance: int,
    stock_panel_index: int | None,
) -> bool:
    if placement.board_id != board_id:
        return False
    if placement.board_instance != board_instance:
        return False
    if stock_panel_index is None or placement.stock_panel_index is None:
        return True
    return placement.stock_panel_index == stock_panel_index


def _board_for(project: StudioProject, board_id: str, stock_panel_index: int | None):
    if stock_panel_index is not None and 0 <= stock_panel_index < len(project.boards):
        board = project.boards[stock_panel_index]
        if board.board_id == board_id:
            return board
    return next((item for item in project.boards if item.board_id == board_id), None)
