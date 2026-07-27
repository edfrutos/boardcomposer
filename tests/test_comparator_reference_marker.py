"""Pinned comparator reference is visible in the table (SCR-003)."""

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window_with_solutions(tmp_path):
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es", theme="light"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Solutions",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 100, 50, "Demo", 19)],
            placements=[StudioPlacement("A", 0, 0, False, 0, "B1", 0, 0)],
        )
    )
    services.layout.solutions = [
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)]),
        AssemblySolution(placements=[BoardPlacement("A", 200, 100, 100, 50)]),
    ]
    services.layout.select_solution(1)
    window = MainWindow(services)
    window.workspace.reload_project()
    window._reload_solution_table()
    return window, services


def test_pin_reference_marks_table_and_thumbnail(qapp, tmp_path):
    del qapp
    window, services = _window_with_solutions(tmp_path)

    assert window.solutions_table.item(1, 0).text() == "2"
    assert window.solution_thumbnails.item(1).text() == "#2"

    window._pin_selected_as_reference()

    assert window._comparator_reference_pinned is True
    assert window._comparator_reference_index == 1
    assert window.solutions_table.item(1, 0).text() == "Ref 2"
    assert "Referencia fijada" in window.solutions_table.item(1, 0).toolTip()
    assert window.solution_thumbnails.item(1).text() == "#2 · ref"
    assert window.solutions_table.item(0, 0).text() == "1"
    assert window.solution_thumbnails.item(0).text() == "#1"
    assert services.layout.selected_solution_index == 1
