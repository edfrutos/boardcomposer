"""Tests for menu and Inspector language switching (SCR-006)."""

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def test_main_window_menus_and_inspector_follow_language(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))

    window = MainWindow(services)

    assert window._menus["file"].title() == "Archivo"
    assert window._actions["solve_layout"].text() == "Calcular layout"
    assert "Sin selección" in window.inspector.toPlainText()
    assert window.inspector_dock.windowTitle() == "Inspector"
    assert window.pin_reference_button.text() == "Fijar como referencia"

    services.preferences.update(StudioPreferences(language="en"))
    window._apply_preferences()

    assert window._menus["file"].title() == "File"
    assert window._actions["solve_layout"].text() == "Calculate layout"
    assert "No selection" in window.inspector.toPlainText()
    assert window.solutions_dock.windowTitle() == "Solution comparator"
    assert window.pin_reference_button.text() == "Pin as reference"
    assert window.comparator_sort.itemText(0) == "Solver order"

    window._status("status.prefs_saved")
    assert "Preferences saved" in window.statusBar().currentMessage()


def test_project_path_status_and_reveal_action(qapp, tmp_path, monkeypatch):
    del qapp
    from studio.models import StudioBoard, StudioProject
    from studio.project_serializer import save_project

    path = tmp_path / "demo.bcproj"
    project = StudioProject(
        project_id="PRJ-1",
        name="Demo",
        boards=[StudioBoard("P1", 1000, 500, "Demo", 19, 1)],
        pieces=[],
        placements=[],
    )
    save_project(project, path)

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="en"))
    window = MainWindow(services)

    assert window._project_path_label.text() == "Project not saved yet"
    assert not window._actions["reveal_project_folder"].isEnabled()

    services.projects.open_project(project, str(path))
    window.update_window_title()

    assert str(path) in window._project_path_label.toolTip()
    assert window._project_path_label.text() == path.name
    assert window._actions["reveal_project_folder"].isEnabled()

    revealed: list[str] = []
    monkeypatch.setattr(
        "studio.file_reveal.reveal_in_file_manager",
        lambda target: revealed.append(str(target)) or True,
    )
    window._reveal_project_folder()
    assert revealed == [str(path)]


def test_menu_actions_have_status_tips(qapp, tmp_path):
    del qapp
    from studio.keyboard_shortcuts import with_native_shortcuts

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="en"))
    window = MainWindow(services)

    assert not window._actions["solve_layout"].isEnabled()
    assert (
        window._actions["solve_layout"].statusTip() == "No project to calculate layout"
    )
    assert not window._actions["fit_board"].isEnabled()
    assert window._actions["fit_board"].statusTip() == "No boards to fit the view"

    services.preferences.update(StudioPreferences(language="es"))
    window._apply_preferences()

    assert (
        window._actions["solve_layout"].statusTip()
        == "No hay proyecto para calcular layout"
    )
    assert window._actions["zoom_in"].statusTip() == with_native_shortcuts(
        "Acercar el Workspace (Ctrl+=)"
    )


def test_undo_redo_show_honest_tips_without_history(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)

    assert not window._actions["undo"].isEnabled()
    assert not window._actions["redo"].isEnabled()
    assert (
        "no hay acciones para deshacer" in window._actions["undo"].statusTip().lower()
    )
    assert "no hay acciones para rehacer" in window._actions["redo"].statusTip().lower()

    services.preferences.update(StudioPreferences(language="en"))
    window._apply_preferences()

    assert window._actions["undo"].statusTip() == "No actions to undo"
    assert window._actions["redo"].statusTip() == "No actions to redo"


def test_generate_and_compare_menus_are_populated(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="en"))
    window = MainWindow(services)

    assert "tools" not in window._menus
    assert window._menus["generate"].title() == "Generate"
    assert window._menus["compare"].title() == "Compare"

    generate_texts = [a.text() for a in window._menus["generate"].actions() if a.text()]
    compare_texts = [a.text() for a in window._menus["compare"].actions() if a.text()]
    assert "Calculate layout" in generate_texts
    assert "Previous solution" in compare_texts
    assert "Next solution" in compare_texts
    assert "Apply calculated layout" in compare_texts


