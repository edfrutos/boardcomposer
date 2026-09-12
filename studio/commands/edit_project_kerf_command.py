"""Command for editing project saw kerf (IDE-0020)."""

from __future__ import annotations

from studio.commands.command import Command


class EditProjectKerfCommand(Command):
    """Replace ``kerf_mm``; undo restores the previous value."""

    name: str = "Editar espesor de sierra"

    def __init__(self, services, old_kerf_mm: float, new_kerf_mm: float) -> None:
        self.services = services
        self.old_kerf_mm = old_kerf_mm
        self.new_kerf_mm = new_kerf_mm

    def redo(self) -> None:
        self._apply(self.new_kerf_mm)

    def undo(self) -> None:
        self._apply(self.old_kerf_mm)

    def _apply(self, kerf_mm: float) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        project.kerf_mm = kerf_mm
