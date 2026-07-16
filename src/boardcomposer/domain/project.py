from dataclasses import dataclass, field

from .board import Board
from .constraints import ProjectConstraints
from .panel_reference import PanelReference
from .stock_panel import StockPanel


@dataclass
class Project:
    boards: list[Board] = field(default_factory=list)
    stock_panels: list[StockPanel] = field(default_factory=list)
    constraints: ProjectConstraints = field(default_factory=ProjectConstraints)

    def add_board(self, board: Board) -> None:
        self.boards.append(board)

    def add_stock_panel(self, panel: StockPanel) -> None:
        self.stock_panels.append(panel)

    def stock_panel_instances(
        self,
    ) -> tuple[tuple[PanelReference, StockPanel], ...]:
        """Return every available physical panel in deterministic order."""
        return tuple(
            (
                PanelReference(
                    stock_panel_index=stock_panel_index,
                    instance_index=instance_index,
                ),
                panel,
            )
            for stock_panel_index, panel in enumerate(self.stock_panels)
            for instance_index in range(panel.quantity)
        )

    def stock_panel_for(self, reference: PanelReference) -> StockPanel | None:
        """Resolve a physical panel reference against this project."""
        if reference.stock_panel_index >= len(self.stock_panels):
            return None

        panel = self.stock_panels[reference.stock_panel_index]
        if reference.instance_index >= panel.quantity:
            return None

        return panel

    @property
    def total_area_mm2(self) -> float:
        return sum(board.area_mm2 for board in self.boards)
