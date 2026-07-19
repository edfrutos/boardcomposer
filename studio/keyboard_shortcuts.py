"""Central keyboard shortcut bindings for BoardComposer Studio."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtGui import QAction, QKeySequence


@dataclass(frozen=True)
class ShortcutBinding:
    """Maps a main-window action key to a keyboard sequence."""

    action_key: str
    sequence: str
    alternates: tuple[str, ...] = ()


STUDIO_SHORTCUTS: tuple[ShortcutBinding, ...] = (
    ShortcutBinding("new_project", "Ctrl+N"),
    ShortcutBinding("open", "Ctrl+O"),
    ShortcutBinding("save", "Ctrl+S"),
    ShortcutBinding("save_as", "Ctrl+Shift+S"),
    ShortcutBinding("undo", "Ctrl+Z"),
    ShortcutBinding("redo", "Ctrl+Shift+Z"),
    ShortcutBinding("rotate_piece", "R"),
    ShortcutBinding("duplicate_piece", "Ctrl+D"),
    ShortcutBinding("delete_piece", "Backspace", ("Delete",)),
    ShortcutBinding("select_all_pieces", "Ctrl+A"),
    ShortcutBinding("deselect_pieces", "Escape"),
    ShortcutBinding("invert_selection", "Ctrl+Shift+I"),
    ShortcutBinding("preferences", "Ctrl+,"),
    ShortcutBinding("solve_layout", "Ctrl+Return"),
    ShortcutBinding("fit_board", "Ctrl+0"),
    ShortcutBinding("zoom_in", "Ctrl+=", ("Ctrl++",)),
    ShortcutBinding("zoom_out", "Ctrl+-"),
    ShortcutBinding("toggle_grid", "Ctrl+G"),
)


def format_shortcut_label(binding: ShortcutBinding) -> str:
    """Human-readable shortcut list including alternates."""
    if not binding.alternates:
        return binding.sequence
    return ", ".join((binding.sequence, *binding.alternates))


def apply_shortcuts(actions: dict[str, QAction]) -> None:
    """Assign configured shortcuts to existing QAction instances."""
    for binding in STUDIO_SHORTCUTS:
        action = actions.get(binding.action_key)
        if action is None:
            continue
        if binding.alternates:
            action.setShortcuts(
                [QKeySequence(binding.sequence)]
                + [QKeySequence(alt) for alt in binding.alternates]
            )
        else:
            action.setShortcut(binding.sequence)
