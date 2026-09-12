"""Swap-pieces action gated until two placed pieces can trade seats."""

from __future__ import annotations

import pytest

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices

pytestmark = pytest.mark.usefixtures("qapp")


def _window(tmp_path, *, place_b: bool = True) -> MainWindow:
    placements = [StudioPlacement("A", 0, 0, False, 0, "P1", 0, 0)]
    if place_b:
        placements.append(StudioPlacement("B", 300, 0, False, 0, "P1", 0, 0))
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="SwapGate",
            boards=[StudioBoard("P1", 1000, 500, "Demo", 19, 1)],
            pieces=[
                StudioPiece("A", 200, 100, "Demo", 19),
                StudioPiece("B", 200, 100, "Demo", 19),
            ],
            placements=placements,
        )
    )
    window = MainWindow(services)
    window._show_workspace()
    window.workspace.reload_project()
    return window


def test_swap_disabled_without_two_pieces(tmp_path):
    window = _window(tmp_path)
    window.workspace.clear_piece_selection()
    window._sync_edit_selection_actions()

    action = window._actions["swap_pieces"]
    assert not action.isEnabled()
    assert action.statusTip() == window._tr("status.swap_need_two")

    window.workspace.select_piece("A")
    window._sync_edit_selection_actions()
    assert not action.isEnabled()
    assert action.statusTip() == window._tr("status.swap_need_two")


def test_swap_disabled_when_one_unplaced(tmp_path):
    window = _window(tmp_path, place_b=False)
    window.workspace.select_pieces(["A", "B"])
    window._sync_edit_selection_actions()

    action = window._actions["swap_pieces"]
    assert not action.isEnabled()
    assert action.statusTip() == window._tr("status.swap_need_placed")


def test_swap_enabled_with_two_placed_and_runs(tmp_path):
    window = _window(tmp_path)
    window.workspace.select_pieces(["A", "B"])
    window._sync_edit_selection_actions()

    action = window._actions["swap_pieces"]
    assert action.isEnabled()
    tip = action.statusTip()
    assert "Ctrl+Alt+X" in tip or "⌥⌘X" in tip or "⌘⌥X" in tip

    window._swap_selected_pieces()
    project = window.services.projects.current_project
    a = project.placement_by_piece_id("A")
    b = project.placement_by_piece_id("B")
    assert (a.x_mm, a.y_mm) == (300, 0)
    assert (b.x_mm, b.y_mm) == (0, 0)
    assert "intercambi" in window.statusBar().currentMessage().casefold()
