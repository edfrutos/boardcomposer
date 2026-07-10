"""Command for moving a piece."""

from typing import TYPE_CHECKING

from studio.commands.command import Command

if TYPE_CHECKING:
    from studio.services import StudioServices


class MovePieceCommand(Command):
    """Move a piece between two positions."""

    name: str = "Mover pieza"

    def __init__(
        self,
        services: "StudioServices",
        piece_id: str,
        old_x: float,
        old_y: float,
        new_x: float,
        new_y: float,
    ) -> None:
        self.services = services
        self.piece_id = piece_id
        self.old_x = old_x
        self.old_y = old_y
        self.new_x = new_x
        self.new_y = new_y

    def redo(self) -> None:
        self._move_to(self.new_x, self.new_y)

    def undo(self) -> None:
        self._move_to(self.old_x, self.old_y)

    def _move_to(self, x: float, y: float) -> None:
        project = self.services.projects.current_project
        if project is None:
            return

        placement = project.placement_by_piece_id(self.piece_id)
        if placement is None:
            return

        placement.x_mm = x
        placement.y_mm = y
