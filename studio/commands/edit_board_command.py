"""Command for editing a Studio board (FLW-006)."""

from __future__ import annotations

from studio.commands.command import Command
from studio.models import StudioBoard


class EditBoardCommand(Command):
    """Replace a board and update placements that reference it."""

    name: str = "Editar tablero"

    def __init__(self, services, old_board: StudioBoard, new_board: StudioBoard):
        self.services = services
        self.old_board = old_board
        self.new_board = new_board
        self._placement_instances: list[tuple[str, int]] | None = None

    def redo(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        if self._placement_instances is None:
            self._placement_instances = [
                (placement.piece_id, placement.board_instance)
                for placement in project.placements
                if placement.board_id == self.old_board.board_id
            ]
        self._apply(self.old_board, self.new_board)

    def undo(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        self._apply(self.new_board, self.old_board)
        if not self._placement_instances:
            return
        restored = dict(self._placement_instances)
        for placement in project.placements:
            if (
                placement.board_id == self.old_board.board_id
                and placement.piece_id in restored
            ):
                placement.board_instance = restored[placement.piece_id]

    def _apply(self, from_board: StudioBoard, to_board: StudioBoard) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        from_id = from_board.board_id
        for index, existing in enumerate(project.boards):
            if existing.board_id == from_id:
                project.boards[index] = to_board
                break
        else:
            return
        max_instance = max(to_board.quantity - 1, 0)
        for placement in project.placements:
            if placement.board_id == from_id:
                placement.board_id = to_board.board_id
                placement.board_instance = min(placement.board_instance, max_instance)
