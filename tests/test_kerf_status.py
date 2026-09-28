"""Status bar shows the project saw kerf in Preferences units (IDE-0065)."""

from dataclasses import replace

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_copy_selection_id import _window


def test_kerf_status_hidden_without_project(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    assert window._kerf_label.text() == ""
    assert window._kerf_label.isHidden()


def test_kerf_status_uses_display_units(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    assert window._kerf_label.text() == "kerf 0 mm"
    assert not window._kerf_label.isHidden()

    project = window.services.projects.current_project
    assert project is not None
    project.kerf_mm = 3.2
    window.update_window_title()
    assert window._kerf_label.text() == "kerf 3.2 mm"
    tip = window._kerf_label.toolTip().casefold()
    assert "sierra" in tip
    assert "3.2 mm" in tip

    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm")
    )
    window._retranslate_ui()
    assert window._kerf_label.text() == "kerf 0.32 cm"

    window.services.preferences.update(
        replace(window.services.preferences.current, language="en")
    )
    window._retranslate_ui()
    assert "saw kerf" in window._kerf_label.toolTip().casefold()
    assert window._kerf_label.text() == "kerf 0.32 cm"
