"""PgUp/PgDown status when only one candidate is visible."""

from boardcomposer.domain import AssemblySolution, BoardPlacement

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path, *, max_solutions: int = 20) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(
        StudioPreferences(language="es", max_solutions=max_solutions)
    )
    return MainWindow(services)


def test_step_with_single_visible_explains_no_neighbor(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.stats.accepted = 1
    window.services.layout.solutions = [
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 10, 10)])
    ]
    window.services.layout.selected_solution_index = 0
    window._solution_display_indexes = [0]

    window._step_layout_solution(1)
    message = window.statusBar().currentMessage()
    assert "1 candidata" in message
    assert "Re Pág" in message or "Av Pág" in message


def test_step_with_empty_filter_but_cached_solutions(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = [
        AssemblySolution(
            placements=[BoardPlacement("A", 0, 0, 10, 10)],
            omitted_piece_ids=("B",),
        )
    ]
    window._solution_display_indexes = []
    window._comparator_complete_only = True

    window._step_layout_solution(1)
    assert "filtro" in window.statusBar().currentMessage()


def test_step_with_no_solutions_at_all(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = []
    window._solution_display_indexes = []

    window._step_layout_solution(-1)
    assert "No hay soluciones" in window.statusBar().currentMessage()
