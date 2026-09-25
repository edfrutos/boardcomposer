"""Piece Inspector shows area (IDE-0055)."""

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def test_piece_inspector_shows_area_in_mm(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es", units="mm"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Área",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 400, 300, "Demo", 19)],
        )
    )
    window = MainWindow(services)
    window.refresh_inspector_for_piece("A")
    assert "Área: 120000 mm²" in window.inspector.toPlainText()
