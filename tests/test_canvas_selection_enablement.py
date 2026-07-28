"""Select all / deselect / invert gated until useful."""

from __future__ import annotations

import pytest

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices

pytestmark = pytest.mark.usefixtures("qapp")


def _window(tmp_path, *, with_placement: bool = True) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    placements = (
        [StudioPlacement("A", 10, 20, False, 0, "B1", 0, 0)] if with_placement else []
    )
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="SelGate",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 200, 100, "Demo", 19)],
            placements=placements,
        )
    )
    window = MainWindow(services)
    window.workspace.reload_project()
    window._reload_explorer()
    return window


def test_select_all_and_invert_disabled_without_canvas_pieces(tmp_path):
    window = _window(tmp_path, with_placement=False)
    window._sync_edit_selection_actions()

    for key in ("select_all_pieces", "invert_selection"):
        action = window._actions[key]
        assert not action.isEnabled(), key
        assert action.statusTip() == window._tr("status.no_pieces_to_select"), key


def test_select_all_and_invert_enabled_with_placements(tmp_path):
    window = _window(tmp_path)
    window.workspace.clear_piece_selection()
    window._sync_edit_selection_actions()

    for key in ("select_all_pieces", "invert_selection"):
        action = window._actions[key]
        assert action.isEnabled(), key
        tip = action.statusTip()
        assert tip != window._tr("status.no_pieces_to_select"), key
        assert tip


def test_deselect_gated_until_selection(tmp_path):
    window = _window(tmp_path)
    window.workspace.clear_piece_selection()
    window._sync_edit_selection_actions()

    assert not window._actions["deselect_pieces"].isEnabled()
    assert window._actions["deselect_pieces"].statusTip() == window._tr(
        "status.nothing_to_deselect"
    )

    window._deselect_pieces()
    assert window._tr("status.nothing_to_deselect") in (
        window.statusBar().currentMessage()
    )

    window.workspace.select_piece("A")
    window._sync_edit_selection_actions()
    assert window._actions["deselect_pieces"].isEnabled()
    tip = window._actions["deselect_pieces"].statusTip()
    assert tip != window._tr("status.nothing_to_deselect")
    assert "selección" in tip.lower() or "selection" in tip.lower()
