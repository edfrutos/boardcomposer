from __future__ import annotations

from PySide6 import QtCore

from studio.workspace.board_piece_item import BoardPieceItem


class PlacementValidator:
    """Única fuente de verdad para validar colocaciones."""

    def __init__(self, board_rect: QtCore.QRectF):
        self.board_rect = board_rect

    def constrain_position(
        self,
        item: BoardPieceItem,
        new_pos: QtCore.QPointF,
    ) -> QtCore.QPointF:
        rect = item.rect()

        x = min(
            max(new_pos.x(), self.board_rect.left()),
            self.board_rect.right() - rect.width(),
        )
        y = min(
            max(new_pos.y(), self.board_rect.top()),
            self.board_rect.bottom() - rect.height(),
        )

        return QtCore.QPointF(x, y)

    def collides(self, item: BoardPieceItem) -> bool:
        for other in item.collidingItems():
            if isinstance(other, BoardPieceItem):
                return True
        return False

    def can_place(self, item: BoardPieceItem) -> bool:
        return (
            self.board_rect.contains(item.sceneBoundingRect())
            and not self.collides(item)
        )
