"""Project/category Inspector shows counts and areas (IDE-0050)."""

from boardcomposer.domain import AssemblySolution, BoardPlacement, PanelReference
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path, *, units: str = "mm", language: str = "es") -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language=language, units=units))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Resumen",
            client="Taller Norte",
            reference="PED-9",
            notes="Puerta",
            kerf_mm=3.2,
            boards=[
                StudioBoard("B1", 1000, 500, "Roble", 19, 2),
                StudioBoard("R1", 400, 300, "Pino", 19, 1, remnant=True),
            ],
            pieces=[
                StudioPiece("A", 400, 300, "Roble", 19),
                StudioPiece("B", 200, 100, "Pino", 19),
            ],
            placements=[StudioPlacement("A", 0, 0, False, 0, "B1", 0, 0)],
        )
    )
    window = MainWindow(services)
    window.workspace.reload_project()
    window._reload_explorer()
    return window


def test_project_inspector_shows_counts_and_metadata(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window._show_project_inspector()
    text = window.inspector.toPlainText()
    assert "Proyecto: Resumen" in text
    assert "Cliente: Taller Norte" in text
    assert "Referencia: PED-9" in text
    assert "Notas: Puerta" in text
    assert "Espesor de sierra: 3.2 mm" in text
    assert "Tableros: 2 tipos · 3 físicos" in text
    assert "Piezas: 2 (1 colocadas, 1 sin colocar)" in text
    assert "Soluciones: 0" in text
    assert "Materiales: Roble, Pino" in text
    assert "Área de stock: 1120000 mm²" in text


def test_boards_category_inspector_counts_physical_and_remnants(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window._show_category_inspector("boards")
    text = window.inspector.toPlainText()
    assert "Tableros" in text
    assert "Tipos: 2" in text
    assert "Físicos: 3" in text
    assert "Retales de inventario: 1" in text
    assert "Materiales: Roble, Pino" in text
    assert "Área de stock: 1120000 mm²" in text


def test_pieces_category_inspector_counts_placed_and_area(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, units="cm")
    window._show_category_inspector("pieces")
    text = window.inspector.toPlainText()
    assert "Piezas" in text
    assert "Total: 2" in text
    assert "Colocadas: 1" in text
    assert "Sin colocar: 1" in text
    assert "Materiales: Roble, Pino" in text
    assert "Área de piezas: 1400 cm²" in text
    assert " mm" not in text


def test_solutions_category_inspector_empty_and_selected(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window._show_category_inspector("solutions")
    empty = window.inspector.toPlainText()
    assert "Candidatas: 0" in empty
    assert "Sin candidatas calculadas" in empty

    window.services.layout.solutions = [
        AssemblySolution(
            placements=[
                BoardPlacement(
                    "A", 0, 0, 400, 300, panel_reference=PanelReference(0, 0)
                )
            ]
        )
    ]
    window.services.layout.selected_solution_index = 0
    window.services.layout.solutions_outdated = True
    window._show_category_inspector("solutions")
    text = window.inspector.toPlainText()
    assert "Candidatas: 1" in text
    assert "Seleccionada: 1 / 1" in text
    assert "pendientes de regeneración" in text


def test_explorer_category_selection_fills_inspector(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    item = window._find_explorer_item_by_role("category:boards")
    assert item is not None
    window.explorer.setCurrentItem(item)
    text = window.inspector.toPlainText()
    assert "Físicos: 3" in text
    assert "Retales de inventario: 1" in text


def test_refresh_keeps_category_inspector(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    item = window._find_explorer_item_by_role("category:pieces")
    assert item is not None
    window.explorer.setCurrentItem(item)
    window._refresh_inspector_from_context()
    text = window.inspector.toPlainText()
    assert "Colocadas: 1" in text
    assert "Sin colocar: 1" in text
