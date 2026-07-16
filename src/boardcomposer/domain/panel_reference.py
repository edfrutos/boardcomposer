"""Reference to one physical stock-panel instance."""

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class PanelReference:
    """Identify a panel type and one unit from its available quantity."""

    stock_panel_index: int
    instance_index: int

    def __post_init__(self) -> None:
        if self.stock_panel_index < 0:
            raise ValueError("stock_panel_index no puede ser negativo")
        if self.instance_index < 0:
            raise ValueError("instance_index no puede ser negativo")
