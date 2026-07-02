"""Command protocol for BoardComposer Studio."""

from typing import Protocol


class Command(Protocol):
    """Executable Studio command."""

    name: str

    def execute(self) -> None:
        """Execute the command."""

    def undo(self) -> None:
        """Undo the command."""
