"""Piece model for BoardComposer Studio."""

from dataclasses import dataclass

from boardcomposer.domain.grain import GRAIN_NONE, normalize_grain


@dataclass(frozen=True)
class StudioPiece:
    """Piece data used by the Studio workspace."""

    piece_id: str
    length_mm: float
    width_mm: float
    material: str = "Demo"
    thickness_mm: float = 19
    grain: str = GRAIN_NONE

    def __post_init__(self) -> None:
        object.__setattr__(self, "grain", normalize_grain(self.grain))
