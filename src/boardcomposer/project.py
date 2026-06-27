from dataclasses import dataclass, field

from .board import Board


@dataclass
class Project:
    boards: list[Board] = field(default_factory=list)

    def add_board(self, board: Board) -> None:
        self.boards.append(board)

    @property
    def total_area_mm2(self) -> float:
        return sum(board.area_mm2 for board in self.boards)
