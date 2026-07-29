"""Helpers for unique Studio board identifiers."""

from __future__ import annotations

from studio.unique_ids import allocate_unique_id


def allocate_unique_board_id(base_id: str, existing_ids: set[str]) -> str:
    """Return ``base_id`` or ``base_id-2``, ``base_id-3``, … until free."""
    return allocate_unique_id(base_id, existing_ids)
