from PySide6.QtWidgets import QGraphicsRectItem

from studio.models import StudioBoard
from studio.workspace.canvas_style import color, pen


def create_board_item(board_model: StudioBoard) -> QGraphicsRectItem:
    board = QGraphicsRectItem(
        0,
        0,
        board_model.length_mm,
        board_model.width_mm,
    )
    board.setBrush(color("board_fill"))
    board.setPen(pen("board_stroke", 4))
    return board
