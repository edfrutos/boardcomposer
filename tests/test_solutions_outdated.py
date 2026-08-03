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

    services.layout.solutions = [_fake_solution(), _fake_solution()]
    window._mark_project_modified(reason="edit")
    assert not window.solutions_outdated_row.isHidden()
    assert window.solutions_outdated_recalculate.objectName() == "primaryButton"
    assert window.solutions_outdated_recalculate.minimumHeight() >= 36
    assert "Calcular" in window.solutions_outdated_recalculate.text()
    tip = window.solutions_outdated_recalculate.toolTip()
    assert "Ctrl+Return" in tip or "⌘↩" in tip or "layout" in tip.lower()

    apply_tip = window._actions["apply_layout"].statusTip().lower()
    assert "desactualiz" in apply_tip or "recalcul" in apply_tip
    export_tip = window._actions["export_selected"].statusTip().lower()
    assert "desactualiz" in export_tip or "recalcul" in export_tip
    explain = window._actions["explain_solution"]
    explain_tip = explain.statusTip().lower()
    assert "desactualiz" in explain_tip or "vieja" in explain_tip
    prev_tip = window._actions["previous_solution"].statusTip().lower()
    assert "desactualiz" in prev_tip or "viejas" in prev_tip
    next_tip = window._actions["next_solution"].statusTip().lower()
    assert "desactualiz" in next_tip or "viejas" in next_tip
    pin_tip = window.pin_reference_button.statusTip().lower()
    assert "desactualiz" in pin_tip or "viejas" in pin_tip
    body = window._tr("dialog.outdated_solutions_apply").lower()
    assert "recalcul" in body or "segura" in body
    assert "todos modos" in window._tr("dialog.outdated_solutions_apply_anyway").lower()
    export_body = window._tr("dialog.outdated_solutions_export").lower()
    assert "recalcul" in export_body or "segura" in export_body
    assert (
        "todos modos" in window._tr("dialog.outdated_solutions_export_anyway").lower()
    )


def test_apply_while_outdated_recalculate_choice(qapp, tmp_path, monkeypatch):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    project = StudioProject(
        project_id="PRJ-A",
        name="Apply",
        boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
        pieces=[StudioPiece("A", 100, 50, "Demo", 19)],
        placements=[],
    )
    services.projects.new_project(project)
    window = MainWindow(services)
    services.layout.solutions = [_fake_solution()]
    services.layout.selected_solution_index = 0
    window._mark_project_modified(reason="edit")

    calls: list[str] = []
    monkeypatch.setattr(window, "_confirm_apply_while_outdated", lambda: "recalculate")
    monkeypatch.setattr(window, "_solve_layout", lambda: calls.append("solve"))
    monkeypatch.setattr(
        services.layout,
        "apply_last_solution_to_current_project",
        lambda: calls.append("apply") or True,
    )
    window._apply_layout()
    assert calls == ["solve"]

    calls.clear()
    monkeypatch.setattr(window, "_confirm_apply_while_outdated", lambda: "cancel")
    window._apply_layout()
    assert calls == []

    calls.clear()
    monkeypatch.setattr(window, "_confirm_apply_while_outdated", lambda: "apply")
    window._apply_layout()
    assert calls == ["apply"]


def test_export_while_outdated_recalculate_choice(qapp, tmp_path, monkeypatch):
    from PySide6.QtWidgets import QDialog

    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    project = StudioProject(
        project_id="PRJ-E",
        name="Export",
        boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
        pieces=[StudioPiece("A", 100, 50, "Demo", 19)],
        placements=[],
    )
    services.projects.new_project(project)
    window = MainWindow(services)
    services.layout.solutions = [_fake_solution()]
    services.layout.selected_solution_index = 0
    window._mark_project_modified(reason="edit")

    calls: list[str] = []
    opened: list[str] = []

    class _NoDialog:
        DialogCode = QDialog.DialogCode

        def __init__(self, *args, **kwargs):
            del args, kwargs
            opened.append("dialog")

        def exec(self):
            return QDialog.DialogCode.Rejected

    monkeypatch.setattr("studio.main_window.ExportDialog", _NoDialog)
    monkeypatch.setattr(
        window,
        "_confirm_while_outdated",
        lambda **kwargs: calls.append("confirm") or "recalculate",
    )
    monkeypatch.setattr(window, "_solve_layout", lambda: calls.append("solve"))
    window._export_selected_solution()
    assert calls == ["confirm", "solve"]
    assert opened == []

    calls.clear()
    monkeypatch.setattr(
        window,
        "_confirm_while_outdated",
        lambda **kwargs: calls.append("confirm") or "cancel",
    )
    window._export_selected_solution()
    assert calls == ["confirm"]
    assert opened == []

    calls.clear()
    monkeypatch.setattr(
        window,
        "_confirm_while_outdated",
        lambda **kwargs: calls.append("confirm") or "proceed",
    )
    window._export_selected_solution()
    assert calls == ["confirm"]
    assert opened == ["dialog"]
