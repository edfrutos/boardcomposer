"""Command to place an unplaced piece onto a physical panel."""

from __future__ import annotations

from studio.commands.command import Command
from studio.models import StudioPlacement


class PlacePieceCommand(Command):
    """Create a placement for a piece that is not yet on any panel."""

    name: str = "Colocar pieza"

    def __init__(self, services, placement: StudioPlacement) -> None:
        self.services = services
        self.placement = placement

    def redo(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        if project.placement_by_piece_id(self.placement.piece_id) is not None:
            return
        project.placements.append(self.placement)

    def undo(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        project.placements = [
            placement
            for placement in project.placements
            if placement.piece_id != self.placement.piece_id
        ]
