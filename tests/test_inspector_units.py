"""Inspector lengths/areas follow prefs.units (IDE-0040). Storage stays mm."""

from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    Offcut,
    PanelReference,
)
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path, *, units: str) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es", units=units))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Unidades",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 400, 300, "Demo", 19)],
            placements=[StudioPlacement("A", 0, 0, False, 0, "B1", 0, 0)],
        )
    )
    window = MainWindow(services)
    window.workspace.reload_project()
    window._reload_explorer()
    return window


def test_board_inspector_uses_centimetres(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, units="cm")
    window._show_board_inspector("B1")
    text = window.inspector.toPlainText()
    assert "100 x 50 cm" in text
    assert "1.9 cm" in text


def test_piece_inspector_uses_inches(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, units="in")
    window.refresh_inspector_for_piece("A")
    text = window.inspector.toPlainText()
    assert "15.75 x 11.81 in" in text
    assert "0.75 in" in text


def test_layout_inspector_converts_length_and_area(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, units="cm")
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 1000, 500, panel_reference=PanelReference(0, 0))
        ],
        offcuts=(Offcut(PanelReference(0, 0), 0, 0, 200, 100),),
    )
    window._show_layout_solution(solution)
    text = window.inspector.toPlainText()
    assert "Largo total: 100 cm" in text
    assert "Ancho total: 50 cm" in text
    assert "área total 200 cm²" in text
    assert " mm" not in text
    assert "mm²" not in text
