"""Board Inspector shows one-sheet area (IDE-0059)."""

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def test_board_inspector_area_ignores_quantity(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es", units="mm"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Hoja",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 2)],
        )
    )
    window = MainWindow(services)
    window._show_board_inspector("B1")
    text = window.inspector.toPlainText()
    assert "Área: 500000 mm²" in text
    assert "1000000" not in text
