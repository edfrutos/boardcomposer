"""UAT multi-candidate star flow: demo → solve → navigate → pin → export."""

from __future__ import annotations

from pathlib import Path

import pytest
from PySide6.QtWidgets import QDialog, QFileDialog

from studio.export_options import ExportOptions
from studio.main_window import MainWindow
from studio.preferences import (
    DEFAULT_MAX_SOLUTIONS,
    PreferencesManager,
    StudioPreferences,
)
from studio.services import StudioServices

pytestmark = pytest.mark.usefixtures("qapp")


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(
        StudioPreferences(language="es", max_solutions=DEFAULT_MAX_SOLUTIONS)
    )
    return MainWindow(services)


def _demo_solve(window: MainWindow, monkeypatch) -> int:
    monkeypatch.setattr(window, "_confirm_discard_unsaved_changes", lambda: True)
    window._new_demo_project()
    window._show_workspace()
    solution = window.services.layout.solve_current_project()
    assert solution is not None
    window._reload_solution_table()
    window._show_layout_solution(solution)
    window._reload_explorer()
    window._sync_solution_actions()
    window._reveal_comparator_after_solve()
    return len(window.services.layout.solutions)


def test_uat_demo_solve_fills_comparator_and_explorer(tmp_path, monkeypatch):
    window = _window(tmp_path)
    window.show()
    count = _demo_solve(window, monkeypatch)

    assert count >= 2
    assert window.solutions_table.rowCount() >= 2
    assert window.solution_thumbnails.count() >= 2
    assert window._actions["previous_solution"].isEnabled()
    assert window._actions["next_solution"].isEnabled()
    assert window._actions["export_selected"].isEnabled()
    assert window.pin_reference_button.isEnabled()
    assert window.comparator_sort.isEnabled()
    assert window.solutions_dock.isVisible()

    solutions_root = window._find_explorer_item_by_role("category:solutions")
    assert solutions_root is not None
    assert solutions_root.childCount() >= 2


def test_uat_page_navigation_and_pin_with_demo(tmp_path, monkeypatch):
    window = _window(tmp_path)
    count = _demo_solve(window, monkeypatch)
    assert count >= 2

    first = window.services.layout.selected_solution_index
    window._next_layout_solution()
    second = window.services.layout.selected_solution_index
    assert second != first
    window._previous_layout_solution()
    assert window.services.layout.selected_solution_index == first

    window.services.layout.select_solution(1)
    window._show_layout_solution(window.services.layout.selected_solution)
    window._pin_selected_as_reference()
    assert window._comparator_reference_index == 1
    assert window._comparator_reference_pinned is True
    assert window.solution_differences.toPlainText().strip()


def test_uat_export_solution_offers_open_after(tmp_path, monkeypatch):
    window = _window(tmp_path)
    count = _demo_solve(window, monkeypatch)
    assert count >= 2
    window.services.layout.select_solution(0)
    window._sync_solution_actions()

    target = tmp_path / "boardcomposer-solution-1.json"
    offered: list[Path] = []

    class _FakeExportDialog:
        DialogCode = QDialog.DialogCode

        def __init__(self, *args, **kwargs):
            pass

        def exec(self):
            return QDialog.DialogCode.Accepted

        def options(self):
            return ExportOptions(format="json")

    monkeypatch.setattr("studio.main_window.ExportDialog", _FakeExportDialog)
    monkeypatch.setattr(
        QFileDialog,
        "getSaveFileName",
        lambda *args, **kwargs: (str(target), "JSON"),
    )
    monkeypatch.setattr(
        window,
        "_offer_open_exported_path",
        lambda path: offered.append(Path(path)),
    )

    window._export_selected_solution()

    assert target.is_file()
    assert offered == [target]
    assert window._actions["export_selected"].isEnabled()
