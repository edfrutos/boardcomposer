"""Gate save/rename/template actions until a project is open."""

from studio.main_window import MainWindow
from studio.models import StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    return MainWindow(services)


def test_project_file_actions_disabled_without_project(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    assert window.services.projects.current_project is None

    for key in ("save", "save_as", "save_as_template", "rename_project"):
        assert not window._actions[key].isEnabled(), key

    assert "guardar" in window._actions["save"].statusTip().lower()
    assert "renombrar" in window._actions["rename_project"].statusTip().lower()
    assert "plantilla" in window._actions["save_as_template"].statusTip().lower()


def test_project_file_actions_enabled_with_project(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.projects.new_project(StudioProject(project_id="PRJ-1", name="Demo"))
    window.update_window_title()

    for key in ("save", "save_as", "save_as_template", "rename_project"):
        assert window._actions[key].isEnabled(), key

    assert "Ctrl+S" in window._actions["save"].statusTip() or "⌘S" in (
        window._actions["save"].statusTip()
    )
