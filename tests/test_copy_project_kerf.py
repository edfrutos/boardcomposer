"""Copy the project saw kerf in Preferences units (IDE-0072)."""

from dataclasses import replace

from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_copy_selection_id import _window


def test_copy_project_kerf_uses_display_units(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    action = window._actions["copy_project_kerf"]
    assert "Ctrl+Alt+Shift+K" in action.shortcut().toString()
    assert action.isEnabled()

    project = window.services.projects.current_project
    assert project is not None
    project.kerf_mm = 3.2
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.clear()
    action.trigger()
    assert clipboard.text() == "3.2 mm"
    assert window.statusBar().currentMessage() == window._tr(
        "status.kerf_copied", length="3.2 mm"
    )

    project.kerf_mm = 0
    action.trigger()
    assert clipboard.text() == "0 mm"

    project.kerf_mm = 3.2
    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm")
    )
    action.trigger()
    assert clipboard.text() == "0.32 cm"


def test_copy_project_kerf_without_project_keeps_clipboard(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    action = window._actions["copy_project_kerf"]
    assert not action.isEnabled()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    window._copy_project_kerf()
    assert clipboard.text() == "keep-me"
    assert window.statusBar().currentMessage() == window._tr(
        "status.nothing_to_copy_kerf"
    )
