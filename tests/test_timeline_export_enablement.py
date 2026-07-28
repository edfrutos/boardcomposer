"""Timeline export gated until events exist; UI font bootstrapped early."""

from PySide6.QtWidgets import QApplication

from studio.events.catalog import PROJECT_CREATED
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from studio.theme import _UI_FAMILY, bootstrap_ui_font


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    return MainWindow(services)


def test_bootstrap_ui_font_avoids_sans_serif(qapp):
    del qapp
    app = QApplication.instance()
    assert app is not None
    bootstrap_ui_font(app)
    assert app.font().family() == _UI_FAMILY
    assert app.font().family() != "Sans Serif"


def test_timeline_export_disabled_when_empty(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    assert not window.services.timeline.entries
    assert not window._actions["export_timeline"].isEnabled()
    assert not window.console._export.isEnabled()
    assert not window.console._clear.isEnabled()
    tip = window._actions["export_timeline"].statusTip()
    assert "Timeline" in tip or "eventos" in tip.lower()
    assert "vaciar" in window.console._clear.statusTip().lower()


def test_timeline_export_enabled_after_event(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.events.publish(PROJECT_CREATED, {"kind": "demo"})
    assert window._actions["export_timeline"].isEnabled()
    assert window.console._export.isEnabled()
    assert window.console._clear.isEnabled()
    assert (
        "Ctrl+Shift+L" in window._actions["export_timeline"].statusTip()
        or "⇧⌘L" in window._actions["export_timeline"].statusTip()
        or "Timeline" in window._actions["export_timeline"].statusTip()
    )
    assert "Vaciar" in window.console._clear.statusTip()


def test_timeline_export_disabled_after_clear(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.events.publish(PROJECT_CREATED, {"kind": "demo"})
    window.services.timeline.clear()
    assert not window._actions["export_timeline"].isEnabled()
    assert not window.console._export.isEnabled()
    assert not window.console._clear.isEnabled()


def test_timeline_export_disabled_when_filters_hide_events(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.events.publish(PROJECT_CREATED, {"kind": "demo"})
    assert window._actions["export_timeline"].isEnabled()
    assert window.console._export.isEnabled()

    # Simulate active filter set with no matches.
    window.console._filter_event = "__missing_event__"
    window.console._sync_event_actions()
    window._sync_timeline_actions()

    assert not window._actions["export_timeline"].isEnabled()
    assert not window.console._export.isEnabled()
    tip = window._actions["export_timeline"].statusTip().lower()
    assert "timeline" in tip or "eventos" in tip
