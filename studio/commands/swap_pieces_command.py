"""Command for swapping two placed pieces (IDE-0019 / SCR-002)."""

from __future__ import annotations

from studio.commands.command import Command
from studio.events import catalog as events
from studio.swap_pieces import apply_swap


class SwapPiecesCommand(Command):
    """Exchange the seats of two placed pieces; undo swaps them back."""

    name: str = "Intercambiar piezas"

    def __init__(self, services, first_id: str, second_id: str) -> None:
        self.services = services
        self.first_id = first_id
        self.second_id = second_id

    def redo(self) -> None:
        self._swap()

    def undo(self) -> None:
        self._swap()

    def _swap(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        first = project.placement_by_piece_id(self.first_id)
        second = project.placement_by_piece_id(self.second_id)
        if first is None or second is None:
            return

        first_from = (
            first.x_mm,
            first.y_mm,
            first.board_id,
            first.board_instance,
            first.stock_panel_index,
        )
        second_from = (
            second.x_mm,
            second.y_mm,
            second.board_id,
            second.board_instance,
            second.stock_panel_index,
        )
        apply_swap(project, self.first_id, self.second_id)
        first = project.placement_by_piece_id(self.first_id)
        second = project.placement_by_piece_id(self.second_id)
        if first is None or second is None:
            return
        self._publish(self.first_id, first_from, first)
        self._publish(self.second_id, second_from, second)

    def _publish(self, piece_id: str, before: tuple, after) -> None:
        from_x, from_y, from_board, from_instance, from_index = before
        reassigned = (
            from_board != after.board_id
            or from_instance != after.board_instance
            or from_index != after.stock_panel_index
        )
        self.services.events.publish(
            events.PIECE_MOVED,
            {
                "piece": piece_id,
                "kind": "reassigned" if reassigned else "moved",
                "from_x": from_x,
                "from_y": from_y,
                "to_x": after.x_mm,
                "to_y": after.y_mm,
                "from_board": from_board,
                "to_board": after.board_id,
                "from_board_instance": from_instance,
                "to_board_instance": after.board_instance,
                "from_stock_panel_index": from_index,
                "to_stock_panel_index": after.stock_panel_index,
            },
        )