def test_reload_recent_menu_prunes_missing_paths(qapp, tmp_path):
    del qapp
    from studio.recent_files import RecentFilesManager

    existing = tmp_path / "demo.bcproj"
    existing.write_text("{}", encoding="utf-8")
    missing = tmp_path / "gone.bcproj"
    recent = RecentFilesManager(path=tmp_path / "recent.json")
    recent.add(str(missing))
    recent.add(str(existing))

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json"),
        recent_files=recent,
    )
    window = MainWindow(services)
    window._reload_recent_files_menu()

    clear_label = window._tr("action.clear_recent")
    menu_labels = [
        action.text()
        for action in window._recent_menu.actions()
        if action.isEnabled()
        and not action.isSeparator()
        and action.text() != clear_label
    ]
    assert menu_labels == [existing.name]
    assert services.recent_files.files == [str(existing)]
    assert window.welcome.recent_list.count() == 1
    recent_action = next(
        action
        for action in window._recent_menu.actions()
        if action.isEnabled()
        and not action.isSeparator()
        and action.text() != clear_label
    )
    assert recent_action.text() == existing.name
    assert str(existing) in (recent_action.statusTip() or "")
    assert str(existing) in (recent_action.toolTip() or "")
    assert "Abrir" in (recent_action.statusTip() or "")


def test_recent_menu_actions_use_pinned_status_tip(qapp, tmp_path):
    del qapp
    from studio.recent_files import RecentFilesManager

    existing = tmp_path / "demo.bcproj"
    existing.write_text("{}", encoding="utf-8")
    recent = RecentFilesManager(path=tmp_path / "recent.json")
    recent.add(str(existing))
    recent.toggle_pin(str(existing))

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json"),
        recent_files=recent,
    )
    window = MainWindow(services)
    window._reload_recent_files_menu()

    clear_label = window._tr("action.clear_recent")
    recent_action = next(
        action
        for action in window._recent_menu.actions()
        if action.isEnabled()
        and not action.isSeparator()
        and action.text() != clear_label
    )
    assert recent_action.text() == f"★ {existing.name}"
    tip = recent_action.statusTip() or ""
    assert str(existing) in tip
    assert "anclado" in tip.lower()
    submenu = recent_action.menu()
    assert submenu is not None
    labels = [action.text() for action in submenu.actions()]
    assert window._tr("action.open_recent") in labels
    assert window._tr("welcome.unpin_recent") in labels
    assert window._tr("welcome.reveal_folder") in labels
    assert window._tr("welcome.remove_recent") in labels
    by_label = {action.text(): action for action in submenu.actions()}
    path = str(existing)
    assert path in (by_label[window._tr("action.open_recent")].statusTip() or "")
    assert path in (by_label[window._tr("welcome.unpin_recent")].statusTip() or "")
    assert path in (by_label[window._tr("welcome.reveal_folder")].statusTip() or "")
    assert path in (by_label[window._tr("welcome.remove_recent")].statusTip() or "")
    assert (
        "anclaje"
        in (by_label[window._tr("welcome.unpin_recent")].statusTip() or "").lower()
    )


def test_recent_menu_submenu_pin_reveal_remove(qapp, tmp_path, monkeypatch):
    del qapp
    from studio.recent_files import RecentFilesManager

    existing = tmp_path / "demo.bcproj"
    existing.write_text("{}", encoding="utf-8")
    recent = RecentFilesManager(path=tmp_path / "recent.json")
    recent.add(str(existing))

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json"),
        recent_files=recent,
    )
    window = MainWindow(services)
    window._reload_recent_files_menu()

    clear_label = window._tr("action.clear_recent")
    recent_action = next(
        action
        for action in window._recent_menu.actions()
        if action.isEnabled()
        and not action.isSeparator()
        and action.text() != clear_label
    )
    submenu = recent_action.menu()
    assert submenu is not None

    pin_action = next(
        action
        for action in submenu.actions()
        if action.text() == window._tr("welcome.pin_recent")
    )
    assert str(existing) in (pin_action.statusTip() or "")
    assert "Anclar" in (pin_action.statusTip() or "")
    pin_action.trigger()
    assert services.recent_files.is_pinned(str(existing))

    window._reload_recent_files_menu()
    recent_action = next(
        action
        for action in window._recent_menu.actions()
        if action.isEnabled()
        and not action.isSeparator()
        and action.text() != clear_label
    )
    submenu = recent_action.menu()
    assert submenu is not None

    revealed: list[str] = []
    monkeypatch.setattr(
        window,
        "_reveal_recent_file",
        lambda path: revealed.append(path),
    )
    reveal_action = next(
        action
        for action in submenu.actions()
        if action.text() == window._tr("welcome.reveal_folder")
    )
    assert str(existing) in (reveal_action.statusTip() or "")
    reveal_action.trigger()
    assert revealed == [str(existing)]

    remove_action = next(
        action
        for action in submenu.actions()
        if action.text() == window._tr("welcome.remove_recent")
    )
    assert str(existing) in (remove_action.statusTip() or "")
    remove_action.trigger()
    assert services.recent_files.files == []


