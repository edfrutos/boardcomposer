"""Guard Calcular layout until boards and pieces exist."""

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path, project: StudioProject | None = None) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    if project is not None:
        services.projects.new_project(project)
    window = MainWindow(services)
    window.update_window_title()
    return window


def test_solve_layout_status_without_inventory(qapp, tmp_path):
    del qapp
    window = _window(
        tmp_path,
        StudioProject(project_id="PRJ-1", name="Empty", boards=[], pieces=[]),
    )

    window._solve_layout()

    assert window._tr("status.solve_needs_inventory") in (
        window.statusBar().currentMessage()
    )


def test_solve_layout_status_without_pieces(qapp, tmp_path):
    del qapp
    window = _window(
        tmp_path,
        StudioProject(
            project_id="PRJ-1",
            name="BoardsOnly",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[],
        ),
    )

    window._solve_layout()

    assert window._tr("status.solve_needs_pieces") in (
        window.statusBar().currentMessage()
    )
