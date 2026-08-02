"""Enablement for export-revision-backup and explain-candidate actions."""

from __future__ import annotations

from boardcomposer.domain import AssemblySolution, BoardPlacement, SolutionExplanation
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.project_serializer import save_project
from studio.services import StudioServices


def _window(tmp_path, *, with_file: bool = False) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    project = StudioProject(
        project_id="PRJ-P",
        name="Pilot",
        boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
        pieces=[StudioPiece("A", 100, 50, "Demo", 19)],
        placements=[],
    )
    if with_file:
        path = tmp_path / "demo.bcproj"
        save_project(project, path)
        services.projects.open_project(project, str(path))
    else:
        services.projects.new_project(project)
    window = MainWindow(services)
    window.update_window_title()
    return window


def test_export_revision_backup_requires_saved_file(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, with_file=False)
    action = window._actions["export_revision_backup"]
    assert not action.isEnabled()
    assert "guarda" in action.statusTip().lower()

    window = _window(tmp_path, with_file=True)
    action = window._actions["export_revision_backup"]
    assert action.isEnabled()
    assert "backup" in action.statusTip().lower() or ".revs" in action.statusTip()


def test_explain_solution_requires_candidate(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, with_file=True)
    explain = window._actions["explain_solution"]
    window.services.layout.solutions = []
    window._reload_solution_table()
    assert not explain.isEnabled()

    window.services.layout.solutions = [
        AssemblySolution(
            placements=[BoardPlacement("A", 0, 0, 100, 50)],
            explanation=SolutionExplanation(strengths=["ok"], notes=["demo"]),
        )
    ]
    window._reload_solution_table()
    assert explain.isEnabled()
    tip = explain.statusTip().lower()
    assert "fortaleza" in tip or "candidata" in tip or "debilidades" in tip
    assert "copiar" in tip
