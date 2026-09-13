"""Studio cut-list export enablement, write, and format memory."""

from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.main_window import MainWindow
from studio.models import StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    return MainWindow(services)


def _sol() -> AssemblySolution:
    return AssemblySolution(placements=[BoardPlacement("A", 10, 20, 400, 300)])


def test_cut_list_export_writes_csv_and_remembers_folder(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    window.services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Cocina",
            client="ACME",
            reference="PED-1",
            kerf_mm=3.2,
        )
    )
    window.services.layout.solutions = [_sol()]
    window.services.layout.selected_solution_index = 0
    window._reload_solution_table()

    target = tmp_path / "out" / "lista.csv"
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
        lambda *args, **kwargs: (str(target), "CSV (*.csv)"),
    )

    window._export_cut_list()

    assert target.is_file()
    text = target.read_text(encoding="utf-8")
    assert "Cocina" in text and "ACME" in text and "3.2" in text
    assert "section,id" in text
    assert offered == [target]
    prefs = window.services.preferences.current
    assert prefs.cut_list_export_format == "csv"
    assert prefs.last_export_directory == str(target.parent.resolve())


def test_cut_list_export_remembers_pdf_format(qapp, tmp_path, monkeypatch):
    del qapp
    prefs_path = tmp_path / "preferences.json"
    services = StudioServices(preferences=PreferencesManager(prefs_path))
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    window.services.layout.solutions = [_sol()]
    window.services.layout.selected_solution_index = 0
    window._reload_solution_table()

    target = tmp_path / "lista.pdf"
    monkeypatch.setattr(window, "_offer_open_exported_path", lambda path: None)
    monkeypatch.setattr(
        QFileDialog,
        "getSaveFileName",
        lambda *args, **kwargs: (str(target), "PDF (*.pdf)"),
    )

    window._export_cut_list()

    assert target.is_file()
    assert target.read_bytes().startswith(b"%PDF")
    assert services.preferences.current.cut_list_export_format == "pdf"

    services2 = StudioServices(preferences=PreferencesManager(prefs_path))
    window2 = MainWindow(services2)
    window2.services.layout.solutions = [_sol()]
    window2.services.layout.selected_solution_index = 0
    window2._reload_solution_table()

    filters: list[str] = []

    def _fake_save(*args, **kwargs):
        filters.append(str(args[3] if len(args) > 3 else kwargs.get("filter", "")))
        return "", ""

    monkeypatch.setattr(QFileDialog, "getSaveFileName", _fake_save)
    window2._export_cut_list()
    assert filters and filters[0].startswith("PDF")