def test_failed_open_recent_removes_entry(qapp, tmp_path, monkeypatch):
    del qapp
    from PySide6.QtWidgets import QMessageBox

    from studio.recent_files import RecentFilesManager

    ghost = tmp_path / "ghost.bcproj"
    ghost.write_text("{}", encoding="utf-8")
    recent = RecentFilesManager(path=tmp_path / "recent.json")
    recent.add(str(ghost))

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json"),
        recent_files=recent,
    )
    window = MainWindow(services)
    window._reload_recent_files_menu()

    monkeypatch.setattr(
        QMessageBox, "warning", lambda *args, **kwargs: QMessageBox.StandardButton.Ok
    )
    monkeypatch.setattr(
        "studio.main_window.load_project",
        lambda path: (_ for _ in ()).throw(OSError("missing")),
    )
    monkeypatch.setattr(window, "_confirm_discard_unsaved_changes", lambda: True)

    window._open_recent_project(str(ghost))

    assert services.recent_files.files == []
    assert not window.welcome.clear_recent_button.isEnabled()


def test_clear_recent_files_updates_menu_and_welcome(qapp, tmp_path, monkeypatch):
    del qapp
    from PySide6.QtWidgets import QMessageBox

    from studio.recent_files import RecentFilesManager

    project = tmp_path / "demo.bcproj"
    project.write_text("{}", encoding="utf-8")
    recent = RecentFilesManager(path=tmp_path / "recent.json")
    recent.add(str(project))

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json"),
        recent_files=recent,
    )
    window = MainWindow(services)
    window._reload_recent_files_menu()

    assert any(
        action.text() == window._tr("action.clear_recent")
        for action in window._recent_menu.actions()
    )
    assert window._actions["clear_recent"].isEnabled()
    assert window.welcome.clear_recent_button.isEnabled()

    monkeypatch.setattr(
        QMessageBox,
        "question",
        lambda *args, **kwargs: QMessageBox.StandardButton.Yes,
    )
    window._clear_recent_files()

    assert services.recent_files.files == []
    assert not window.welcome.clear_recent_button.isEnabled()
    assert any(
        action.text() == window._tr("action.no_recent")
        for action in window._recent_menu.actions()
    )
    assert not window._actions["clear_recent"].isEnabled()
    tip = window._actions["clear_recent"].statusTip().lower()
    assert "proyectos recientes" in tip or "recent projects" in tip


def test_clear_recent_shortcut_shows_honest_status_when_empty(qapp, tmp_path):
    del qapp
    from studio.recent_files import RecentFilesManager

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json"),
        recent_files=RecentFilesManager(path=tmp_path / "recent.json"),
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    window._clear_recent_files()
    assert "no hay proyectos recientes" in window.statusBar().currentMessage().lower()


def test_edit_menu_includes_select_all_pieces(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="en"))
    window = MainWindow(services)

    texts = [a.text() for a in window._menus["edit"].actions() if a.text()]
    assert "Select all pieces" in texts
    assert "Deselect pieces" in texts
    assert "Invert selection" in texts
    assert window._actions["select_all_pieces"].shortcut().toString() in {
        "Ctrl+A",
        "Meta+A",
    }
    assert window._actions["deselect_pieces"].shortcut().toString() == "Esc"
    assert window._actions["invert_selection"].shortcut().toString() in {
        "Ctrl+Shift+I",
        "Meta+Shift+I",
    }


