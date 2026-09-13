"""Per-piece grain lock (IDE-0021). Locked pieces must not rotate."""

from __future__ import annotations

from typing import Any

GRAIN_NONE = "none"
GRAIN_LOCKED = "locked"
VALID_GRAINS = (GRAIN_NONE, GRAIN_LOCKED)


def normalize_grain(value: object) -> str:
    """Return ``none`` or ``locked``; unknown input becomes ``none``."""
    if isinstance(value, str):
        text = value.strip().casefold()
        if text in {GRAIN_LOCKED, "fixed", "lock", "veta"}:
            return GRAIN_LOCKED
        return GRAIN_NONE
    if value is True:
        return GRAIN_LOCKED
    return GRAIN_NONE


def grain_allows_rotation(grain: object) -> bool:
    """False when the piece grain is locked."""
    return normalize_grain(grain) == GRAIN_NONE


def rotation_allowed(board: Any, allow_rotation: bool) -> bool:
    """Project rotation AND piece grain both allow a 90° turn."""
    grain = getattr(board, "grain", GRAIN_NONE)
    return bool(allow_rotation) and grain_allows_rotation(grain)
