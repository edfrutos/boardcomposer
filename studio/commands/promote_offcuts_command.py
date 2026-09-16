"""Command for adding remnant boards from solution offcuts (IDE-0025)."""

from __future__ import annotations

from studio.board_ids import casefolded_board_ids
from studio.commands.command import Command
from studio.models import StudioBoard


class PromoteOffcutsCommand(Command):
    """Append remnant boards; undo removes exactly those boards."""

    name: str = "Añadir retales"

    def __init__(self, services, boards: list[StudioBoard] | tuple[StudioBoard, ...]):
        self.services = services
        self.boards = list(boards)
        self._board_ids = {board.board_id for board in self.boards}

    def redo(self) -> None:
        project = self.services.projects.current_project
        if project is None or not self.boards:
            return
        existing = casefolded_board_ids(project)
        for board in self.boards:
            if board.board_id.casefold() not in existing:
                project.boards.append(board)
                existing.add(board.board_id.casefold())

    def undo(self) -> None:
        project = self.services.projects.current_project
        if project is None or not self._board_ids:
            return
        project.boards = [
            board for board in project.boards if board.board_id not in self._board_ids
        ]
