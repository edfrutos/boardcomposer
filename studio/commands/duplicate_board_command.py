"""Command for duplicating a board in the project inventory."""

from __future__ import annotations

from studio.board_ids import casefolded_board_ids
from studio.commands.command import Command
from studio.models import StudioBoard


class DuplicateBoardCommand(Command):
    """Append a cloned board; undo removes the clone by id."""

    name: str = "Duplicar tablero"

    def __init__(self, services, board: StudioBoard):
        self.services = services
        self.board = board
        self._board_id = board.board_id

    def redo(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        existing = casefolded_board_ids(project)
        if self._board_id.casefold() not in existing:
            project.boards.append(self.board)

    def undo(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        project.boards = [
            board for board in project.boards if board.board_id != self._board_id
        ]
