from studio.workspace.board_piece_item import BoardPieceItem


def collides(item: BoardPieceItem) -> bool:
    for other in item.collidingItems():
        if isinstance(other, BoardPieceItem):
            return True
    return False
