"""Piece Inspector shows thickness, rotation and grain (IDE-0046)."""

from boardcomposer.domain.grain import GRAIN_LOCKED
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path, *, grain: str = "none", placed: bool = True) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    placements = []
    if placed:
        placements.append(StudioPlacement("A", 10, 20, False, 0, "B1", 0, 0))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Meta",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 400, 300, "Demo", 19, grain=grain)],
            placements=placements,
        )
    )
    window = MainWindow(services)
    window.workspace.reload_project()
    return window


def test_placed_piece_inspector_shows_thickness_rotation_and_grain(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, grain="none", placed=True)
    window.refresh_inspector_for_piece("A")
    text = window.inspector.toPlainText()
    assert "Espesor: 19 mm" in text
    assert "Rotación: 0°" in text
    assert "Veta: libre (puede rotar)" in text


def test_unplaced_piece_inspector_shows_empty_rotation_and_locked_grain(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, grain=GRAIN_LOCKED, placed=False)
    window.refresh_inspector_for_piece("A")
    text = window.inspector.toPlainText()
    assert "Espesor: 19 mm" in text
    assert "Rotación: —" in text
    assert "Veta: fija (no rotar)" in text
    assert "Sin colocar" in text


def test_rotate_updates_inspector_rotation(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, placed=True)
    window.workspace.select_piece("A")
    window._rotate_selected_piece()
    text = window.inspector.toPlainText()
    assert "Rotación: 90°" in text
    assert "Espesor: 19 mm" in text
