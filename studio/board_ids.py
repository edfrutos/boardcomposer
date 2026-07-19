"""Helpers for unique Studio board identifiers."""

from __future__ import annotations


def allocate_unique_board_id(base_id: str, existing_ids: set[str]) -> str:
    """Return ``base_id`` or ``base_id-2``, ``base_id-3``, … until free."""
    if base_id.casefold() not in existing_ids:
        return base_id
    suffix = 2
    while True:
        candidate = f"{base_id}-{suffix}"
        if candidate.casefold() not in existing_ids:
            return candidate
        suffix += 1
