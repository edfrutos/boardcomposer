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
    ShortcutBinding("rename_selection", "F2"),
    ShortcutBinding("edit_selection", "Return"),
    ShortcutBinding("copy_selection_id", "Ctrl+Shift+C"),
    ShortcutBinding("duplicate_piece", "Ctrl+D"),
    ShortcutBinding("delete_piece", "Backspace", ("Delete",)),
    ShortcutBinding("select_all_pieces", "Ctrl+A"),
    ShortcutBinding("deselect_pieces", "Escape"),
    ShortcutBinding("invert_selection", "Ctrl+Shift+I"),
    ShortcutBinding("preferences", "Ctrl+,"),
    ShortcutBinding("solve_layout", "Ctrl+Return"),
    ShortcutBinding("previous_solution", "PgUp"),
    ShortcutBinding("next_solution", "PgDown"),
    ShortcutBinding("apply_layout", "Ctrl+Shift+Return"),
    ShortcutBinding("export_selected", "Ctrl+Shift+E"),
    ShortcutBinding("add_piece", "Ctrl+Shift+P"),
    ShortcutBinding("add_board", "Ctrl+Shift+B"),
    ShortcutBinding("import_pieces_csv", "Ctrl+Shift+O"),
    ShortcutBinding("import_boards_csv", "Ctrl+Shift+T"),
    ShortcutBinding("export_timeline", "Ctrl+Shift+L"),
    ShortcutBinding("show_welcome", "Ctrl+Shift+H"),
    ShortcutBinding("reveal_project_folder", "Ctrl+Shift+R"),
    ShortcutBinding("shortcuts", "F1"),
    ShortcutBinding("reset_window_layout", "Ctrl+Shift+W"),
    ShortcutBinding("new_from_template", "Ctrl+Shift+N"),
    ShortcutBinding("save_as_template", "Ctrl+Shift+M"),
    ShortcutBinding("whats_new", "Ctrl+Shift+U"),
    ShortcutBinding("new_demo_project", "Ctrl+Shift+D"),
    ShortcutBinding("open_docs", "Shift+F1"),
    ShortcutBinding("about", "Ctrl+Shift+A"),
    ShortcutBinding("rename_project", "Ctrl+Shift+F2"),
    ShortcutBinding("exit", "Ctrl+Q"),
    ShortcutBinding("clear_recent", "Ctrl+Shift+X"),
    ShortcutBinding("toggle_toolbar", "Ctrl+Shift+K"),
    ShortcutBinding("toggle_explorer", "Ctrl+1"),
    ShortcutBinding("toggle_inspector", "Ctrl+2"),
    ShortcutBinding("fit_board", "Ctrl+0"),
    ShortcutBinding("fit_selection", "Ctrl+Shift+0"),
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
