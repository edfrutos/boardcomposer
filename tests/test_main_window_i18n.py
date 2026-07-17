"""Tests for menu and Inspector language switching (SCR-006)."""

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def test_main_window_menus_and_inspector_follow_language(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))

    window = MainWindow(services)

    assert window._menus["file"].title() == "Archivo"
    assert window._actions["solve_layout"].text() == "Calcular layout"
    assert "Sin selección" in window.inspector.toPlainText()
    assert window.inspector_dock.windowTitle() == "Inspector"
    assert window.pin_reference_button.text() == "Fijar como referencia"

    services.preferences.update(StudioPreferences(language="en"))
    window._apply_preferences()

    assert window._menus["file"].title() == "File"
    assert window._actions["solve_layout"].text() == "Calculate layout"
    assert "No selection" in window.inspector.toPlainText()
    assert window.solutions_dock.windowTitle() == "Solution comparator"
    assert window.pin_reference_button.text() == "Pin as reference"
    assert window.comparator_sort.itemText(0) == "Solver order"

    window._status("status.prefs_saved")
    assert "Preferences saved" in window.statusBar().currentMessage()
