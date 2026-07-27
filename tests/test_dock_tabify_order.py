"""Bottom docks must be added before tabify (macOS Qt raise_ crash)."""

from PySide6.QtCore import Qt

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    return MainWindow(services)


def test_comparator_is_tabified_with_timeline_after_build(qapp, tmp_path):
    window = _window(tmp_path)
    tabbed = window.tabifiedDockWidgets(window.console_dock)
    assert window.solutions_dock in tabbed
    assert window.console_dock.parent() is window
    assert window.solutions_dock.parent() is window


def test_raise_dock_defers_and_skips_hidden(qapp, tmp_path):
    window = _window(tmp_path)
    window.solutions_dock.hide()
    window._raise_dock(window.solutions_dock)
    qapp.processEvents()
    # Hidden dock must not be forced visible by the safe raise helper.
    assert not window.solutions_dock.isVisible()


def test_ensure_bottom_docks_tabified_repairs_ungrouped(qapp, tmp_path):
    window = _window(tmp_path)
    # Split tab group: re-add comparator alone in the bottom area.
    window.removeDockWidget(window.solutions_dock)
    window.addDockWidget(
        Qt.DockWidgetArea.BottomDockWidgetArea,
        window.solutions_dock,
    )
    window.solutions_dock.show()
    window.console_dock.show()
    assert window.solutions_dock not in window.tabifiedDockWidgets(window.console_dock)

    window._ensure_bottom_docks_tabified()
    assert window.solutions_dock in window.tabifiedDockWidgets(window.console_dock)
