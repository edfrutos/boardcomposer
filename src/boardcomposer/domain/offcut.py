"""Leftover rectangular area on a consumed physical panel.

Purely informational for now (see ADR-016): a solution reports the usable
offcuts left on each panel it consumed, but they are not yet persisted as
reusable `StockPanel` inventory for future projects.
"""

from dataclasses import dataclass

from .panel_reference import PanelReference


@dataclass(frozen=True)
class Offcut:
    """A rectangular region of a consumed panel left unused by any piece."""

    panel_reference: PanelReference
    x_mm: float
    y_mm: float
    length_mm: float
    width_mm: float

    def __post_init__(self) -> None:
        if self.x_mm < 0:
            raise ValueError("x_mm no puede ser negativo")
        if self.y_mm < 0:
            raise ValueError("y_mm no puede ser negativo")
        if self.length_mm <= 0:
            raise ValueError("length_mm debe ser mayor que 0")
        if self.width_mm <= 0:
            raise ValueError("width_mm debe ser mayor que 0")

    @property
    def area_mm2(self) -> float:
        return self.length_mm * self.width_mm
