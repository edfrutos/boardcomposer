"""Command for duplicating a piece and its placement."""

from __future__ import annotations

from studio.commands.command import Command
from studio.models import StudioPiece, StudioPlacement


class DuplicatePieceCommand(Command):
    """Append a cloned piece/placement; undo removes the clone by id."""

    name: str = "Duplicar pieza"

    def __init__(
        self,
        services,
        piece: StudioPiece,
        placement: StudioPlacement,
    ):
        self.services = services
        self.piece = piece
        self.placement = placement
        self._piece_id = piece.piece_id

    def redo(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        existing = {piece.piece_id.casefold() for piece in project.pieces}
        if self._piece_id.casefold() not in existing:
            project.pieces.append(self.piece)
        placed = {placement.piece_id for placement in project.placements}
        if self.placement.piece_id not in placed:
            project.placements.append(self.placement)

    def undo(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        project.pieces = [
            piece for piece in project.pieces if piece.piece_id != self._piece_id
        ]
        project.placements = [
            placement
            for placement in project.placements
            if placement.piece_id != self._piece_id
        ]
