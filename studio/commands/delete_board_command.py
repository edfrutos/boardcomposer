"""Command for deleting a board and its placements (pieces remain)."""

from __future__ import annotations

from studio.commands.command import Command
from studio.models import StudioBoard, StudioPlacement


class DeleteBoardCommand(Command):
    """Remove a board; detach placements that referenced it (keep pieces)."""

    name: str = "Eliminar tablero"

    def __init__(self, services, board_id: str):
        self.services = services
        self.board_id = board_id
        self._board: StudioBoard | None = None
        self._board_index: int | None = None
        self._placements: list[tuple[int, StudioPlacement]] = []

    def redo(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return

        if self._board is None:
            for index, board in enumerate(project.boards):
                if board.board_id == self.board_id:
                    self._board = board
                    self._board_index = index
                    break
            if self._board is None:
                return
            self._placements = [
                (index, placement)
                for index, placement in enumerate(project.placements)
                if placement.board_id == self.board_id
            ]

        assert self._board is not None
        if self._board in project.boards:
            project.boards.remove(self._board)
        kept = [
            placement
            for placement in project.placements
            if placement.board_id != self.board_id
        ]
        project.placements = kept

    def undo(self) -> None:
        project = self.services.projects.current_project
        if project is None or self._board is None:
            return

        index = (
            self._board_index if self._board_index is not None else len(project.boards)
        )
        project.boards.insert(index, self._board)

        # Re-insert removed placements at original indices (ascending).
        for placement_index, placement in sorted(
            self._placements, key=lambda item: item[0]
        ):
            insert_at = min(placement_index, len(project.placements))
            if placement not in project.placements:
                project.placements.insert(insert_at, placement)
