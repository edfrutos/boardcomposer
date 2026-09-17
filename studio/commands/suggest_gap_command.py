"""Undoable snap of a piece to a suggested gap (IDE-0036)."""

from __future__ import annotations

from studio.commands.command import Command
from studio.models import StudioPlacement


def clone_placement(placement: StudioPlacement) -> StudioPlacement:
    """Copy placement fields so undo snapshots stay independent."""
    return StudioPlacement(
        piece_id=placement.piece_id,
        x_mm=placement.x_mm,
        y_mm=placement.y_mm,
        rotated=placement.rotated,
        rotation=placement.rotation,
        board_id=placement.board_id,
        board_instance=placement.board_instance,
        stock_panel_index=placement.stock_panel_index,
    )


class SuggestGapCommand(Command):
    """Place or move a piece onto a suggested origin (one undo)."""

    name: str = "Sugerir hueco"

    def __init__(
        self,
        services,
        piece_id: str,
        old: StudioPlacement | None,
        new: StudioPlacement,
    ) -> None:
        self.services = services
        self.piece_id = piece_id
        self.old = None if old is None else clone_placement(old)
        self.new = clone_placement(new)

    def redo(self) -> None:
        self._apply(self.new)

    def undo(self) -> None:
        self._apply(self.old)

    def _apply(self, target: StudioPlacement | None) -> None:
        project = self.services.projects.current_project
        if project is None:
            return

        current = project.placement_by_piece_id(self.piece_id)
        if target is None:
            project.placements = [
                placement
                for placement in project.placements
                if placement.piece_id != self.piece_id
            ]
            return

        if current is None:
            project.placements.append(clone_placement(target))
            return

        current.x_mm = target.x_mm
        current.y_mm = target.y_mm
        current.rotated = target.rotated
        current.rotation = target.rotation
        current.board_id = target.board_id
        current.board_instance = target.board_instance
        current.stock_panel_index = target.stock_panel_index
