class DragController:
    """Tracks the pre-drag position and physical panel of a piece."""

    def __init__(self):
        self.drag_start = None

    def begin(
        self,
        piece_id,
        x,
        y,
        board_id=None,
        board_instance=0,
        stock_panel_index=None,
    ):
        self.drag_start = (
            piece_id,
            x,
            y,
            board_id,
            board_instance,
            stock_panel_index,
        )

    def clear(self):
        value = self.drag_start
        self.drag_start = None
        return value
