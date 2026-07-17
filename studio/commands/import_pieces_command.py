"""Command for importing pieces (and placements) from CSV/Excel (FLW-002)."""

from __future__ import annotations

from studio.commands.command import Command
from studio.models import StudioPiece, StudioPlacement


class ImportPiecesCommand(Command):
    """Append imported pieces and placements; undo removes them by id."""

    name: str = "Importar piezas"

    def __init__(
        self,
        services,
        pieces: list[StudioPiece] | tuple[StudioPiece, ...],
        placements: list[StudioPlacement] | tuple[StudioPlacement, ...],
    ):
        self.services = services
        self.pieces = list(pieces)
        self.placements = list(placements)
        self._piece_ids = {piece.piece_id for piece in self.pieces}

    def redo(self) -> None:
        project = self.services.projects.current_project
        if project is None or not self.pieces:
            return
        existing = {piece.piece_id.casefold() for piece in project.pieces}
        for piece in self.pieces:
            if piece.piece_id.casefold() not in existing:
                project.pieces.append(piece)
                existing.add(piece.piece_id.casefold())
        placed = {placement.piece_id for placement in project.placements}
        for placement in self.placements:
            if placement.piece_id not in placed:
                project.placements.append(placement)
                placed.add(placement.piece_id)

    def undo(self) -> None:
        project = self.services.projects.current_project
        if project is None or not self._piece_ids:
            return
        project.pieces = [
            piece for piece in project.pieces if piece.piece_id not in self._piece_ids
        ]
        project.placements = [
            placement
            for placement in project.placements
            if placement.piece_id not in self._piece_ids
        ]
