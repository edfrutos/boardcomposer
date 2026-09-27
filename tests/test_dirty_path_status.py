"""Unsaved marker on the status-bar project path (IDE-0058)."""

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.project_serializer import save_project
from studio.services import StudioServices


def test_path_label_shows_dirty_marker(qapp, tmp_path):
    del qapp
    path = tmp_path / "taller.bcproj"
    project = StudioProject(
        project_id="PRJ-1",
        name="Taller",
        boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
    )
    save_project(project, path)
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    services.projects.open_project(project, str(path))
    window.update_window_title()
    assert window._project_path_label.text() == path.name

    services.projects.mark_modified()
    window.update_window_title()
    assert window._project_path_label.text() == f"● {path.name}"
    assert "sin guardar" in window._project_path_label.toolTip().casefold()

    services.projects.mark_saved(str(path))
    window.update_window_title()
    assert window._project_path_label.text() == path.name
