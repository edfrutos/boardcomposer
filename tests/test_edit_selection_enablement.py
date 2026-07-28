"""Edit selection actions gated until piece/board/project target exists."""

from __future__ import annotations

import pytest

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices

pytestmark = pytest.mark.usefixtures("qapp")

_EDIT_ACTIONS = (
    ("delete_piece", "status.nothing_to_delete"),
    ("duplicate_piece", "status.nothing_to_duplicate"),
    ("edit_selection", "status.nothing_to_edit_selection"),
    ("rename_selection", "status.nothing_to_rename_selection"),
    ("copy_selection_id", "status.nothing_to_copy_id"),
)


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="EditGate",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 200, 100, "Demo", 19)],
            placements=[StudioPlacement("A", 10, 20, False, 0, "B1", 0, 0)],
        )
    )
    window = MainWindow(services)
    window.workspace.reload_project()
    window._reload_explorer()
    return window


def test_edit_selection_actions_disabled_without_target(tmp_path):
    window = _window(tmp_path)
    window.explorer.setCurrentItem(None)
    window.workspace.clear_piece_selection()
    window._sync_edit_selection_actions()

    for key, status_key in _EDIT_ACTIONS:
        action = window._actions[key]
        assert not action.isEnabled(), key
        assert action.statusTip() == window._tr(status_key), key


def test_edit_selection_actions_enabled_with_piece(tmp_path):
    window = _window(tmp_path)
    window.explorer.setCurrentItem(None)
    window.workspace.select_piece("A")
    window._sync_edit_selection_actions()

    for key, status_key in _EDIT_ACTIONS:
        action = window._actions[key]
        assert action.isEnabled(), key
        tip = action.statusTip()
        assert tip
        assert tip != window._tr(status_key), key


def test_edit_selection_actions_enabled_with_focused_board(tmp_path):
    window = _window(tmp_path)
    window.workspace.clear_piece_selection()
    window.explorer.setCurrentItem(None)
    window.workspace.focus_board("B1")
    window._sync_edit_selection_actions()

    for key in (
        "delete_piece",
        "duplicate_piece",
        "edit_selection",
        "copy_selection_id",
    ):
        assert window._actions[key].isEnabled(), key

    # Rename needs explorer project/piece/board or a single canvas piece.
    assert not window._actions["rename_selection"].isEnabled()
    assert window._actions["rename_selection"].statusTip() == window._tr(
        "status.nothing_to_rename_selection"
    )


def test_rename_enabled_with_explorer_project(tmp_path):
    window = _window(tmp_path)
    window.workspace.clear_piece_selection()
    item = window._find_explorer_item_by_role("project:root")
    assert item is not None
    window.explorer.setCurrentItem(item)
    window._sync_edit_selection_actions()

    assert window._actions["rename_selection"].isEnabled()
    tip = window._actions["rename_selection"].statusTip()
    assert "F2" in tip or "Rename" in tip or "Renombrar" in tip
