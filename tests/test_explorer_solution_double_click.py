"""Activating a solution in the Explorador previews it."""

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window_with_solutions(tmp_path):
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Solutions",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 100, 50, "Demo", 19)],
            placements=[
                StudioPlacement("A", 0, 0, False, 0, "B1", 0, 0),
            ],
        )
    )
    services.layout.solutions = [
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)]),
        AssemblySolution(placements=[BoardPlacement("A", 200, 100, 100, 50)]),
    ]
    services.layout.select_solution(0)
    window = MainWindow(services)
    window.workspace.reload_project()
    window._reload_explorer()
    return window, services


def test_explorer_activate_solution_selects_preview(qapp, tmp_path, monkeypatch):
    del qapp
    window, services = _window_with_solutions(tmp_path)

    previewed: list[object] = []
    monkeypatch.setattr(
        window.workspace,
        "preview_solution",
        lambda solution, **kwargs: previewed.append(solution),
    )

    item = window._find_explorer_item_by_role("solution:1")
    assert item is not None
    window._on_explorer_item_activated(item, 0)

    assert services.layout.selected_solution_index == 1
    assert previewed == [services.layout.solutions[1]]
    assert "2" in window.statusBar().currentMessage()


def test_selecting_solution_keeps_tree_item_alive(qapp, tmp_path):
    """Regression: reload-on-select deleted the item and killed double-click."""
    del qapp
    window, services = _window_with_solutions(tmp_path)
    window.show()

    item = window._find_explorer_item_by_role("solution:1")
    assert item is not None
    role_before = item.data(0, Qt.ItemDataRole.UserRole)

    center = window.explorer.visualItemRect(item).center()
    QTest.mouseClick(
        window.explorer.viewport(),
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
        center,
    )

    assert services.layout.selected_solution_index == 1
    # Same C++ item must still be valid after preview.
    assert item.data(0, Qt.ItemDataRole.UserRole) == role_before
    assert window._find_explorer_item_by_role("solution:1") is item

    piece = window.workspace.piece_item_by_id("A")
    assert piece is not None
    assert piece.pos().x() == 200
    assert piece.pos().y() == 100
    assert window.explorer.expandsOnDoubleClick() is False
