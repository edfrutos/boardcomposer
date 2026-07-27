"""Enable/disable apply/export/prev-next based on solution availability."""

from boardcomposer.domain import AssemblySolution, BoardPlacement

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es", max_solutions=20))
    return MainWindow(services)


def _sol() -> AssemblySolution:
    return AssemblySolution(placements=[BoardPlacement("A", 0, 0, 10, 10)])


def test_solution_actions_disabled_without_solutions(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = []
    window._reload_solution_table()

    assert not window._actions["apply_layout"].isEnabled()
    assert not window._actions["export_selected"].isEnabled()
    assert not window._actions["previous_solution"].isEnabled()
    assert not window._actions["next_solution"].isEnabled()


def test_solution_actions_single_candidate(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = [_sol()]
    window.services.layout.selected_solution_index = 0
    window._reload_solution_table()

    assert window._actions["apply_layout"].isEnabled()
    assert window._actions["export_selected"].isEnabled()
    assert not window._actions["previous_solution"].isEnabled()
    assert not window._actions["next_solution"].isEnabled()


def test_solution_actions_multiple_candidates(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.layout.solutions = [_sol(), _sol()]
    window.services.layout.selected_solution_index = 0
    window._reload_solution_table()

    assert window._actions["apply_layout"].isEnabled()
    assert window._actions["export_selected"].isEnabled()
    assert window._actions["previous_solution"].isEnabled()
    assert window._actions["next_solution"].isEnabled()
