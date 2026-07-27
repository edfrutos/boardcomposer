"""Demo project raises max_solutions when UAT would see only one candidate."""

from studio.main_window import MainWindow
from studio.preferences import (
    DEFAULT_MAX_SOLUTIONS,
    PreferencesManager,
    StudioPreferences,
)
from studio.services import StudioServices


def _window(tmp_path, *, max_solutions: int) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(
        StudioPreferences(language="es", max_solutions=max_solutions)
    )
    return MainWindow(services)


def test_demo_raises_max_solutions_when_too_low(qapp, tmp_path, monkeypatch):
    window = _window(tmp_path, max_solutions=1)
    monkeypatch.setattr(window, "_confirm_discard_unsaved_changes", lambda: True)
    monkeypatch.setattr(window, "_show_workspace", lambda: None)

    window._new_demo_project()

    assert window.services.preferences.current.max_solutions == DEFAULT_MAX_SOLUTIONS
    assert window.services.projects.current_project is not None
    assert window.services.projects.current_project.project_id == "PRJ-DEMO-001"


def test_demo_keeps_max_solutions_when_already_multi(qapp, tmp_path, monkeypatch):
    window = _window(tmp_path, max_solutions=5)
    monkeypatch.setattr(window, "_confirm_discard_unsaved_changes", lambda: True)
    monkeypatch.setattr(window, "_show_workspace", lambda: None)

    window._new_demo_project()

    assert window.services.preferences.current.max_solutions == 5


def test_demo_solve_yields_multiple_candidates(qapp, tmp_path, monkeypatch):
    window = _window(tmp_path, max_solutions=1)
    monkeypatch.setattr(window, "_confirm_discard_unsaved_changes", lambda: True)
    monkeypatch.setattr(window, "_show_workspace", lambda: None)

    window._new_demo_project()
    window.services.layout.solve_current_project()

    assert len(window.services.layout.solutions) >= 2
