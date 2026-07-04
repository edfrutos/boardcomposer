from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QGraphicsRectItem

from studio.workspace.board_piece_item import BoardPieceItem


def constrain_to_board(
    board: QGraphicsRectItem,
    item: BoardPieceItem,
    new_pos: QPointF,
) -> QPointF:
    board_rect = board.sceneBoundingRect()
    rect = item.rect()

    x = min(max(new_pos.x(), board_rect.left()),
            board_rect.right() - rect.width())
    y = min(max(new_pos.y(), board_rect.top()),
            board_rect.bottom() - rect.height())

    return QPointF(x, y)
