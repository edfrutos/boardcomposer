"""Remember last successful export folder for save dialogs."""

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    return MainWindow(services)


def test_suggested_export_path_uses_existing_directory(qapp, tmp_path):
    del qapp
    export_dir = tmp_path / "out"
    export_dir.mkdir()
    window = _window(tmp_path)
    window.services.preferences.update(
        StudioPreferences(language="es", last_export_directory=str(export_dir))
    )

    suggested = window._suggested_export_path("boardcomposer-solution-1.svg")

    assert suggested == str(export_dir / "boardcomposer-solution-1.svg")


def test_suggested_export_path_falls_back_when_directory_missing(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.preferences.update(
        StudioPreferences(
            language="es",
            last_export_directory=str(tmp_path / "gone"),
        )
    )

    assert (
        window._suggested_export_path("boardcomposer-timeline.json")
        == "boardcomposer-timeline.json"
    )


def test_remember_export_directory_persists(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    target = tmp_path / "exports" / "layout.svg"
    target.parent.mkdir()
    target.write_text("<svg/>", encoding="utf-8")

    window._remember_export_directory(target)

    assert window.services.preferences.current.last_export_directory == str(
        target.parent.resolve()
    )
    reloaded = PreferencesManager(tmp_path / "preferences.json").current
    assert reloaded.last_export_directory == str(target.parent.resolve())
