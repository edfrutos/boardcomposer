"""Command for renaming the current Studio project (FLW-006 / SCR-005)."""

from __future__ import annotations

from studio.commands.command import Command


class RenameProjectCommand(Command):
    """Change ``StudioProject.name``; undo restores the previous name."""

    name: str = "Renombrar proyecto"

    def __init__(self, services, old_name: str, new_name: str):
        self.services = services
        self.old_name = old_name
        self.new_name = new_name

    def redo(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        project.name = self.new_name

    def undo(self) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        project.name = self.old_name
