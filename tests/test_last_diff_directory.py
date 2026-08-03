"""Remember last browsed .bcproj folder for Compare revisions."""

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    return MainWindow(services)


def test_suggested_diff_directory_uses_existing(qapp, tmp_path):
    del qapp
    diff_dir = tmp_path / "diffs"
    diff_dir.mkdir()
    window = _window(tmp_path)
    window.services.preferences.update(
        StudioPreferences(language="es", last_diff_directory=str(diff_dir))
    )

    assert window._suggested_diff_directory() == str(diff_dir)


def test_suggested_diff_directory_falls_back_when_missing(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.preferences.update(
        StudioPreferences(
            language="es",
            last_diff_directory=str(tmp_path / "gone"),
        )
    )

    assert window._suggested_diff_directory() == ""


def test_remember_diff_directory_persists(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    target = tmp_path / "revs" / "old.bcproj"
    target.parent.mkdir()
    target.write_text("{}", encoding="utf-8")

    window._remember_diff_directory(target)

    assert window.services.preferences.current.last_diff_directory == str(
        target.parent.resolve()
    )
    reloaded = PreferencesManager(tmp_path / "preferences.json").current
    assert reloaded.last_diff_directory == str(target.parent.resolve())
