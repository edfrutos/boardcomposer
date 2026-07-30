"""Timeline export offers the same open/reveal dialog as solution export."""

from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from studio.events.catalog import PROJECT_CREATED
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    return MainWindow(services)


def test_timeline_export_offers_open_after_save(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    window.services.events.publish(PROJECT_CREATED, {"kind": "demo"})

    target = tmp_path / "boardcomposer-timeline.json"
    offered: list[Path] = []
    monkeypatch.setattr(
        window,
        "_offer_open_exported_path",
        lambda path: offered.append(Path(path)),
    )
    monkeypatch.setattr(
        QFileDialog,
        "getSaveFileName",
        lambda *args, **kwargs: (str(target), "JSON"),
    )

    window._export_timeline_history()

    assert target.is_file()
    assert offered == [target]
    assert "Timeline" in window.statusBar().currentMessage() or target.name in str(
        window.statusBar().currentMessage()
    )


def test_timeline_export_remembers_format(qapp, tmp_path, monkeypatch):
    del qapp
    prefs_path = tmp_path / "preferences.json"
    services = StudioServices(preferences=PreferencesManager(prefs_path))
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    window.services.events.publish(PROJECT_CREATED, {"kind": "demo"})

    target = tmp_path / "boardcomposer-timeline.csv"
    monkeypatch.setattr(window, "_offer_open_exported_path", lambda path: None)
    monkeypatch.setattr(
        QFileDialog,
        "getSaveFileName",
        lambda *args, **kwargs: (str(target), "CSV (*.csv)"),
    )

    window._export_timeline_history()

    assert target.is_file()
    assert services.preferences.current.timeline_export_format == "csv"

    services2 = StudioServices(preferences=PreferencesManager(prefs_path))
    window2 = MainWindow(services2)
    window2.services.events.publish(PROJECT_CREATED, {"kind": "again"})

    suggested: list[str] = []
    filters: list[str] = []

    def _fake_save2(*args, **kwargs):
        suggested.append(str(args[2] if len(args) > 2 else kwargs.get("dir", "")))
        filters.append(str(args[3] if len(args) > 3 else kwargs.get("filter", "")))
        return "", ""

    monkeypatch.setattr(QFileDialog, "getSaveFileName", _fake_save2)
    window2._export_timeline_history()

    assert suggested and suggested[0].endswith("boardcomposer-timeline.csv")
    assert filters and filters[0].startswith("CSV")
