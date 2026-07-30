"""Timeline export gated until events exist; UI font bootstrapped early."""

from dataclasses import replace as dataclass_replace

from PySide6.QtWidgets import QApplication, QMessageBox

from studio.events.catalog import PIECE_MOVED, PROJECT_CREATED, TIMELINE_MARKED
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


def test_timeline_clear_confirms_before_wiping(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    window.services.events.publish(PROJECT_CREATED, {"kind": "demo"})
    window.services.events.publish(TIMELINE_MARKED, {"note": "keep"})
    assert window.console.total_event_count() == 2

    monkeypatch.setattr(
        QMessageBox,
        "question",
        lambda *args, **kwargs: QMessageBox.StandardButton.No,
    )
    window.console._clear.click()
    assert window.console.total_event_count() == 2

    monkeypatch.setattr(
        QMessageBox,
        "question",
        lambda *args, **kwargs: QMessageBox.StandardButton.Yes,
    )
    window.console._clear.click()
    assert window.console.total_event_count() == 0
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
    window.console.filters_changed.emit()

    assert not window._actions["export_timeline"].isEnabled()
    assert not window.console._export.isEnabled()
    assert window.console._clear.isEnabled()
    tip = window._actions["export_timeline"].statusTip().lower()
    assert "timeline" in tip or "eventos" in tip


def test_timeline_quick_filter_piece_moves(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.events.publish(PROJECT_CREATED, {"kind": "demo"})

    # Toggle quick filter -> only PieceMoved should remain visible.
    window.console._piece_moves.click()
    assert window.console.current_filter_event() == PIECE_MOVED
    assert not window._actions["export_timeline"].isEnabled()
    assert not window.console._export.isEnabled()

    window.services.events.publish(
        PIECE_MOVED,
        {
            "piece": "A",
            "kind": "moved",
            "from_x": 0.0,
            "from_y": 0.0,
            "to_x": 10.0,
            "to_y": 10.0,
        },
    )
    assert window._actions["export_timeline"].isEnabled()
    assert window.console._export.isEnabled()

    # Second click returns to all events.
    window.console._piece_moves.click()
    assert window.console.current_filter_event() is None


def test_timeline_event_count_label(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    assert window.console.total_event_count() == 0
    assert window.console.visible_event_count() == 0
    assert "0" in window.console._count_label.text()

    window.services.events.publish(PROJECT_CREATED, {"kind": "demo"})
    window.services.events.publish(TIMELINE_MARKED, {"note": "a"})
    assert window.console.total_event_count() == 2
    assert window.console.visible_event_count() == 2
    assert "2" in window.console._count_label.text()

    window.console._markers.click()
    assert window.console.visible_event_count() == 1
    assert window.console.total_event_count() == 2
    label = window.console._count_label.text()
    assert "1" in label and "2" in label


def test_timeline_quick_filter_markers(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.events.publish(PROJECT_CREATED, {"kind": "demo"})

    window.console._markers.click()
    assert window.console.current_filter_event() == TIMELINE_MARKED
    assert window.console._markers.isChecked()
    assert not window.console._piece_moves.isChecked()
    assert not window._actions["export_timeline"].isEnabled()
    assert not window.console._export.isEnabled()

    window.services.events.publish(TIMELINE_MARKED, {"note": "checkpoint"})
    assert window._actions["export_timeline"].isEnabled()
    assert window.console._export.isEnabled()

    # Switching to piece-moves clears the markers toggle.
    window.console._piece_moves.click()
    assert window.console.current_filter_event() == PIECE_MOVED
    assert window.console._piece_moves.isChecked()
    assert not window.console._markers.isChecked()

    window.console._markers.click()
    assert window.console.current_filter_event() == TIMELINE_MARKED
    window.console._markers.click()
    assert window.console.current_filter_event() is None
    assert not window.console._markers.isChecked()


def test_timeline_filters_persist_in_preferences(qapp, tmp_path):
    del qapp
    prefs_path = tmp_path / "preferences.json"
    services = StudioServices(preferences=PreferencesManager(prefs_path))
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)

    window.services.events.publish(PROJECT_CREATED, {"kind": "demo"})
    window.services.events.publish(
        PIECE_MOVED,
        {
            "piece": "A",
            "kind": "moved",
            "from_x": 0.0,
            "from_y": 0.0,
            "to_x": 1.0,
            "to_y": 1.0,
        },
    )
    window.console.set_filters(
        event_name=PIECE_MOVED, algorithm=None, period_seconds=300
    )

    services2 = StudioServices(preferences=PreferencesManager(prefs_path))
    services2.preferences.update(
        dataclass_replace(services2.preferences.current, language="es")
    )
    restored = MainWindow(services2)
    assert restored.console.current_filter_event() == PIECE_MOVED
    assert restored.console.current_filter_algorithm() is None
    assert restored.console.current_filter_period_seconds() == 300


def test_timeline_replay_mode_persists_in_preferences(qapp, tmp_path):
    del qapp
    prefs_path = tmp_path / "preferences.json"
    services = StudioServices(preferences=PreferencesManager(prefs_path))
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)

    assert window.console.current_replay_mode() == "placements"
    window.console.set_replay_mode("phases")
    assert window.console.current_replay_mode() == "phases"
    assert services.preferences.current.timeline_replay_mode == "phases"

    services2 = StudioServices(preferences=PreferencesManager(prefs_path))
    services2.preferences.update(
        dataclass_replace(services2.preferences.current, language="es")
    )
    restored = MainWindow(services2)
    assert restored.console.current_replay_mode() == "phases"


def test_timeline_replay_speed_persists_in_preferences(qapp, tmp_path):
    del qapp
    prefs_path = tmp_path / "preferences.json"
    services = StudioServices(preferences=PreferencesManager(prefs_path))
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)

    assert window.console.current_replay_interval_ms() == 450
    window.console.set_replay_interval_ms(200)
    assert window.console.current_replay_interval_ms() == 200
    assert services.preferences.current.timeline_replay_interval_ms == 200

    services2 = StudioServices(preferences=PreferencesManager(prefs_path))
    services2.preferences.update(
        dataclass_replace(services2.preferences.current, language="es")
    )
    restored = MainWindow(services2)
    assert restored.console.current_replay_interval_ms() == 200
    assert restored.console._play_timer.interval() == 200


def test_timeline_follow_latest_persists_and_skips_scroll(qapp, tmp_path):
    del qapp
    prefs_path = tmp_path / "preferences.json"
    services = StudioServices(preferences=PreferencesManager(prefs_path))
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)

    assert window.console.follows_latest() is True
    window.console.set_follow_latest(False)
    assert window.console.follows_latest() is False
    assert services.preferences.current.timeline_follow_latest is False

    window.services.events.publish(PROJECT_CREATED, {"kind": "demo"})
    window.services.events.publish(TIMELINE_MARKED, {"note": "keep"})
    # With follow off, programmatic scroll-to-bottom is skipped on rebuild path;
    # toggle remains off after new events.
    assert window.console.follows_latest() is False

    services2 = StudioServices(preferences=PreferencesManager(prefs_path))
    services2.preferences.update(
        dataclass_replace(services2.preferences.current, language="es")
    )
    restored = MainWindow(services2)
    assert restored.console.follows_latest() is False
    assert restored.console._follow.isChecked() is False
