from dataclasses import dataclass, field


@dataclass(frozen=True)
class Board:
    length_mm: float
    width_mm: float
    thickness_mm: float
    id: str | None = None

    def __post_init__(self) -> None:
        if self.length_mm <= 0:
            raise ValueError("length_mm debe ser mayor que 0")
        if self.width_mm <= 0:
            raise ValueError("width_mm debe ser mayor que 0")
        if self.thickness_mm <= 0:
            raise ValueError("thickness_mm debe ser mayor que 0")

    @property
    def area_mm2(self) -> float:
        return self.length_mm * self.width_mm


@dataclass
class Project:
    boards: list[Board] = field(default_factory=list)

    def add_board(self, board: Board) -> None:
        self.boards.append(board)

    @property
    def total_area_mm2(self) -> float:
        return sum(board.area_mm2 for board in self.boards)
