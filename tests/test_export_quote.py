"""Studio quote PDF export (IDE-0032)."""

from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from boardcomposer import Board, Project, StockPanel
from boardcomposer.domain import AssemblySolution, BoardPlacement, PanelReference
from studio.main_window import MainWindow
from studio.material_catalog import CatalogMaterial
from studio.models import StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    return MainWindow(services)


def test_quote_export_writes_pdf_and_remembers_folder(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    window.services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Cocina",
            client="ACME",
            reference="PED-1",
        )
    )
    window.services.material_catalog.replace_all(
        [CatalogMaterial("Melamina", (19.0,), price_per_m2=25.0)]
    )
    core = Project()
    core.add_stock_panel(StockPanel(1000, 500, 19, "P1", material="Melamina"))
    core.add_board(Board(400, 300, 19, "A", material="Melamina"))
    window.services.layout._solved_project = core
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
    window._reload_solution_table()

    target = tmp_path / "out" / "presupuesto.pdf"
    target.parent.mkdir()
    offered: list[Path] = []
    monkeypatch.setattr(
        window,
        "_offer_open_exported_path",
        lambda path: offered.append(Path(path)),
    )
    monkeypatch.setattr(
        QFileDialog,
        "getSaveFileName",
        lambda *args, **kwargs: (str(target), "PDF (*.pdf)"),
    )

    window._export_quote()

    assert target.is_file()
    payload = target.read_bytes()
    assert payload.startswith(b"%PDF")
    assert b"Cocina" in payload
    assert b"ACME" in payload
    assert b"12.50 EUR" in payload
    assert offered == [target]
    prefs = window.services.preferences.current
    assert prefs.last_export_directory == str(target.parent.resolve())
    assert window._actions["export_quote"].isEnabled()
    assert window._actions["export_quote"].text() == "Exportar presupuesto…"
