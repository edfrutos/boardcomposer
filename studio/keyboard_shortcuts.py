"""Central keyboard shortcut bindings for BoardComposer Studio."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtGui import QAction


@dataclass(frozen=True)
class ShortcutBinding:
    """Maps a main-window action key to a keyboard sequence."""

    action_key: str
    sequence: str


STUDIO_SHORTCUTS: tuple[ShortcutBinding, ...] = (
    ShortcutBinding("new_project", "Ctrl+N"),
    ShortcutBinding("open", "Ctrl+O"),
    ShortcutBinding("save", "Ctrl+S"),
    ShortcutBinding("save_as", "Ctrl+Shift+S"),
    ShortcutBinding("undo", "Ctrl+Z"),
    ShortcutBinding("redo", "Ctrl+Shift+Z"),
    ShortcutBinding("rotate_piece", "R"),
    ShortcutBinding("duplicate_piece", "Ctrl+D"),
    ShortcutBinding("delete_piece", "Backspace"),
    ShortcutBinding("preferences", "Ctrl+,"),
    ShortcutBinding("solve_layout", "Ctrl+Return"),
)


def apply_shortcuts(actions: dict[str, QAction]) -> None:
    """Assign configured shortcuts to existing QAction instances."""
    for binding in STUDIO_SHORTCUTS:
        action = actions.get(binding.action_key)
        if action is not None:
            action.setShortcut(binding.sequence)
