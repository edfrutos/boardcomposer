"""Helpers for unique Studio piece identifiers."""

from __future__ import annotations

from studio.unique_ids import allocate_unique_id


def allocate_unique_piece_id(base_id: str, existing_ids: set[str]) -> str:
    """Return ``base_id`` or ``base_id-2``, ``base_id-3``, … until free."""
    return allocate_unique_id(base_id, existing_ids)


def casefolded_piece_ids(project, *, strip: bool = False) -> set[str]:
    """Return casefolded piece ids currently in ``project``."""
    if strip:
        return {piece.piece_id.strip().casefold() for piece in project.pieces}
    return {piece.piece_id.casefold() for piece in project.pieces}
