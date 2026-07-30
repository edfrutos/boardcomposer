"""Command for moving a piece, possibly to another physical panel."""

from typing import TYPE_CHECKING

from studio.commands.command import Command
from studio.events import catalog as events

if TYPE_CHECKING:
    from studio.services import StudioServices


class MovePieceCommand(Command):
    """Move a piece between two positions and, if applicable, panels."""

    name: str = "Mover pieza"

    def __init__(
        self,
        services: "StudioServices",
        piece_id: str,
        old_x: float,
        old_y: float,
        new_x: float,
        new_y: float,
        *,
        old_board_id: str | None = None,
        old_board_instance: int = 0,
        old_stock_panel_index: int | None = None,
        new_board_id: str | None = None,
        new_board_instance: int = 0,
        new_stock_panel_index: int | None = None,
    ) -> None:
        self.services = services
        self.piece_id = piece_id
        self.old_x = old_x
        self.old_y = old_y
        self.new_x = new_x
        self.new_y = new_y
        self.old_board_id = old_board_id
        self.old_board_instance = old_board_instance
        self.old_stock_panel_index = old_stock_panel_index
        self.new_board_id = new_board_id
        self.new_board_instance = new_board_instance
        self.new_stock_panel_index = new_stock_panel_index

    def redo(self) -> None:
        self._move_to(
            self.new_x,
            self.new_y,
            self.new_board_id,
            self.new_board_instance,
            self.new_stock_panel_index,
            from_x=self.old_x,
            from_y=self.old_y,
            from_board_id=self.old_board_id,
            from_board_instance=self.old_board_instance,
            from_stock_panel_index=self.old_stock_panel_index,
        )

    def undo(self) -> None:
        self._move_to(
            self.old_x,
            self.old_y,
            self.old_board_id,
            self.old_board_instance,
            self.old_stock_panel_index,
            from_x=self.new_x,
            from_y=self.new_y,
            from_board_id=self.new_board_id,
            from_board_instance=self.new_board_instance,
            from_stock_panel_index=self.new_stock_panel_index,
        )

    def _move_to(
        self,
        x: float,
        y: float,
        board_id: str | None,
        board_instance: int,
        stock_panel_index: int | None,
        *,
        from_x: float,
        from_y: float,
        from_board_id: str | None,
        from_board_instance: int,
        from_stock_panel_index: int | None,
    ) -> None:
        project = self.services.projects.current_project
        if project is None:
            return

        placement = project.placement_by_piece_id(self.piece_id)
        if placement is None:
            return

        placement.x_mm = x
        placement.y_mm = y
        placement.board_id = board_id
        placement.board_instance = board_instance
        placement.stock_panel_index = stock_panel_index

        self.services.events.publish(
            events.PIECE_MOVED,
            {
                "piece": self.piece_id,
                "kind": (
                    "reassigned"
                    if (
                        from_board_id != board_id
                        or from_board_instance != board_instance
                        or from_stock_panel_index != stock_panel_index
                    )
                    else "moved"
                ),
                "from_x": from_x,
                "from_y": from_y,
                "to_x": x,
                "to_y": y,
                "from_board": from_board_id,
                "to_board": board_id,
                "from_board_instance": from_board_instance,
                "to_board_instance": board_instance,
                "from_stock_panel_index": from_stock_panel_index,
                "to_stock_panel_index": stock_panel_index,
            },
        )
