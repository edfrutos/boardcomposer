"""Command manager for BoardComposer Studio."""

from dataclasses import dataclass, field

from studio.commands.command import Command


@dataclass
class CommandManager:
    """Executes commands and tracks undo/redo stacks."""

    _undo_stack: list[Command] = field(default_factory=list)
    _redo_stack: list[Command] = field(default_factory=list)

    @property
    def can_undo(self) -> bool:
        return bool(self._undo_stack)

    @property
    def can_redo(self) -> bool:
        return bool(self._redo_stack)

    def execute(self, command: Command) -> None:
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self) -> None:
        if not self._undo_stack:
            return

        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)

    def redo(self) -> None:
        if not self._redo_stack:
            return

        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)
