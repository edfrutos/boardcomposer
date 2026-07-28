"""Dock toggle status feedback and dynamic Mostrar/Ocultar tips."""

from __future__ import annotations

import pytest

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices

pytestmark = pytest.mark.usefixtures("qapp")


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    window.show()
    window._sync_dock_toggle_tips()
    return window


def test_dock_tips_reflect_visibility(tmp_path):
    window = _window(tmp_path)
    tip = window._actions["toggle_explorer"].statusTip()
    assert "Ocultar" in tip
    assert "Ctrl+1" in tip or "⌘1" in tip

    window.explorer_dock.hide()
    window._sync_dock_toggle_tips()
    tip = window._actions["toggle_explorer"].statusTip()
    assert "Mostrar" in tip


def test_dock_toggle_announces_status(tmp_path):
    window = _window(tmp_path)
    window._actions["toggle_inspector"].trigger()
    message = window.statusBar().currentMessage().lower()
    assert "inspector" in message
    assert "oculto" in message or "visible" in message
