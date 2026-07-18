"""Command for editing a Studio piece (FLW-006)."""

from __future__ import annotations

from studio.commands.command import Command
from studio.models import StudioPiece


class EditPieceCommand(Command):
    """Replace a piece (and rename its placement if the id changes)."""

    name: str = "Editar pieza"

    def __init__(self, services, old_piece: StudioPiece, new_piece: StudioPiece):
        self.services = services
        self.old_piece = old_piece
        self.new_piece = new_piece

    def redo(self) -> None:
        self._apply(self.old_piece.piece_id, self.new_piece)

    def undo(self) -> None:
        self._apply(self.new_piece.piece_id, self.old_piece)

    def _apply(self, from_id: str, piece: StudioPiece) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        for index, existing in enumerate(project.pieces):
            if existing.piece_id == from_id:
                project.pieces[index] = piece
                break
        else:
            return
        for placement in project.placements:
            if placement.piece_id == from_id:
                placement.piece_id = piece.piece_id
