"""Status hint when max_solutions truncates visible candidates."""

from boardcomposer.domain import AssemblySolution, BoardPlacement

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def test_warn_when_more_accepted_than_shown(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es", max_solutions=1))
    window = MainWindow(services)

    services.layout.stats.accepted = 3
    services.layout.solutions = [
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 10, 10)])
    ]

    window._maybe_warn_solution_truncated_by_limit(shown=1)
    message = window.statusBar().currentMessage()
    assert "1/3" in message
    assert "límite" in message
