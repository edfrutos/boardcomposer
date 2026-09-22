"""Comparator lengths follow prefs.units (IDE-0047). Storage stays mm."""

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from studio.solution_diff import compare_solutions


def _window(tmp_path, *, units: str = "mm") -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es", units=units))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Unidades",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 100, 50, "Demo", 19)],
            placements=[StudioPlacement("A", 0, 0, False, 0, "B1", 0, 0)],
        )
    )
    services.layout.solutions = [
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)]),
        AssemblySolution(placements=[BoardPlacement("A", 200, 100, 400, 200)]),
    ]
    services.layout.select_solution(1)
    window = MainWindow(services)
    window.workspace.reload_project()
    window._reload_solution_table()
    return window


def test_comparator_table_keeps_mm_integers(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, units="mm")
    assert window.solutions_table.item(0, 5).text() == "100"
    assert window.solutions_table.item(0, 6).text() == "50"
    assert window.solutions_table.item(1, 5).text() == "400"
    assert window.solutions_table.item(1, 6).text() == "200"


def test_comparator_table_uses_centimetres(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, units="cm")
    assert window.solutions_table.item(0, 5).text() == "10 cm"
    assert window.solutions_table.item(0, 6).text() == "5 cm"
    assert window.solutions_table.item(1, 5).text() == "40 cm"
    assert window.solutions_table.item(1, 6).text() == "20 cm"


def test_comparator_diff_converts_lengths_and_placements(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, units="cm")
    window._reload_solution_differences()
    text = window.solution_differences.toPlainText()
    assert "Largo total: 10 cm → 40 cm" in text
    assert "Ancho total: 5 cm → 20 cm" in text
    assert "20 cm, 10 cm" in text
    assert "40x20 cm" in text
    assert " mm" not in text


def test_compare_solutions_default_mm_keeps_placement_text():
    reference = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 10, 10)])
    candidate = AssemblySolution(placements=[BoardPlacement("A", 5, 0, 10, 10)])
    diff = compare_solutions(
        reference,
        candidate,
        reference_index=0,
        candidate_index=1,
    )
    moved = next(change for change in diff.placements if change.kind == "moved")
    assert "(0, 0) 10×10 mm" in moved.detail
    assert "(5, 0) 10×10 mm" in moved.detail
