"""Piece ↔ stock-panel compatibility helpers (material + thickness)."""

from __future__ import annotations

from math import isclose

from studio.models import StudioBoard, StudioPiece


def material_key(value: str | None) -> str:
    return (value or "").strip().casefold()


def piece_compatible_with_board(piece: StudioPiece, board: StudioBoard) -> bool:
    """Match Core solver rules: same thickness and material key."""
    return isclose(piece.thickness_mm, board.thickness_mm) and (
        material_key(piece.material) == material_key(board.material)
    )


def incompatibility_reason(piece: StudioPiece, board: StudioBoard) -> str | None:
    """Return a short machine key, or None when compatible."""
    thickness_ok = isclose(piece.thickness_mm, board.thickness_mm)
    material_ok = material_key(piece.material) == material_key(board.material)
    if thickness_ok and material_ok:
        return None
    if not thickness_ok and not material_ok:
        return "both"
    if not thickness_ok:
        return "thickness"
    return "material"
