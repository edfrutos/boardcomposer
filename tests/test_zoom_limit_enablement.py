"""Zoom in/out gated at camera min/max."""

from __future__ import annotations

import pytest

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices

pytestmark = pytest.mark.usefixtures("qapp")


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="ZoomGate",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 200, 100, "Demo", 19)],
            placements=[StudioPlacement("A", 10, 20, False, 0, "B1", 0, 0)],
        )
    )
    window = MainWindow(services)
    window.workspace.reload_project()
    return window


def test_zoom_actions_enabled_at_default(tmp_path):
    window = _window(tmp_path)
    window._sync_zoom_actions()
    assert window._actions["zoom_in"].isEnabled()
    assert window._actions["zoom_out"].isEnabled()


def test_zoom_in_disabled_at_maximum(tmp_path):
    window = _window(tmp_path)
    window.workspace._camera.zoom = window.workspace._camera.max_zoom
    window.workspace._apply_camera()

    assert not window.workspace.can_zoom_in
    assert window.workspace.can_zoom_out
    assert not window._actions["zoom_in"].isEnabled()
    assert window._actions["zoom_in"].statusTip() == window._tr(
        "status.zoom_at_maximum"
    )
    assert window._actions["zoom_out"].isEnabled()

    window._zoom_in()
    assert window._tr("status.zoom_at_maximum") in window.statusBar().currentMessage()


def test_zoom_out_disabled_at_minimum(tmp_path):
    window = _window(tmp_path)
    window.workspace._camera.zoom = window.workspace._camera.min_zoom
    window.workspace._apply_camera()

    assert window.workspace.can_zoom_in
    assert not window.workspace.can_zoom_out
    assert not window._actions["zoom_out"].isEnabled()
    assert window._actions["zoom_out"].statusTip() == window._tr(
        "status.zoom_at_minimum"
    )
    assert window._actions["zoom_in"].isEnabled()

    window._zoom_out()
    assert window._tr("status.zoom_at_minimum") in window.statusBar().currentMessage()
