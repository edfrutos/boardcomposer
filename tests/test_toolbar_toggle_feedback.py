"""Toolbar toggle status feedback and dynamic Mostrar/Ocultar tip."""

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
    window._sync_toolbar_toggle_tip()
    return window


def test_toolbar_tip_reflects_visibility(tmp_path):
    window = _window(tmp_path)
    tip = window._actions["toggle_toolbar"].statusTip()
    assert "Ocultar" in tip
    assert "Ctrl+Shift+K" in tip or "⇧⌘K" in tip

    window._toolbar.hide()
    window._sync_toolbar_toggle_tip()
    tip = window._actions["toggle_toolbar"].statusTip()
    assert "Mostrar" in tip


def test_toolbar_toggle_announces_status(tmp_path):
    window = _window(tmp_path)
    window._actions["toggle_toolbar"].trigger()
    assert window._tr("status.toolbar_hidden") in window.statusBar().currentMessage()

    window._actions["toggle_toolbar"].trigger()
    assert window._tr("status.toolbar_shown") in window.statusBar().currentMessage()
