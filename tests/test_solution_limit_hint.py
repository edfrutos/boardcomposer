"""Status hints for layout cardinality (single vs truncated)."""

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


def test_warn_when_more_accepted_than_shown(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, max_solutions=1)
    window.services.layout.stats.accepted = 3
    window.services.layout.solutions = [
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 10, 10)])
    ]

    window._maybe_warn_solution_truncated_by_limit(shown=1)
    message = window.statusBar().currentMessage()
    assert "1/3" in message
    assert "límite" in message


def test_announce_single_candidate_explains_no_more(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, max_solutions=20)
    window.services.layout.stats.generated = 4
    window.services.layout.stats.unique = 2
    window.services.layout.stats.accepted = 1
    window.services.layout.solutions = [
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 10, 10)])
    ]

    window._announce_layout_ok(shown=1)
    message = window.statusBar().currentMessage()
    assert "única candidata" in message
    assert "no hay más" in message
    assert "Ctrl+Shift+D" in message or "⇧⌘D" in message
    assert "4" in message
    assert "2" in message


def test_announce_multiple_keeps_count_message(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, max_solutions=20)
    window.services.layout.stats.accepted = 5

    window._announce_layout_ok(shown=5)
    message = window.statusBar().currentMessage()
    assert "5 soluciones" in message
    assert "única" not in message
