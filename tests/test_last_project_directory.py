"""Remember last successful .bcproj open/save folder."""

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    return MainWindow(services)


def test_suggested_project_directory_uses_existing(qapp, tmp_path):
    del qapp
    project_dir = tmp_path / "projects"
    project_dir.mkdir()
    window = _window(tmp_path)
    window.services.preferences.update(
        StudioPreferences(language="es", last_project_directory=str(project_dir))
    )

    assert window._suggested_project_directory() == str(project_dir)
    assert window._suggested_project_path("demo.bcproj") == str(
        project_dir / "demo.bcproj"
    )


def test_suggested_project_directory_falls_back_when_missing(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.preferences.update(
        StudioPreferences(
            language="es",
            last_project_directory=str(tmp_path / "gone"),
        )
    )

    assert window._suggested_project_directory() == ""
    assert window._suggested_project_path("demo.bcproj") == "demo.bcproj"


def test_remember_project_directory_persists(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    target = tmp_path / "projects" / "demo.bcproj"
    target.parent.mkdir()
    target.write_text("{}", encoding="utf-8")

    window._remember_project_directory(target)

    assert window.services.preferences.current.last_project_directory == str(
        target.parent.resolve()
    )
    reloaded = PreferencesManager(tmp_path / "preferences.json").current
    assert reloaded.last_project_directory == str(target.parent.resolve())
