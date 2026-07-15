from dataclasses import dataclass, field

from .board import Board
from .constraints import ProjectConstraints
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

    @property
    def total_area_mm2(self) -> float:
        return sum(board.area_mm2 for board in self.boards)
