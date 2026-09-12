"""Validate and apply a two-piece placement swap (IDE-0019)."""

from __future__ import annotations

from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.panel_compatibility import incompatibility_reason


def placed_size(piece: StudioPiece, rotation: int) -> tuple[float, float]:
    """Return occupied (length, width) for ``piece`` at ``rotation``."""
    if rotation % 180 == 90:
        return piece.width_mm, piece.length_mm
    return piece.length_mm, piece.width_mm


def board_by_id(project: StudioProject, board_id: str | None) -> StudioBoard | None:
    if not board_id:
        return None
    for board in project.boards:
        if board.board_id == board_id:
            return board
    return None


def same_physical_panel(left: StudioPlacement, right: StudioPlacement) -> bool:
    return (
        left.board_id == right.board_id
        and left.board_instance == right.board_instance
        and left.stock_panel_index == right.stock_panel_index
    )


def _rects_overlap(
    left: tuple[float, float, float, float],
    right: tuple[float, float, float, float],
) -> bool:
    ax, ay, aw, ah = left
    bx, by, bw, bh = right
    return not (ax + aw <= bx or bx + bw <= ax or ay + ah <= by or by + bh <= ay)


def _fits_board(
    board: StudioBoard, x: float, y: float, width: float, height: float
) -> bool:
    return (
        x >= -1e-6
        and y >= -1e-6
        and x + width <= board.length_mm + 1e-6
        and y + height <= board.width_mm + 1e-6
    )


def swap_block_reason(
    project: StudioProject, first_id: str, second_id: str
) -> str | None:
    """Return a ``status.swap_*`` key, or ``None`` when the swap is valid."""
    if not first_id or not second_id or first_id == second_id:
        return "status.swap_need_two"

    first = project.placement_by_piece_id(first_id)
    second = project.placement_by_piece_id(second_id)
    if first is None or second is None:
        return "status.swap_need_placed"
    if not first.board_id or not second.board_id:
        return "status.swap_need_placed"

    try:
        first_piece = project.piece_by_id(first_id)
        second_piece = project.piece_by_id(second_id)
    except KeyError:
        return "status.swap_need_two"

    first_board = board_by_id(project, second.board_id)
    second_board = board_by_id(project, first.board_id)
    if first_board is None or second_board is None:
        return "status.swap_missing_board"

    if incompatibility_reason(first_piece, first_board) is not None:
        return "status.swap_incompatible"
    if incompatibility_reason(second_piece, second_board) is not None:
        return "status.swap_incompatible"

    first_w, first_h = placed_size(first_piece, first.rotation)
    second_w, second_h = placed_size(second_piece, second.rotation)
    if not _fits_board(first_board, second.x_mm, second.y_mm, first_w, first_h):
        return "status.swap_overflow"
    if not _fits_board(second_board, first.x_mm, first.y_mm, second_w, second_h):
        return "status.swap_overflow"

    first_rect = (second.x_mm, second.y_mm, first_w, first_h)
    second_rect = (first.x_mm, first.y_mm, second_w, second_h)
    if _rects_overlap(first_rect, second_rect) and same_physical_panel(first, second):
        return "status.swap_overlap"

    proposed = {
        first_id: (second, first_rect),
        second_id: (first, second_rect),
    }
    for seat, rect in proposed.values():
        for other in project.placements:
            if other.piece_id in proposed:
                continue
            if not (
                other.board_id == seat.board_id
                and other.board_instance == seat.board_instance
                and other.stock_panel_index == seat.stock_panel_index
            ):
                continue
            try:
                other_piece = project.piece_by_id(other.piece_id)
            except KeyError:
                continue
            ow, oh = placed_size(other_piece, other.rotation)
            if _rects_overlap(rect, (other.x_mm, other.y_mm, ow, oh)):
                return "status.swap_overlap"

    return None


def apply_swap(project: StudioProject, first_id: str, second_id: str) -> None:
    """Exchange seat fields; each piece keeps its own rotation."""
    first = project.placement_by_piece_id(first_id)
    second = project.placement_by_piece_id(second_id)
    if first is None or second is None:
        return
    (
        first.x_mm,
        first.y_mm,
        first.board_id,
        first.board_instance,
        first.stock_panel_index,
        second.x_mm,
        second.y_mm,
        second.board_id,
        second.board_instance,
        second.stock_panel_index,
    ) = (
        second.x_mm,
        second.y_mm,
        second.board_id,
        second.board_instance,
        second.stock_panel_index,
        first.x_mm,
        first.y_mm,
        first.board_id,
        first.board_instance,
        first.stock_panel_index,
    )
