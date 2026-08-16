"""Tests for changelog highlights and documentation paths."""

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QLabel, QTableWidget

from studio.dialogs.help_dialogs import AboutDialog, ShortcutsDialog, WhatsNewDialog
from studio.keyboard_shortcuts import (
    CONTEXTUAL_SHORTCUTS,
    STUDIO_SHORTCUTS,
    all_shortcut_rows,
    apply_shortcuts,
    format_shortcut_label,
    native_sequence_label,
)
from studio.welcome_screen import WelcomeScreen
from studio.whats_new import documentation_paths, load_whats_new, repo_root


def test_repo_root_contains_changelog():
    root = repo_root()
    assert (root / "CHANGELOG.md").is_file()
    assert (root / "studio").is_dir()


def test_documentation_paths_exist():
    paths = documentation_paths()
    assert paths["user_guide"].is_file()
    assert paths["docs_index"].is_file()
    assert paths["readme"].is_file()
    assert paths["masterplan"].is_file()
    assert paths["changelog"].is_file()
    assert paths["design"].is_file()


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


def test_load_whats_new_reads_english_added_section(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        "# CHANGELOG\n\n## Unreleased\n\n### Added\n\n- First item\n\n### Changed\n\n- Skip\n",
        encoding="utf-8",
    )
    title, bullets = load_whats_new(changelog_path=changelog)
    assert "Unreleased" in title
    assert bullets == ["First item"]


def test_load_whats_new_respects_max_items(tmp_path):
    bullets_src = "\n".join(f"- Item {i}" for i in range(1, 8))
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        f"# CHANGELOG\n\n## Unreleased\n\n### Añadido\n\n{bullets_src}\n",
        encoding="utf-8",
    )
    _title, bullets = load_whats_new(changelog_path=changelog, max_items=3)
    assert bullets == ["Item 1", "Item 2", "Item 3"]


def test_load_whats_new_fallback_when_unreleased_has_no_added_bullets(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        "# CHANGELOG\n\n## Unreleased\n\n### Cambiado\n\n- Solo cambios\n",
        encoding="utf-8",
    )
    title, bullets = load_whats_new(changelog_path=changelog, language="es")
    assert "Unreleased" in title
    assert len(bullets) == 1
    assert "CHANGELOG.md" in bullets[0]

    _title_en, bullets_en = load_whats_new(changelog_path=changelog, language="en")
    assert "See CHANGELOG.md" in bullets_en[0]


def test_load_whats_new_skips_empty_cycle_placeholder(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        "# CHANGELOG\n\n## Unreleased — 0.4.2.dev0\n\n### Añadido\n\n"
        "- _(ciclo post-`0.4.1` — vacío al corte)_\n\n"
        "## 0.4.1 — 2026-08-01\n\n### Añadido\n\n"
        "- Restaurar última revisión local\n\n### Cambiado\n\n"
        "- Anillo local a 10 revisiones\n",
        encoding="utf-8",
    )
    title, bullets = load_whats_new(changelog_path=changelog, max_items=10)
    assert title.startswith("0.4.1")
    assert "Restaurar última revisión local" in bullets
    assert "Anillo local a 10 revisiones" in bullets
    assert not any("vacío al corte" in b for b in bullets)


def test_load_whats_new_prefers_real_unreleased_over_release(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        "# CHANGELOG\n\n## Unreleased — 0.4.2.dev0\n\n### Añadido\n\n"
        "- Novedad del ciclo\n\n"
        "## 0.4.1 — 2026-08-01\n\n### Añadido\n\n- De la release\n",
        encoding="utf-8",
    )
    title, bullets = load_whats_new(changelog_path=changelog)
    assert "Unreleased" in title
    assert bullets == ["Novedad del ciclo"]


def test_load_whats_new_falls_back_to_release_when_unreleased_only_changed(
    tmp_path,
):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        "# CHANGELOG\n\n## Unreleased\n\n### Cambiado\n\n- Solo WIP\n\n"
        "## 0.4.1\n\n### Añadido\n\n- Highlight de release\n",
        encoding="utf-8",
    )
    title, bullets = load_whats_new(changelog_path=changelog)
    assert title.startswith("0.4.1")
    assert bullets == ["Highlight de release"]


def test_load_whats_new_repo_changelog_has_no_placeholder_bullets():
    title, bullets = load_whats_new(max_items=12)
    assert title
    assert bullets
    assert not any("vacío al corte" in b.lower() for b in bullets)
    assert not any(b.startswith("_(") and b.endswith(")_") for b in bullets)


