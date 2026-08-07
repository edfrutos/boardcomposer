"""Central keyboard shortcut bindings for BoardComposer Studio.

Portable sequences use Qt's ``Ctrl+…`` notation. On macOS Qt maps that
modifier to the Command key (⌘), not the physical Control key (⌃). UI
labels should always go through ``format_shortcut_label`` /
``with_native_shortcuts`` so Mac users see ⌘.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt
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
    ShortcutBinding("diff_bcproj", "Ctrl+Shift+Y"),
    ShortcutBinding("restore_local_revision", "Ctrl+Alt+Y"),
    ShortcutBinding("export_revision_backup", "Ctrl+Alt+B"),
    ShortcutBinding("explain_solution", "Ctrl+Alt+E"),
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
    ShortcutBinding("toggle_timeline", "Ctrl+3"),
    ShortcutBinding("toggle_comparator", "Ctrl+4"),
    ShortcutBinding("fit_board", "Ctrl+0"),
    ShortcutBinding("fit_selection", "Ctrl+Shift+0"),
    ShortcutBinding("zoom_in", "Ctrl+=", ("Ctrl++",)),
    ShortcutBinding("zoom_out", "Ctrl+-"),
    ShortcutBinding("toggle_grid", "Ctrl+G"),
)

# Display-only rows for F1 / docs. Not applied via apply_shortcuts (list-focused).
CONTEXTUAL_SHORTCUTS: tuple[ShortcutBinding, ...] = (
    ShortcutBinding("timeline_replay_play", "Space"),
    ShortcutBinding("timeline_replay_reset", "Home"),
    ShortcutBinding("timeline_replay_back", "Left"),
    ShortcutBinding("timeline_replay_forward", "Right"),
)


def all_shortcut_rows() -> tuple[ShortcutBinding, ...]:
    """Global menu shortcuts plus contextual Timeline replay rows for F1."""
    return STUDIO_SHORTCUTS + CONTEXTUAL_SHORTCUTS


def native_sequence_label(sequence: str) -> str:
    """Platform-native label for a portable shortcut (⌘N on macOS)."""
    return QKeySequence(sequence).toString(QKeySequence.SequenceFormat.NativeText)


def format_shortcut_label(binding: ShortcutBinding) -> str:
    """Human-readable shortcut list including alternates (native glyphs)."""
    labels = [native_sequence_label(binding.sequence)]
    labels.extend(native_sequence_label(alt) for alt in binding.alternates)
    return ", ".join(labels)


def with_native_shortcuts(text: str) -> str:
    """Replace portable ``Ctrl+…`` tokens in tip/help text with native labels."""
    replacements: list[tuple[str, str]] = []
    for binding in STUDIO_SHORTCUTS:
        for sequence in (binding.sequence, *binding.alternates):
            portable = QKeySequence(sequence).toString(
                QKeySequence.SequenceFormat.PortableText
            )
            native = native_sequence_label(sequence)
            if portable and portable != native:
                replacements.append((portable, native))
            if sequence != portable and sequence != native:
                replacements.append((sequence, native))
    replacements.sort(key=lambda item: len(item[0]), reverse=True)
    for portable, native in replacements:
        text = text.replace(portable, native)
    return text


def _has_command_modifier(sequence: str) -> bool:
    """True for portable Ctrl/Meta/Alt chords (⌘ on macOS via Ctrl)."""
    text = sequence.upper()
    return "CTRL+" in text or "META+" in text or "ALT+" in text


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
        # Chord shortcuts stay app-wide so they work with Workspace focus.
        # Bare keys (R, F2, Return, …) stay window-scoped: ApplicationShortcut
        # steals typing in fields and still fails inside QGraphicsView.
        if _has_command_modifier(binding.sequence) or any(
            _has_command_modifier(alt) for alt in binding.alternates
        ):
            action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        else:
            action.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
