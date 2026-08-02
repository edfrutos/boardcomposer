"""Tests for marking layout solutions outdated after project edits (FLW-006)."""

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.events.catalog import PROJECT_MODIFIED, SOLUTIONS_MARKED_OUTDATED
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _fake_solution() -> AssemblySolution:
    return AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
    )


def test_mark_project_modified_flags_existing_solutions():
    services = StudioServices()
    seen: list[str] = []
    services.events.subscribe(
        "*",
        lambda name, _payload: seen.append(name),
    )

    services.layout.solutions = [_fake_solution()]
    assert services.layout.solutions_outdated is False

    marked = services.mark_project_modified(reason="test")
    assert marked is True
    assert services.layout.solutions_outdated is True
    assert services.projects.is_modified is True
    assert PROJECT_MODIFIED in seen
    assert SOLUTIONS_MARKED_OUTDATED in seen

    # Second edit does not re-emit SolutionsMarkedOutdated.
    seen.clear()
    marked_again = services.mark_project_modified(reason="test-2")
    assert marked_again is False
    assert PROJECT_MODIFIED in seen
    assert SOLUTIONS_MARKED_OUTDATED not in seen


def test_mark_project_modified_skips_layout_when_requested():
    services = StudioServices()
    services.layout.solutions = [_fake_solution()]

    marked = services.mark_project_modified(
        affects_layout=False,
        reason="apply",
    )
    assert marked is False
    assert services.layout.solutions_outdated is False
    assert services.projects.is_modified is True


def test_solve_clears_outdated_flag():
    services = StudioServices()
    services.layout.solutions = [_fake_solution()]
    services.layout.solutions_outdated = True
    services.layout.clear_solutions()
    assert services.layout.solutions_outdated is False


def test_outdated_banner_shows_recalculate_cta(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    project = StudioProject(
        project_id="PRJ-O",
        name="Outdated",
        boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
        pieces=[StudioPiece("A", 100, 50, "Demo", 19)],
        placements=[],
    )
    services.projects.new_project(project)
    window = MainWindow(services)
    assert window.solutions_outdated_row.isHidden()

    services.layout.solutions = [_fake_solution()]
    window._mark_project_modified(reason="edit")
    assert not window.solutions_outdated_row.isHidden()
    assert window.solutions_outdated_recalculate.objectName() == "primaryButton"
    assert window.solutions_outdated_recalculate.minimumHeight() >= 36
    assert "Calcular" in window.solutions_outdated_recalculate.text()
    tip = window.solutions_outdated_recalculate.toolTip()
    assert "Ctrl+Return" in tip or "⌘↩" in tip or "layout" in tip.lower()

    apply_tip = window._actions["apply_layout"].statusTip().lower()
    assert "desactualiz" in apply_tip or "recalcul" in apply_tip
    assert "banner" in window._tr("dialog.outdated_solutions_apply").lower()