def test_reset_window_layout_restores_toolbar_and_docks(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)

    assert window._actions["reset_window_layout"] in window._menus["view"].actions()
    assert (
        window._actions["reset_window_layout"].text()
        == "Restablecer disposición de ventana"
    )

    window._toolbar.setVisible(False)
    window.explorer_dock.setVisible(False)
    window.inspector_dock.setVisible(False)
    window._persist_window_layout()

    window._reset_window_layout()

    assert not window._toolbar.isHidden()
    assert not window.explorer_dock.isHidden()
    assert not window.inspector_dock.isHidden()
    assert not window.console_dock.isHidden()
    assert not window.solutions_dock.isHidden()
    assert "restablecida" in window.statusBar().currentMessage().casefold()

    prefs = PreferencesManager(tmp_path / "preferences.json").current
    assert prefs.window_geometry
    assert prefs.window_state


def test_window_layout_persists_geometry_and_toolbar_visibility(qapp, tmp_path):
    del qapp
    from PySide6.QtCore import QByteArray

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    window = MainWindow(services)
    window.resize(1111, 777)
    window._toolbar.setVisible(False)
    saved_geometry = window.saveGeometry()
    window._persist_window_layout()

    prefs = PreferencesManager(tmp_path / "preferences.json").current
    assert prefs.window_geometry
    assert prefs.window_state
    assert (
        QByteArray.fromBase64(prefs.window_geometry.encode("ascii")) == saved_geometry
    )

    services2 = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    restored = MainWindow(services2)
    assert restored._toolbar.isHidden()
    assert restored.restoreGeometry(saved_geometry) is True


def test_status_bar_shows_workspace_zoom_percent(qapp, tmp_path):
    del qapp
    from studio.models import StudioBoard, StudioProject

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-Z",
            name="Zoom",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[],
            placements=[],
        )
    )
    window = MainWindow(services)
    window.workspace.resize(800, 600)
    window.workspace.reload_project()

    assert window._zoom_label.objectName() == "statusZoom"
    assert window._zoom_label.text().endswith("%")
    baseline = window.workspace.zoom
    window.workspace.zoom_in()
    assert window.workspace.zoom > baseline
    assert window._zoom_label.text() == window._tr(
        "status.zoom", n=int(round(window.workspace.zoom * 100))
    )

    window.workspace.zoom_out()
    assert window._zoom_label.text() == window._tr(
        "status.zoom", n=int(round(window.workspace.zoom * 100))
    )
    assert "zoom" in window._zoom_label.toolTip().casefold()


def test_view_menu_includes_dock_toggles(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)

    view_actions = window._menus["view"].actions()
    for key in ("explorer", "inspector", "timeline", "comparator"):
        action = window._dock_toggles[key]
        assert action in view_actions
        assert action.isCheckable()
        assert action.text() == window._tr(f"dock.{key}")

    window.explorer_dock.setVisible(False)
    assert window.explorer_dock.isHidden()
    assert not window._dock_toggles["explorer"].isChecked()

    window._dock_toggles["explorer"].trigger()
    assert not window.explorer_dock.isHidden()
    assert window._dock_toggles["explorer"].isChecked()

    services.preferences.update(StudioPreferences(language="en"))
    window._apply_preferences()
    assert window._dock_toggles["inspector"].text() == "Inspector"
    assert "Explorer" in window._dock_toggles["explorer"].statusTip()


def test_main_toolbar_reuses_core_actions(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="en"))
    window = MainWindow(services)

    assert window._toolbar.objectName() == "mainToolbar"
    assert window._toolbar.windowTitle() == "Main toolbar"
    toolbar_actions = set(window._toolbar.actions())
    assert window._actions["solve_layout"] in toolbar_actions
    assert window._actions["export_selected"] in toolbar_actions
    assert window._actions["fit_board"] in toolbar_actions
    assert window._toolbar_toggle in window._menus["view"].actions()
    assert window._toolbar_toggle.text() == "Toolbar"