def test_load_whats_new_missing_file(tmp_path):
    title, bullets = load_whats_new(
        changelog_path=tmp_path / "missing.md", language="es"
    )
    assert title == "BoardComposer Studio"
    assert bullets == ["No hay notas de versión disponibles."]

    _title_en, bullets_en = load_whats_new(
        changelog_path=tmp_path / "missing.md", language="en"
    )
    assert bullets_en == ["No release notes available."]


def test_whats_new_and_about_dialogs(qapp):
    del qapp
    whats = WhatsNewDialog(language="en")
    assert whats.objectName() == "whatsNewRoot"
    assert whats.windowTitle() == "What’s new"
    about = AboutDialog(language="en")
    assert about.objectName() == "aboutRoot"
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
        b.action_key == "export_revision_backup" and b.sequence == "Ctrl+Alt+B"
        for b in STUDIO_SHORTCUTS
    )
    assert any(
        b.action_key == "explain_solution" and b.sequence == "Ctrl+Alt+E"
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
    assert dialog.objectName() == "shortcutsRoot"
    assert dialog.windowTitle() == "Keyboard shortcuts"
    table = dialog.findChild(QTableWidget)
    assert table is not None
    assert table.objectName() == "shortcutsTable"
    assert table.rowCount() == len(all_shortcut_rows())
    assert table.item(0, 0) is not None
    assert table.item(0, 1) is not None

    delete_row = next(
        i
        for i, binding in enumerate(all_shortcut_rows())
        if binding.action_key == "delete_piece"
    )
    delete_binding = all_shortcut_rows()[delete_row]
    assert table.item(delete_row, 1).text() == format_shortcut_label(delete_binding)
    assert native_sequence_label("Backspace") in table.item(delete_row, 1).text()
    assert native_sequence_label("Delete") in table.item(delete_row, 1).text()

    zoom_row = next(
        i
        for i, binding in enumerate(all_shortcut_rows())
        if binding.action_key == "zoom_in"
    )
    zoom_binding = all_shortcut_rows()[zoom_row]
    assert table.item(zoom_row, 1).text() == format_shortcut_label(zoom_binding)
    assert native_sequence_label("Ctrl+=") in table.item(zoom_row, 1).text()
    assert native_sequence_label("Ctrl++") in table.item(zoom_row, 1).text()

    replay_row = next(
        i
        for i, binding in enumerate(all_shortcut_rows())
        if binding.action_key == "timeline_replay_play"
    )
    assert "Timeline" in table.item(replay_row, 0).text()
    assert native_sequence_label("Space") in table.item(replay_row, 1).text()

    copy_row = next(
        i
        for i, binding in enumerate(all_shortcut_rows())
        if binding.action_key == "timeline_copy_line"
    )
    assert "Timeline" in table.item(copy_row, 0).text()
    assert native_sequence_label("Ctrl+C") in table.item(copy_row, 1).text()
    assert len(CONTEXTUAL_SHORTCUTS) == 5
    intro = dialog.findChild(QLabel)
    assert intro is not None
    assert "timeline" in intro.text().casefold()
    assert "ctrl+c" in intro.text().casefold() or "⌘c" in intro.text().casefold()


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
    assert "desactualiz" in tr("tip.solve_layout_outdated", "es").lower()
    assert "outdated" in tr("tip.solve_layout_outdated", "en").lower()
    assert "Ctrl+Return" in tr("tip.solve_layout_outdated", "es")
    assert "Ctrl+Return" in tr("tip.solve_layout_outdated", "en")


def test_solve_layout_tip_mentions_inventory():
    from studio.i18n import tr

    es = tr("tip.solve_layout", "es").casefold()
    en = tr("tip.solve_layout", "en").casefold()
    assert "inventario" in es
    assert "tableros" in es and "piezas" in es
    assert "inventory" in en
    assert "board" in en and "piece" in en


def test_save_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+S" in tr("tip.save", "es")
    assert "Ctrl+S" in tr("tip.save", "en")


def test_toggle_grid_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+G" in tr("tip.toggle_grid", "es")
    assert "Ctrl+G" in tr("tip.toggle_grid", "en")
    assert "Ctrl+G" in tr("tip.toggle_grid_show", "es")
    assert "Ctrl+G" in tr("tip.toggle_grid_hide", "en")


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


def test_rotate_piece_tip_mentions_placed_on_board():
    from studio.i18n import tr

    es = tr("tip.rotate_piece", "es").casefold()
    en = tr("tip.rotate_piece", "en").casefold()
    assert "tablero" in es
    assert "board" in en


def test_open_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+O" in tr("tip.open", "es")
    assert "Ctrl+O" in tr("tip.open", "en")


def test_open_tip_mentions_unsaved_confirmation():
    from studio.i18n import tr

    es = tr("tip.open", "es").casefold()
    en = tr("tip.open", "en").casefold()
    assert "sin guardar" in es
    assert "unsaved" in en


def test_recent_menu_open_tip_mentions_unsaved_confirmation():
    from studio.i18n import tr

    es = tr("tip.recent_menu_open", "es").casefold()
    en = tr("tip.recent_menu_open", "en").casefold()
    assert "sin guardar" in es
    assert "unsaved" in en


def test_recent_row_tip_mentions_unsaved_confirmation():
    from studio.i18n import tr

    es = tr("tip.recent_row", "es").casefold()
    en = tr("tip.recent_row", "en").casefold()
    assert "sin guardar" in es
    assert "unsaved" in en


def test_recent_row_pinned_tip_mentions_unsaved_confirmation():
    from studio.i18n import tr

    es = tr("tip.recent_row_pinned", "es").casefold()
    en = tr("tip.recent_row_pinned", "en").casefold()
    assert "sin guardar" in es
    assert "unsaved" in en


def test_folder_memory_status_tips_are_honest():
    from studio.i18n import tr

    keys = (
        "tip.open",
        "tip.save_as",
        "tip.diff_bcproj",
        "tip.import_boards_csv",
        "tip.import_pieces_csv",
        "tip.export_selected",
        "tip.export_timeline",
        "tip.export_share_export",
        "tip.export_share_import",
        "tip.export_revision_backup",
    )
    for key in keys:
        assert "recuerda la última carpeta" in tr(key, "es")
        assert "remembers the last folder" in tr(key, "en")


def test_new_project_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+N" in tr("tip.new_project", "es")
    assert "Ctrl+N" in tr("tip.new_project", "en")


def test_save_as_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+S" in tr("tip.save_as", "es")
    assert "Ctrl+Shift+S" in tr("tip.save_as", "en")


def test_save_as_tip_mentions_becomes_current_file():
    from studio.i18n import tr

    es = tr("tip.save_as", "es").casefold()
    en = tr("tip.save_as", "en").casefold()
    assert "archivo actual" in es
    assert "current file" in en


def test_save_as_tip_mentions_ring_revision_when_file_exists():
    from studio.i18n import tr

    es = tr("tip.save_as", "es").casefold()
    en = tr("tip.save_as", "en").casefold()
    assert "revisión" in es and "anillo" in es
    assert "revision" in en and "ring" in en


def test_preferences_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+," in tr("tip.preferences", "es")
    assert "Ctrl+," in tr("tip.preferences", "en")


def test_fit_board_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+0" in tr("tip.fit_board", "es")
    assert "Ctrl+0" in tr("tip.fit_board", "en")


def test_fit_board_tip_mentions_ignores_selection():
    from studio.i18n import tr

    es = tr("tip.fit_board", "es").casefold()
    en = tr("tip.fit_board", "en").casefold()
    assert "ignora" in es and "selección" in es
    assert "ignores" in en and "selection" in en


def test_fit_selection_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+0" in tr("tip.fit_selection", "es")
    assert "Ctrl+Shift+0" in tr("tip.fit_selection", "en")


def test_fit_selection_tip_mentions_pieces_or_focused_board():
    from studio.i18n import tr

    es = tr("tip.fit_selection", "es").casefold()
    en = tr("tip.fit_selection", "en").casefold()
    assert "seleccionadas" in es and "enfocado" in es
    assert "pieces" in en and "focused" in en


def test_zoom_in_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+=" in tr("tip.zoom_in", "es")
    assert "Ctrl+=" in tr("tip.zoom_in", "en")
    assert "rueda" in tr("tip.zoom_in", "es").casefold()
    assert "wheel" in tr("tip.zoom_in", "en").casefold()


def test_zoom_out_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+-" in tr("tip.zoom_out", "es")
    assert "Ctrl+-" in tr("tip.zoom_out", "en")
    assert "rueda" in tr("tip.zoom_out", "es").casefold()
    assert "wheel" in tr("tip.zoom_out", "en").casefold()


def test_select_all_pieces_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+A" in tr("tip.select_all_pieces", "es")
    assert "Ctrl+A" in tr("tip.select_all_pieces", "en")


def test_deselect_pieces_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Escape" in tr("tip.deselect_pieces", "es")
    assert "Escape" in tr("tip.deselect_pieces", "en")


def test_invert_selection_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+I" in tr("tip.invert_selection", "es")
    assert "Ctrl+Shift+I" in tr("tip.invert_selection", "en")


def test_duplicate_piece_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+D" in tr("tip.duplicate_piece", "es")
    assert "Ctrl+D" in tr("tip.duplicate_piece", "en")


def test_edit_selection_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Return" in tr("tip.edit_selection", "es")
    assert "Return" in tr("tip.edit_selection", "en")


def test_rename_selection_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "F2" in tr("tip.rename_selection", "es")
    assert "F2" in tr("tip.rename_selection", "en")


def test_rename_selection_tip_mentions_name_dialog():
    from studio.i18n import tr

    es = tr("tip.rename_selection", "es").casefold()
    en = tr("tip.rename_selection", "en").casefold()
    assert "nombre" in es or "id" in es
    assert "name" in en or "id" in en


def test_copy_selection_id_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+C" in tr("tip.copy_selection_id", "es")
    assert "Ctrl+Shift+C" in tr("tip.copy_selection_id", "en")


def test_copy_selection_id_tip_mentions_explorer_and_focused_board():
    from studio.i18n import tr

    es = tr("tip.copy_selection_id", "es").casefold()
    en = tr("tip.copy_selection_id", "en").casefold()
    assert "explorador" in es and "única" in es and "enfocado" in es
    assert "explorer" in en and "single" in en and "focused" in en


def test_delete_piece_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Backspace" in tr("tip.delete_piece", "es")
    assert "Delete" in tr("tip.delete_piece", "es")
    assert "Backspace" in tr("tip.delete_piece", "en")
    assert "Delete" in tr("tip.delete_piece", "en")


def test_previous_solution_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Re Pág" in tr("tip.previous_solution", "es")
    assert "Page Up" in tr("tip.previous_solution", "en")


def test_next_solution_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Av Pág" in tr("tip.next_solution", "es")
    assert "Page Down" in tr("tip.next_solution", "en")


def test_apply_layout_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+Return" in tr("tip.apply_layout", "es")
    assert "Ctrl+Shift+Return" in tr("tip.apply_layout", "en")


def test_apply_layout_tip_mentions_replaces_placements():
    from studio.i18n import tr

    es = tr("tip.apply_layout", "es").casefold()
    en = tr("tip.apply_layout", "en").casefold()
    assert "colocaciones" in es
    assert "placements" in en


def test_export_selected_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+E" in tr("tip.export_selected", "es")
    assert "Ctrl+Shift+E" in tr("tip.export_selected", "en")


def test_export_selected_tip_mentions_options_and_preview():
    from studio.i18n import tr

    es = tr("tip.export_selected", "es").casefold()
    en = tr("tip.export_selected", "en").casefold()
    assert "opciones" in es and "vista previa" in es
    assert "options" in en and "preview" in en


def test_export_selected_tip_mentions_offer_to_open():
    from studio.i18n import tr

    es = tr("tip.export_selected", "es").casefold()
    en = tr("tip.export_selected", "en").casefold()
    assert "ofrece" in es and "abrir" in es
    assert "offers" in en and "open" in en


def test_export_timeline_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+L" in tr("tip.export_timeline", "es")
    assert "Ctrl+Shift+L" in tr("tip.export_timeline", "en")


def test_export_timeline_tip_mentions_json_csv_and_filters():
    from studio.i18n import tr

    es = tr("tip.export_timeline", "es").casefold()
    en = tr("tip.export_timeline", "en").casefold()
    assert "json" in es and "csv" in es and "filtros" in es
    assert "json" in en and "csv" in en and "filters" in en


def test_export_timeline_tip_mentions_offer_to_open():
    from studio.i18n import tr

    es = tr("tip.export_timeline", "es").casefold()
    en = tr("tip.export_timeline", "en").casefold()
    assert "ofrece" in es and "abrir" in es
    assert "offers" in en and "open" in en


def test_diff_bcproj_tip_mentions_dialog_and_restore():
    from studio.i18n import tr

    es = tr("tip.diff_bcproj", "es").casefold()
    en = tr("tip.diff_bcproj", "en").casefold()
    assert "diálogo" in es and "restaurar" in es
    assert "dialog" in en and "restore" in en


def test_timeline_clear_tip_mentions_confirmation():
    from studio.i18n import tr

    assert "confirmación" in tr("tip.timeline_clear", "es").casefold()
    assert "confirmation" in tr("tip.timeline_clear", "en").casefold()


def test_timeline_list_and_copy_tips_mention_ctrl_c():
    from studio.i18n import tr

    for lang in ("es", "en"):
        assert "Ctrl+C" in tr("tip.timeline_list", lang)
        assert "Ctrl+C" in tr("tip.timeline_copy_line", lang)
        assert "JSON" in tr("tip.timeline_copy_payload", lang)


def test_timeline_mark_tip_mentions_note_dialog():
    from studio.i18n import tr

    es = tr("tip.timeline_mark", "es").casefold()
    en = tr("tip.timeline_mark", "en").casefold()
    assert "nota" in es
    assert "diálogo" in es
    assert "note" in en
    assert "dialog" in en


def test_comparator_sort_tip_lists_criteria():
    from studio.i18n import tr

    es = tr("tip.comparator_sort", "es").casefold()
    en = tr("tip.comparator_sort", "en").casefold()
    assert "ranking" in es
    assert "puntuación" in es
    assert "ranking" in en
    assert "score" in en


def test_comparator_sort_tip_mentions_session_only():
    from studio.i18n import tr

    es = tr("tip.comparator_sort", "es").casefold()
    en = tr("tip.comparator_sort", "en").casefold()
    assert "sesión" in es
    assert "session" in en


def test_preview_solution_tip_mentions_apply_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+Return" in tr("tip.preview_solution", "es")
    assert "Ctrl+Shift+Return" in tr("tip.preview_solution", "en")
    assert "sin aplicarla" in tr("tip.preview_solution", "es").casefold()
    assert "without applying" in tr("tip.preview_solution", "en").casefold()


def test_comparator_complete_only_tip_explains_toggle():
    from studio.i18n import tr

    es = tr("tip.comparator_complete_only", "es").casefold()
    en = tr("tip.comparator_complete_only", "en").casefold()
    assert "omitidas" in es or "completas" in es
    assert "desactivar" in es
    assert "omitted" in en or "complete" in en
    assert "turn off" in en


def test_comparator_complete_only_tip_mentions_session_only():
    from studio.i18n import tr

    es = tr("tip.comparator_complete_only", "es").casefold()
    en = tr("tip.comparator_complete_only", "en").casefold()
    assert "sesión" in es
    assert "session" in en


def test_new_demo_project_tip_mentions_inventory_and_unsaved():
    from studio.i18n import tr

    es = tr("tip.new_demo_project", "es").casefold()
    en = tr("tip.new_demo_project", "en").casefold()
    assert "Ctrl+Shift+D" in tr("tip.new_demo_project", "es")
    assert "Ctrl+Shift+D" in tr("tip.new_demo_project", "en")
    assert "tableros" in es and "piezas" in es
    assert "sin guardar" in es
    assert "boards" in en and "pieces" in en
    assert "unsaved" in en


def test_new_from_template_tip_mentions_picker_and_unsaved():
    from studio.i18n import tr

    es = tr("tip.new_from_template", "es").casefold()
    en = tr("tip.new_from_template", "en").casefold()
    assert "Ctrl+Shift+N" in tr("tip.new_from_template", "es")
    assert "Ctrl+Shift+N" in tr("tip.new_from_template", "en")
    assert "plantilla" in es and "sin guardar" in es
    assert "template" in en and "unsaved" in en


def test_new_project_tip_mentions_dialog_and_unsaved():
    from studio.i18n import tr

    es = tr("tip.new_project", "es").casefold()
    en = tr("tip.new_project", "en").casefold()
    assert "Ctrl+N" in tr("tip.new_project", "es")
    assert "Ctrl+N" in tr("tip.new_project", "en")
    assert "nombre" in es and "sin guardar" in es
    assert "name" in en and "unsaved" in en


def test_save_as_template_tip_mentions_name_and_placements():
    from studio.i18n import tr

    es = tr("tip.save_as_template", "es").casefold()
    en = tr("tip.save_as_template", "en").casefold()
    assert "Ctrl+Shift+M" in tr("tip.save_as_template", "es")
    assert "Ctrl+Shift+M" in tr("tip.save_as_template", "en")
    assert "nombre" in es and "colocaciones" in es
    assert "name" in en and "placements" in en


def test_clear_recent_tip_mentions_confirmation_and_disk_safe():
    from studio.i18n import tr

    es = tr("tip.clear_recent", "es").casefold()
    en = tr("tip.clear_recent", "en").casefold()
    assert "Ctrl+Shift+X" in tr("tip.clear_recent", "es")
    assert "Ctrl+Shift+X" in tr("tip.clear_recent", "en")
    assert "confirmación" in es and "disco" in es
    assert "confirmation" in en and "disk" in en


def test_remove_recent_tip_mentions_disk_safe():
    from studio.i18n import tr

    es = tr("tip.remove_recent", "es").casefold()
    en = tr("tip.remove_recent", "en").casefold()
    assert "disco" in es
    assert "disk" in en


def test_recent_menu_remove_tip_mentions_disk_safe():
    from studio.i18n import tr

    es = tr("tip.recent_menu_remove", "es").casefold()
    en = tr("tip.recent_menu_remove", "en").casefold()
    assert "disco" in es
    assert "disk" in en


def test_exit_tip_mentions_unsaved_confirmation():
    from studio.i18n import tr

    es = tr("tip.exit", "es").casefold()
    en = tr("tip.exit", "en").casefold()
    assert "Ctrl+Q" in tr("tip.exit", "es")
    assert "Ctrl+Q" in tr("tip.exit", "en")
    assert "sin guardar" in es
    assert "unsaved" in en


def test_whats_new_tip_mentions_dialog_highlights():
    from studio.i18n import tr

    es = tr("tip.whats_new", "es").casefold()
    en = tr("tip.whats_new", "en").casefold()
    assert "Ctrl+Shift+U" in tr("tip.whats_new", "es")
    assert "Ctrl+Shift+U" in tr("tip.whats_new", "en")
    assert "diálogo" in es and "resumen" in es
    assert "dialog" in en and "highlights" in en


def test_open_docs_tip_mentions_local_system_app():
    from studio.i18n import tr

    es = tr("tip.open_docs", "es").casefold()
    en = tr("tip.open_docs", "en").casefold()
    assert "Shift+F1" in tr("tip.open_docs", "es")
    assert "Shift+F1" in tr("tip.open_docs", "en")
    assert "local" in es and "sistema" in es
    assert "local" in en and "system" in en


def test_about_tip_mentions_version_dialog():
    from studio.i18n import tr

    es = tr("tip.about", "es").casefold()
    en = tr("tip.about", "en").casefold()
    assert "Ctrl+Shift+A" in tr("tip.about", "es")
    assert "Ctrl+Shift+A" in tr("tip.about", "en")
    assert "versión" in es
    assert "version" in en


def test_shortcuts_tip_mentions_dialog_and_timeline_rows():
    from studio.i18n import tr

    es = tr("tip.shortcuts", "es").casefold()
    en = tr("tip.shortcuts", "en").casefold()
    assert "F1" in tr("tip.shortcuts", "es")
    assert "F1" in tr("tip.shortcuts", "en")
    assert "diálogo" in es and "timeline" in es
    assert "dialog" in en and "timeline" in en


def test_show_welcome_tip_mentions_keeps_project():
    from studio.i18n import tr

    es = tr("tip.show_welcome", "es").casefold()
    en = tr("tip.show_welcome", "en").casefold()
    assert "Ctrl+Shift+H" in tr("tip.show_welcome", "es")
    assert "Ctrl+Shift+H" in tr("tip.show_welcome", "en")
    assert "sin cerrar" in es and "proyecto" in es
    assert "without closing" in en and "project" in en


def test_preferences_tip_mentions_global_sections():
    from studio.i18n import tr

    es = tr("tip.preferences", "es").casefold()
    en = tr("tip.preferences", "en").casefold()
    assert "Ctrl+," in tr("tip.preferences", "es")
    assert "Ctrl+," in tr("tip.preferences", "en")
    assert "idioma" in es and "cuadrícula" in es and "exportación" in es
    assert "language" in en and "grid" in en and "export" in en


def test_preferences_tip_mentions_apply_on_accept():
    from studio.i18n import tr

    es = tr("tip.preferences", "es").casefold()
    en = tr("tip.preferences", "en").casefold()
    assert "aplican" in es and "aceptar" in es
    assert "applied" in en and "accept" in en


def test_delete_piece_tip_mentions_confirmation():
    from studio.i18n import tr

    es = tr("tip.delete_piece", "es").casefold()
    en = tr("tip.delete_piece", "en").casefold()
    assert "Backspace" in tr("tip.delete_piece", "es")
    assert "Delete" in tr("tip.delete_piece", "en")
    assert "confirmación" in es
    assert "confirmation" in en


def test_rename_project_tip_mentions_name_dialog():
    from studio.i18n import tr

    es = tr("tip.rename_project", "es").casefold()
    en = tr("tip.rename_project", "en").casefold()
    assert "Ctrl+Shift+F2" in tr("tip.rename_project", "es")
    assert "Ctrl+Shift+F2" in tr("tip.rename_project", "en")
    assert "nombre" in es
    assert "name" in en


def test_save_tip_mentions_path_prompt_when_unsaved():
    from studio.i18n import tr

    es = tr("tip.save", "es").casefold()
    en = tr("tip.save", "en").casefold()
    assert "Ctrl+S" in tr("tip.save", "es")
    assert "Ctrl+S" in tr("tip.save", "en")
    assert "ruta" in es and "guardar como" in es
    assert "path" in en and "save as" in en


def test_save_tip_mentions_ring_revision_when_file_exists():
    from studio.i18n import tr

    es = tr("tip.save", "es").casefold()
    en = tr("tip.save", "en").casefold()
    assert "revisión" in es and "anillo" in es
    assert "revision" in en and "ring" in en


def test_add_board_tip_mentions_dimensions_dialog():
    from studio.i18n import tr

    es = tr("tip.add_board", "es").casefold()
    en = tr("tip.add_board", "en").casefold()
    assert "Ctrl+Shift+B" in tr("tip.add_board", "es")
    assert "Ctrl+Shift+B" in tr("tip.add_board", "en")
    assert "diálogo" in es and "dimensiones" in es
    assert "dialog" in en and "dimensions" in en


def test_add_piece_tip_mentions_dimensions_dialog():
    from studio.i18n import tr

    es = tr("tip.add_piece", "es").casefold()
    en = tr("tip.add_piece", "en").casefold()
    assert "Ctrl+Shift+P" in tr("tip.add_piece", "es")
    assert "Ctrl+Shift+P" in tr("tip.add_piece", "en")
    assert "diálogo" in es and "cantidad" in es
    assert "dialog" in en and "quantity" in en


def test_edit_selection_tip_mentions_dimensions_dialog():
    from studio.i18n import tr

    es = tr("tip.edit_selection", "es").casefold()
    en = tr("tip.edit_selection", "en").casefold()
    assert "Return" in tr("tip.edit_selection", "es")
    assert "Return" in tr("tip.edit_selection", "en")
    assert "diálogo" in es and "dimensiones" in es
    assert "dialog" in en and "dimensions" in en


def test_duplicate_piece_tip_mentions_unique_id():
    from studio.i18n import tr

    es = tr("tip.duplicate_piece", "es").casefold()
    en = tr("tip.duplicate_piece", "en").casefold()
    assert "Ctrl+D" in tr("tip.duplicate_piece", "es")
    assert "Ctrl+D" in tr("tip.duplicate_piece", "en")
    assert "id único" in es or "id unico" in es
    assert "unique id" in en


def test_template_delete_tip_mentions_confirmation():
    from studio.i18n import tr

    es = tr("tip.template_delete", "es").casefold()
    en = tr("tip.template_delete", "en").casefold()
    assert "confirmación" in es
    assert "confirmation" in en
    assert "catálogo" in es or "catalogo" in es
    assert "catalog" in en


def test_template_rename_tip_mentions_name_dialog():
    from studio.i18n import tr

    es = tr("tip.template_rename", "es").casefold()
    en = tr("tip.template_rename", "en").casefold()
    assert "nombre" in es
    assert "name" in en


def test_export_delete_template_tip_mentions_confirmation():
    from studio.i18n import tr

    es = tr("tip.export_delete_template", "es").casefold()
    en = tr("tip.export_delete_template", "en").casefold()
    assert "confirmación" in es
    assert "confirmation" in en


def test_export_save_template_tip_mentions_name_dialog():
    from studio.i18n import tr

    es = tr("tip.export_save_template", "es").casefold()
    en = tr("tip.export_save_template", "en").casefold()
    assert "nombre" in es
    assert "name" in en


def test_export_share_import_tip_mentions_merge_or_replace():
    from studio.i18n import tr

    es = tr("tip.export_share_import", "es").casefold()
    en = tr("tip.export_share_import", "en").casefold()
    assert "fusionar" in es and "reemplazar" in es
    assert "merge" in en and "replace" in en


def test_export_share_export_tip_mentions_json_and_client_filter():
    from studio.i18n import tr

    es = tr("tip.export_share_export", "es").casefold()
    en = tr("tip.export_share_export", "en").casefold()
    assert "json" in es and "filtro" in es and "cliente" in es
    assert "json" in en and "filter" in en and "client" in en


def test_export_revision_backup_tip_mentions_offer_to_open():
    from studio.i18n import tr

    es = tr("tip.export_revision_backup", "es").casefold()
    en = tr("tip.export_revision_backup", "en").casefold()
    assert "ofrece" in es and "abrir" in es
    assert "offers" in en and "open" in en


def test_exit_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Q" in tr("tip.exit", "es")
    assert "Ctrl+Q" in tr("tip.exit", "en")


def test_reset_window_layout_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+W" in tr("tip.reset_window_layout", "es")
    assert "Ctrl+Shift+W" in tr("tip.reset_window_layout", "en")


def test_reset_window_layout_tip_mentions_saves_layout():
    from studio.i18n import tr

    es = tr("tip.reset_window_layout", "es").casefold()
    en = tr("tip.reset_window_layout", "en").casefold()
    assert "guarda" in es
    assert "saves" in en


def test_shortcuts_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "F1" in tr("tip.shortcuts", "es")
    assert "F1" in tr("tip.shortcuts", "en")


def test_whats_new_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+U" in tr("tip.whats_new", "es")
    assert "Ctrl+Shift+U" in tr("tip.whats_new", "en")


def test_open_docs_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Shift+F1" in tr("tip.open_docs", "es")
    assert "Shift+F1" in tr("tip.open_docs", "en")
    assert "guía" in tr("tip.open_docs", "es").lower()
    assert "guide" in tr("tip.open_docs", "en").lower()
    assert "guía" in tr("status.docs_opened", "es").lower()
    assert "guide" in tr("status.docs_opened", "en").lower()


def test_about_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+A" in tr("tip.about", "es")
    assert "Ctrl+Shift+A" in tr("tip.about", "en")


def test_clear_recent_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+X" in tr("tip.clear_recent", "es")
    assert "Ctrl+Shift+X" in tr("tip.clear_recent", "en")


def test_toggle_toolbar_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+K" in tr("tip.toggle_toolbar", "es")
    assert "Ctrl+Shift+K" in tr("tip.toggle_toolbar", "en")
    assert "Ctrl+Shift+K" in tr("tip.toggle_toolbar_show", "es")
    assert "Ctrl+Shift+K" in tr("tip.toggle_toolbar_hide", "en")


def test_toggle_explorer_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+1" in tr("tip.toggle_explorer", "es")
    assert "Ctrl+1" in tr("tip.toggle_explorer", "en")
    assert "Ctrl+1" in tr("tip.toggle_explorer_show", "es")
    assert "Ctrl+1" in tr("tip.toggle_explorer_hide", "en")


def test_toggle_inspector_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+2" in tr("tip.toggle_inspector", "es")
    assert "Ctrl+2" in tr("tip.toggle_inspector", "en")


def test_toggle_timeline_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+3" in tr("tip.toggle_timeline", "es")
    assert "Ctrl+3" in tr("tip.toggle_timeline", "en")


def test_toggle_comparator_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+4" in tr("tip.toggle_comparator", "es")
    assert "Ctrl+4" in tr("tip.toggle_comparator", "en")


def test_new_demo_project_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+D" in tr("tip.new_demo_project", "es")
    assert "Ctrl+Shift+D" in tr("tip.new_demo_project", "en")


def test_show_welcome_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+H" in tr("tip.show_welcome", "es")
    assert "Ctrl+Shift+H" in tr("tip.show_welcome", "en")


def test_new_from_template_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+N" in tr("tip.new_from_template", "es")
    assert "Ctrl+Shift+N" in tr("tip.new_from_template", "en")


def test_save_as_template_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+M" in tr("tip.save_as_template", "es")
    assert "Ctrl+Shift+M" in tr("tip.save_as_template", "en")


def test_rename_project_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+F2" in tr("tip.rename_project", "es")
    assert "Ctrl+Shift+F2" in tr("tip.rename_project", "en")


def test_reveal_project_folder_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+R" in tr("tip.reveal_project_folder", "es")
    assert "Ctrl+Shift+R" in tr("tip.reveal_project_folder", "en")


def test_add_board_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+B" in tr("tip.add_board", "es")
    assert "Ctrl+Shift+B" in tr("tip.add_board", "en")


def test_add_piece_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+P" in tr("tip.add_piece", "es")
    assert "Ctrl+Shift+P" in tr("tip.add_piece", "en")


def test_import_boards_csv_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+T" in tr("tip.import_boards_csv", "es")
    assert "Ctrl+Shift+T" in tr("tip.import_boards_csv", "en")


def test_import_boards_csv_tip_mentions_mapping_and_preview():
    from studio.i18n import tr

    es = tr("tip.import_boards_csv", "es").casefold()
    en = tr("tip.import_boards_csv", "en").casefold()
    assert "mapeo" in es and "vista previa" in es
    assert "mapping" in en and "preview" in en


def test_import_pieces_csv_status_tip_includes_shortcut():
    from studio.i18n import tr

    assert "Ctrl+Shift+O" in tr("tip.import_pieces_csv", "es")
    assert "Ctrl+Shift+O" in tr("tip.import_pieces_csv", "en")


def test_import_pieces_csv_tip_mentions_mapping_and_preview():
    from studio.i18n import tr

    es = tr("tip.import_pieces_csv", "es").casefold()
    en = tr("tip.import_pieces_csv", "en").casefold()
    assert "mapeo" in es and "vista previa" in es
    assert "mapping" in en and "preview" in en
