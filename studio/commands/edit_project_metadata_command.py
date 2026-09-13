"""Command for editing Studio project metadata (IDE-0024 / SCR-005)."""

from __future__ import annotations

from studio.commands.command import Command


class EditProjectMetadataCommand(Command):
    """Replace client / reference / notes; undo restores the previous values."""

    name: str = "Editar metadatos del proyecto"

    def __init__(
        self,
        services,
        *,
        old_client: str,
        old_reference: str,
        old_notes: str,
        new_client: str,
        new_reference: str,
        new_notes: str,
    ) -> None:
        self.services = services
        self.old_client = old_client
        self.old_reference = old_reference
        self.old_notes = old_notes
        self.new_client = new_client
        self.new_reference = new_reference
        self.new_notes = new_notes

    def redo(self) -> None:
        self._apply(self.new_client, self.new_reference, self.new_notes)

    def undo(self) -> None:
        self._apply(self.old_client, self.old_reference, self.old_notes)

    def _apply(self, client: str, reference: str, notes: str) -> None:
        project = self.services.projects.current_project
        if project is None:
            return
        project.client = client
        project.reference = reference
        project.notes = notes
