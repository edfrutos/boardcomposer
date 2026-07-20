"""Tests for changelog highlights and documentation paths."""

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QTableWidget

from studio.dialogs.help_dialogs import AboutDialog, ShortcutsDialog, WhatsNewDialog
from studio.keyboard_shortcuts import STUDIO_SHORTCUTS, apply_shortcuts
from studio.welcome_screen import WelcomeScreen
from studio.whats_new import documentation_paths, load_whats_new, repo_root


def test_repo_root_contains_changelog():
    root = repo_root()
    assert (root / "CHANGELOG.md").is_file()
    assert (root / "studio").is_dir()


def test_documentation_paths_exist():
    paths = documentation_paths()
    assert paths["readme"].is_file()
    assert paths["masterplan"].is_file()
    assert paths["changelog"].is_file()


def test_load_whats_new_from_changelog(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        "# CHANGELOG\n\n## Unreleased — 0.4.0\n\n### Añadido\n\n"
        "- Primera novedad\n- Segunda novedad\n\n### Cambiado\n\n- Ignorar\n",
        encoding="utf-8",
    )
    title, bullets = load_whats_new(changelog_path=changelog, max_items=10)
    assert "Unreleased" in title
    assert bullets == ["Primera novedad", "Segunda novedad"]


def test_load_whats_new_missing_file(tmp_path):
    title, bullets = load_whats_new(changelog_path=tmp_path / "missing.md")
    assert title
    assert bullets


def test_whats_new_and_about_dialogs(qapp):
    del qapp
    whats = WhatsNewDialog(language="en")
    assert whats.windowTitle() == "What’s new"
    about = AboutDialog(language="en")
    assert about.windowTitle() == "About"


def test_shortcuts_catalog_and_dialog(qapp):
    del qapp
    assert any(
        b.action_key == "undo" and b.sequence == "Ctrl+Z" for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "duplicate_piece" and b.sequence == "Ctrl+D"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "previous_solution" and b.sequence == "PgUp"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "next_solution" and b.sequence == "PgDown"
        for b in STUDIO_SHORTCUTS
    )
    delete_binding = next(b for b in STUDIO_SHORTCUTS if b.action_key == "delete_piece")
    assert delete_binding.sequence == "Backspace"
    assert delete_binding.alternates == ("Delete",)

    actions = {binding.action_key: QAction("") for binding in STUDIO_SHORTCUTS}
    apply_shortcuts(actions)
    assert actions["save"].shortcut() == QKeySequence("Ctrl+S")
    assert actions["rotate_piece"].shortcut() == QKeySequence("R")
    assert actions["previous_solution"].shortcut() == QKeySequence("PgUp")
    assert actions["next_solution"].shortcut() == QKeySequence("PgDown")
    delete_shortcuts = {
        sequence.toString() for sequence in actions["delete_piece"].shortcuts()
    }
    assert "Backspace" in delete_shortcuts
    assert "Del" in delete_shortcuts or "Delete" in delete_shortcuts

    dialog = ShortcutsDialog(language="en")
    assert dialog.windowTitle() == "Keyboard shortcuts"
    table = dialog.findChild(QTableWidget)
    assert table is not None
    assert table.rowCount() == len(STUDIO_SHORTCUTS)
    assert table.item(0, 0) is not None
    assert table.item(0, 1) is not None

    delete_row = next(
        i
        for i, binding in enumerate(STUDIO_SHORTCUTS)
        if binding.action_key == "delete_piece"
    )
    assert "Backspace" in table.item(delete_row, 1).text()
    assert "Delete" in table.item(delete_row, 1).text()

    zoom_row = next(
        i
        for i, binding in enumerate(STUDIO_SHORTCUTS)
        if binding.action_key == "zoom_in"
    )
    assert "Ctrl+=" in table.item(zoom_row, 1).text()
    assert "Ctrl++" in table.item(zoom_row, 1).text()


def test_welcome_has_docs_and_whats_new_buttons(qapp):
    del qapp
    screen = WelcomeScreen()
    screen.apply_language("en")
    assert screen.docs_button.text() == "Documentation…"
    assert screen.whats_new_button.text() == "What’s new…"
