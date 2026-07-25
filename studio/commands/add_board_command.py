"""Command for adding a board to the project inventory (FLW-006)."""

from __future__ import annotations

from studio.commands.command import Command
from studio.models import StudioBoard


class AddBoardCommand(Command):
    """Append one board; undo removes it by id."""

    name: str = "Añadir tablero"

    def __init__(self, services, board: StudioBoard):
        self.services = services
        self.board = board
        self._board_id = board.board_id

    def redo(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        existing = {board.board_id.casefold() for board in project.boards}
        if self._board_id.casefold() not in existing:
            project.boards.append(self.board)

    def undo(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        project.boards = [
            board for board in project.boards if board.board_id != self._board_id
        ]
