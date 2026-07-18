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
