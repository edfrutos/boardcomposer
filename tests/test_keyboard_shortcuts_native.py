"""Native shortcut labels (⌘ on macOS, Ctrl on Win/Linux)."""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence

from studio.keyboard_shortcuts import (
    STUDIO_SHORTCUTS,
    apply_shortcuts,
    format_shortcut_label,
    native_sequence_label,
    with_native_shortcuts,
)


def test_native_sequence_label_maps_ctrl_on_macos():
    label = native_sequence_label("Ctrl+S")
    if sys.platform == "darwin":
        assert "⌘" in label
        assert "Ctrl" not in label
    else:
        assert "Ctrl" in label


def test_with_native_shortcuts_rewrites_tip_text():
    text = with_native_shortcuts("Guardar (Ctrl+S)")
    if sys.platform == "darwin":
        assert text == f"Guardar ({native_sequence_label('Ctrl+S')})"
        assert "Ctrl+S" not in text
    else:
        assert text == "Guardar (Ctrl+S)"


def test_format_shortcut_label_includes_alternates_natively():
    binding = next(b for b in STUDIO_SHORTCUTS if b.action_key == "delete_piece")
    label = format_shortcut_label(binding)
    assert native_sequence_label("Backspace") in label
    assert native_sequence_label("Delete") in label


def test_apply_shortcuts_contexts_for_chords_vs_bare_keys(qapp):
    del qapp
    actions = {binding.action_key: QAction("") for binding in STUDIO_SHORTCUTS}
    apply_shortcuts(actions)
    assert actions["save"].shortcut() == QKeySequence("Ctrl+S")
    assert actions["save"].shortcutContext() == Qt.ShortcutContext.ApplicationShortcut
    assert (
        actions["rotate_piece"].shortcutContext() == Qt.ShortcutContext.WindowShortcut
    )
