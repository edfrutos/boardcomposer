"""
StockPanel is a domain entity that represents a panel of stock.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class StockPanel:
    """
    StockPanel is a domain entity that represents a panel of stock.
    """

    length_mm: float
    width_mm: float
    thickness_mm: float
    id: str | None = None
    quantity: int = 1
    material: str = "Generico"

    def __post_init__(self) -> None:
        if self.length_mm <= 0:
            raise ValueError("length_mm debe ser mayor que 0")
        if self.width_mm <= 0:
            raise ValueError("width_mm debe ser mayor que 0")
        if self.thickness_mm <= 0:
            raise ValueError("thickness_mm debe ser mayor que 0")
        if self.quantity <= 0:
            raise ValueError("quantity debe ser mayor que 0")

    @property
    def area_mm2(self) -> float:
        """
        Area of the panel in square millimeters.
        """
        return self.length_mm * self.width_mm

    @property
    def material_key(self) -> str:
        """Normalized material for case/whitespace-insensitive comparisons."""
        return self.material.strip().casefold()
