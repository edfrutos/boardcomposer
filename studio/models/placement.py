"""Placement model for BoardComposer Studio."""

from dataclasses import dataclass


@dataclass
class StudioPlacement:
    """Placement data for a piece inside a board."""

    piece_id: str
    x_mm: float
    y_mm: float
    rotated: bool = False
    rotation: int = 0
    board_id: str | None = None
    board_instance: int = 0
    stock_panel_index: int | None = None
