from studio.workspace.board_piece_item import BoardPieceItem


def create_piece_item(
    piece,
    placement,
    *,
    offset_x: float = 0,
    offset_y: float = 0,
) -> BoardPieceItem:
    item = BoardPieceItem(
        piece.piece_id,
        placement.x_mm + offset_x,
        placement.y_mm + offset_y,
        piece.length_mm,
        piece.width_mm,
        board_id=placement.board_id,
        board_instance=placement.board_instance,
        stock_panel_index=placement.stock_panel_index,
    )
    item.set_rotation(placement.rotation)
    return item
