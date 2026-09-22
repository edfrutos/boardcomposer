"""Board Inspector shows panel utilization (IDE-0051)."""

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


def _window(tmp_path, *, units: str = "mm", placed: bool = False) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es", units=units))
    placements = []
    if placed:
        placements.append(StudioPlacement("A", 0, 0, False, 0, "B1", 0, 0))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Uso",
            boards=[
                StudioBoard("B1", 1000, 500, "Roble", 19, 2),
                StudioBoard("B2", 800, 400, "Pino", 19, 1),
            ],
            pieces=[StudioPiece("A", 400, 300, "Roble", 19)],
            placements=placements,
        )
    )
    window = MainWindow(services)
    window.workspace.reload_project()
    return window


def test_board_inspector_without_layout_says_empty(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window._show_board_inspector("B1")
    text = window.inspector.toPlainText()
    assert "Tablero: B1" in text
    assert "Sin layout en este tablero" in text


def test_board_inspector_uses_applied_placements(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, placed=True)
    window._show_board_inspector("B1")
    text = window.inspector.toPlainText()
    assert "Instancias usadas: 1 / 2" in text
    assert "Piezas colocadas: 1" in text
    assert "Aprovechamiento: 24.0%" in text
    assert "Material libre: 76.0%" in text


def test_board_inspector_uses_selected_solution_and_offcuts(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, units="cm")
    window.services.layout.solutions = [
        AssemblySolution(
            placements=[
                BoardPlacement(
                    "A",
                    0,
                    0,
                    400,
                    300,
                    panel_reference=PanelReference(0, 0),
                )
            ],
            offcuts=(Offcut(PanelReference(0, 0), 400, 0, 200, 100),),
        )
    ]
    window.services.layout.selected_solution_index = 0
    window._show_board_inspector("B1")
    text = window.inspector.toPlainText()
    assert "Instancias usadas: 1 / 2" in text
    assert "Aprovechamiento: 24.0%" in text
    assert "área total 200 cm²" in text
    assert " mm" not in text


def test_unused_board_in_solution_reports_zero_instances(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = [
        AssemblySolution(
            placements=[
                BoardPlacement(
                    "A",
                    0,
                    0,
                    400,
                    300,
                    panel_reference=PanelReference(0, 0),
                )
            ]
        )
    ]
    window.services.layout.selected_solution_index = 0
    window._show_board_inspector("B2")
    text = window.inspector.toPlainText()
    assert "Instancias usadas: 0 / 1" in text
    assert "Sin piezas en este tablero" in text
    assert "Aprovechamiento:" not in text