def test_view_menu_includes_zoom_actions(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="en"))
    window = MainWindow(services)

    texts = [a.text() for a in window._menus["view"].actions() if a.text()]
    assert "Zoom in" in texts
    assert "Zoom out" in texts
    assert "Fit to board" in texts


def test_fit_board_action_gated_without_boards(qapp, tmp_path):
    del qapp
    from studio.models import StudioBoard, StudioProject

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)

    assert not window._actions["fit_board"].isEnabled()
    assert "no hay tableros" in window._actions["fit_board"].statusTip().lower()

    services.projects.new_project(
        StudioProject(
            project_id="PRJ-FIT",
            name="Fit",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[],
            placements=[],
        )
    )
    window.update_window_title()
    assert window._actions["fit_board"].isEnabled()
    tip = window._actions["fit_board"].statusTip()
    assert "Ctrl+0" in tip or "⌘0" in tip


def test_fit_selection_action_gated_until_selection_or_focus(qapp, tmp_path):
    del qapp
    from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-SEL",
            name="Sel",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("P1", 200, 100, "Demo", 19)],
            placements=[StudioPlacement("P1", 0, 0, False, 0, "B1", 0, 0)],
        )
    )
    window = MainWindow(services)
    window.workspace.resize(800, 600)
    window.workspace.reload_project()
    window.workspace.clear_piece_selection()
    window._sync_view_actions()

    assert not window._actions["fit_selection"].isEnabled()
    assert (
        "selecciona una pieza" in window._actions["fit_selection"].statusTip().lower()
    )

    window.workspace.focus_board("B1")
    assert window._actions["fit_selection"].isEnabled()
    tip = window._actions["fit_selection"].statusTip()
    assert "Ctrl+Shift+0" in tip or "⇧⌘0" in tip


def test_solve_layout_action_enabled_with_project(qapp, tmp_path):
    del qapp
    from studio.models import StudioBoard, StudioPiece, StudioProject

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="en"))
    window = MainWindow(services)
    assert not window._actions["solve_layout"].isEnabled()

    services.projects.new_project(StudioProject(project_id="PRJ-SOLVE", name="Solve"))
    window.update_window_title()
    assert not window._actions["solve_layout"].isEnabled()
    assert "board" in window._actions["solve_layout"].statusTip().lower()

    project = services.projects.current_project
    assert project is not None
    project.boards.append(StudioBoard("B1", 1000, 500, "Demo", 19, 1))
    window.update_window_title()
    assert not window._actions["solve_layout"].isEnabled()
    assert "piece" in window._actions["solve_layout"].statusTip().lower()

    project.pieces.append(StudioPiece("A", 200, 100, "Demo", 19))
    window.update_window_title()
    assert window._actions["solve_layout"].isEnabled()
    tip = window._actions["solve_layout"].statusTip()
    assert "Ctrl+Return" in tip or "⌘↵" in tip


def test_view_menu_fit_and_grid_toggle(qapp, tmp_path):
    del qapp
    from studio.models import StudioBoard, StudioProject

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="en", show_grid=True))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="View menu",
            boards=[StudioBoard("P1", 1000, 500, "Demo", 19, 1)],
            pieces=[],
            placements=[],
        )
    )

    window = MainWindow(services)
    window.resize(960, 720)
    window.workspace.resize(800, 600)
    window.show()
    window.workspace.reload_project()

    assert window._menus["view"].actions()
    assert window._actions["fit_board"].text() == "Fit to board"
    assert window._actions["toggle_grid"].isCheckable()
    assert window._actions["toggle_grid"].isChecked()

    assert len(window.workspace.scene().items()) > 1

    window._actions["toggle_grid"].setChecked(False)
    assert services.preferences.current.show_grid is False
    # Only the board rect remains when the grid is hidden.
    assert len(window.workspace.scene().items()) == 1

    window.workspace._camera.zoom = window.workspace._camera.clamp_zoom(3.0)
    window.workspace._apply_camera()
    zoomed = window.workspace._camera.zoom
    window._fit_board()
    assert window.workspace._camera.zoom != zoomed
