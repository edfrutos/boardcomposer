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
    assert any(
        b.action_key == "apply_layout" and b.sequence == "Ctrl+Shift+Return"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "export_selected" and b.sequence == "Ctrl+Shift+E"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "add_piece" and b.sequence == "Ctrl+Shift+P"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "add_board" and b.sequence == "Ctrl+Shift+B"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "import_pieces_csv" and b.sequence == "Ctrl+Shift+O"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "import_boards_csv" and b.sequence == "Ctrl+Shift+T"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "export_timeline" and b.sequence == "Ctrl+Shift+L"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "show_welcome" and b.sequence == "Ctrl+Shift+H"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "reveal_project_folder" and b.sequence == "Ctrl+Shift+R"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "shortcuts" and b.sequence == "F1" for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "reset_window_layout" and b.sequence == "Ctrl+Shift+W"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "new_from_template" and b.sequence == "Ctrl+Shift+N"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "save_as_template" and b.sequence == "Ctrl+Shift+M"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "whats_new" and b.sequence == "Ctrl+Shift+U"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "new_demo_project" and b.sequence == "Ctrl+Shift+D"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "open_docs" and b.sequence == "Shift+F1"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "about" and b.sequence == "Ctrl+Shift+A"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "rename_project" and b.sequence == "Ctrl+Shift+F2"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "exit" and b.sequence == "Ctrl+Q" for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "clear_recent" and b.sequence == "Ctrl+Shift+X"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "toggle_toolbar" and b.sequence == "Ctrl+Shift+K"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "toggle_explorer" and b.sequence == "Ctrl+1"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "toggle_inspector" and b.sequence == "Ctrl+2"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "toggle_timeline" and b.sequence == "Ctrl+3"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "toggle_comparator" and b.sequence == "Ctrl+4"
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
    assert actions["apply_layout"].shortcut() == QKeySequence("Ctrl+Shift+Return")
    assert actions["export_selected"].shortcut() == QKeySequence("Ctrl+Shift+E")
    assert actions["add_piece"].shortcut() == QKeySequence("Ctrl+Shift+P")
    assert actions["add_board"].shortcut() == QKeySequence("Ctrl+Shift+B")
    assert actions["import_pieces_csv"].shortcut() == QKeySequence("Ctrl+Shift+O")
    assert actions["import_boards_csv"].shortcut() == QKeySequence("Ctrl+Shift+T")
    assert actions["export_timeline"].shortcut() == QKeySequence("Ctrl+Shift+L")
    assert actions["show_welcome"].shortcut() == QKeySequence("Ctrl+Shift+H")
    assert actions["reveal_project_folder"].shortcut() == QKeySequence("Ctrl+Shift+R")
    assert actions["shortcuts"].shortcut() == QKeySequence("F1")
    assert actions["reset_window_layout"].shortcut() == QKeySequence("Ctrl+Shift+W")
    assert actions["new_from_template"].shortcut() == QKeySequence("Ctrl+Shift+N")
    assert actions["save_as_template"].shortcut() == QKeySequence("Ctrl+Shift+M")
    assert actions["whats_new"].shortcut() == QKeySequence("Ctrl+Shift+U")
    assert actions["new_demo_project"].shortcut() == QKeySequence("Ctrl+Shift+D")
    assert actions["open_docs"].shortcut() == QKeySequence("Shift+F1")
    assert actions["about"].shortcut() == QKeySequence("Ctrl+Shift+A")
    assert actions["rename_project"].shortcut() == QKeySequence("Ctrl+Shift+F2")
    assert actions["exit"].shortcut() == QKeySequence("Ctrl+Q")
    assert actions["clear_recent"].shortcut() == QKeySequence("Ctrl+Shift+X")
    assert actions["toggle_toolbar"].shortcut() == QKeySequence("Ctrl+Shift+K")
    assert actions["toggle_explorer"].shortcut() == QKeySequence("Ctrl+1")
    assert actions["toggle_inspector"].shortcut() == QKeySequence("Ctrl+2")
    assert actions["toggle_timeline"].shortcut() == QKeySequence("Ctrl+3")
    assert actions["toggle_comparator"].shortcut() == QKeySequence("Ctrl+4")
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


def test_solve_layout_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Return" in tr("tip.solve_layout", "es")
    assert "Ctrl+Return" in tr("tip.solve_layout", "en")


def test_save_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+S" in tr("tip.save", "es")
    assert "Ctrl+S" in tr("tip.save", "en")


def test_toggle_grid_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+G" in tr("tip.toggle_grid", "es")
    assert "Ctrl+G" in tr("tip.toggle_grid", "en")


def test_undo_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Z" in tr("tip.undo", "es")
    assert "Ctrl+Z" in tr("tip.undo", "en")


def test_redo_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+Z" in tr("tip.redo", "es")
    assert "Ctrl+Shift+Z" in tr("tip.redo", "en")


def test_rotate_piece_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "(R)" in tr("tip.rotate_piece", "es")
    assert "(R)" in tr("tip.rotate_piece", "en")


def test_open_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+O" in tr("tip.open", "es")
    assert "Ctrl+O" in tr("tip.open", "en")


def test_new_project_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+N" in tr("tip.new_project", "es")
    assert "Ctrl+N" in tr("tip.new_project", "en")


def test_save_as_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+S" in tr("tip.save_as", "es")
    assert "Ctrl+Shift+S" in tr("tip.save_as", "en")


def test_preferences_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+," in tr("tip.preferences", "es")
    assert "Ctrl+," in tr("tip.preferences", "en")


def test_fit_board_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+0" in tr("tip.fit_board", "es")
    assert "Ctrl+0" in tr("tip.fit_board", "en")


def test_fit_selection_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+0" in tr("tip.fit_selection", "es")
    assert "Ctrl+Shift+0" in tr("tip.fit_selection", "en")


def test_zoom_in_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+=" in tr("tip.zoom_in", "es")
    assert "Ctrl+=" in tr("tip.zoom_in", "en")


def test_zoom_out_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+-" in tr("tip.zoom_out", "es")
    assert "Ctrl+-" in tr("tip.zoom_out", "en")
