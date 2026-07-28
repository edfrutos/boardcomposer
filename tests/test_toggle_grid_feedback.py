"""Toggle grid status feedback and dynamic tip."""

from __future__ import annotations

import pytest

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices

pytestmark = pytest.mark.usefixtures("qapp")


def _window(tmp_path, *, show_grid: bool = True) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es", show_grid=show_grid))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Grid",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
        )
    )
    window = MainWindow(services)
    window.workspace.reload_project()
    window._sync_view_actions()
    return window


def test_toggle_grid_tip_reflects_current_state(tmp_path):
    window = _window(tmp_path, show_grid=True)
    tip = window._actions["toggle_grid"].statusTip()
    assert "Ocultar" in tip
    assert "Ctrl+G" in tip or "⌘G" in tip

    window = _window(tmp_path / "off", show_grid=False)
    tip = window._actions["toggle_grid"].statusTip()
    assert "Mostrar" in tip


def test_toggle_grid_announces_status(tmp_path):
    window = _window(tmp_path, show_grid=True)
    window._actions["toggle_grid"].setChecked(False)
    assert window._tr("status.grid_hidden") in window.statusBar().currentMessage()
    assert window.services.preferences.current.show_grid is False
    assert "Mostrar" in window._actions["toggle_grid"].statusTip()

    window._actions["toggle_grid"].setChecked(True)
    assert window._tr("status.grid_shown") in window.statusBar().currentMessage()
    assert window.services.preferences.current.show_grid is True
    assert "Ocultar" in window._actions["toggle_grid"].statusTip()
