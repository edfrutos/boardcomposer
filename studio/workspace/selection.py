from studio.workspace.board_piece_item import BoardPieceItem
from studio.workspace.canvas_style import color, pen


def apply_selection(item: BoardPieceItem, selected: bool) -> None:
    item.setSelected(selected)

    if selected:
        item.setBrush(color("selected_fill"))
        item.setPen(pen("selected_stroke", 10))
    else:
        item.setBrush(color("piece_fill"))
        item.setPen(pen("piece_stroke", 3))
