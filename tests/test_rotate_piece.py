"""Rotate selected piece (Edit → Rotar / R)."""

from __future__ import annotations

from pathlib import Path

import pytest

from studio.commands import RotatePieceCommand
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager
from studio.services import StudioServices

pytestmark = pytest.mark.usefixtures("qapp")


def _window(tmp_path: Path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Rotate",
            boards=[StudioBoard("P1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 400, 300, "Demo", 19)],
            placements=[StudioPlacement("A", 0, 0, False, 0, "P1", 0, 0)],
        )
    )
    window = MainWindow(services)
    window._show_workspace()
    window.workspace.reload_project()
    return window


def test_rotate_selected_piece_toggles_rotation_and_rotated_flag(tmp_path):
    window = _window(tmp_path)
    window.workspace.select_piece("A")

    window._rotate_selected_piece()

    placement = window.services.projects.current_project.placement_by_piece_id("A")
    assert placement is not None
    assert placement.rotation == 90
    assert placement.rotated is True

    item = window.workspace.piece_item_by_id("A")
    assert item is not None
    assert item.rect().width() == 300
    assert item.rect().height() == 400

    window._rotate_selected_piece()
    placement = window.services.projects.current_project.placement_by_piece_id("A")
    assert placement.rotation == 0
    assert placement.rotated is False


def test_rotate_piece_command_keeps_rotated_in_sync():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Rotate",
            boards=[StudioBoard("P1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 100, 50, "Demo", 19)],
            placements=[StudioPlacement("A", 0, 0, False, 0, "P1", 0, 0)],
        )
    )
    command = RotatePieceCommand(services, "A", 0, 90)
    command.execute()
    placement = services.projects.current_project.placement_by_piece_id("A")
    assert placement.rotation == 90
    assert placement.rotated is True
    command.undo()
    assert placement.rotation == 0
    assert placement.rotated is False
