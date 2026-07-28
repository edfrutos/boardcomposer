"""Gate Pantalla de inicio while already on Welcome."""

from __future__ import annotations

import pytest

from studio.main_window import MainWindow
from studio.models import StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices

pytestmark = pytest.mark.usefixtures("qapp")


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    return MainWindow(services)


def test_show_welcome_disabled_on_welcome_screen(tmp_path):
    window = _window(tmp_path)
    window._sync_welcome_action()

    action = window._actions["show_welcome"]
    assert not action.isEnabled()
    assert action.statusTip() == window._tr("status.already_on_welcome")

    window._show_welcome_screen()
    assert window._tr("status.already_on_welcome") in (
        window.statusBar().currentMessage()
    )


def test_show_welcome_enabled_on_workspace(tmp_path):
    window = _window(tmp_path)
    window.services.projects.new_project(StudioProject(project_id="PRJ-1", name="Ws"))
    window._show_workspace()

    action = window._actions["show_welcome"]
    assert action.isEnabled()
    tip = action.statusTip()
    assert tip != window._tr("status.already_on_welcome")
    assert "Ctrl+Shift+H" in tip or "⇧⌘H" in tip
