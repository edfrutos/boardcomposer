"""Status bar shows physical board sheets, summing quantity (IDE-0069)."""

from studio.main_window import MainWindow
from studio.models import StudioBoard
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_copy_selection_id import _window


def test_physical_board_status_hidden_without_boards(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    assert window._boards_label.text() == ""
    assert window._boards_label.isHidden()


def test_physical_board_status_sums_quantity(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    assert window._boards_label.text() == "1 tab."
    assert not window._boards_label.isHidden()
    assert "físicos" in window._boards_label.toolTip().casefold()

    project = window.services.projects.current_project
    assert project is not None
    project.boards[0] = StudioBoard("B1", 1000, 500, "Demo", 19, 3)
    project.boards.append(StudioBoard("B2", 800, 400, "Demo", 19, 2))
    window.update_window_title()
    assert window._boards_label.text() == "5 tab."
    assert "5" in window._boards_label.toolTip()

    window.services.preferences.update(
        window.services.preferences.current.__class__(language="en", units="mm")
    )
    window._retranslate_ui()
    assert window._boards_label.text() == "5 tab."
    assert "physical" in window._boards_label.toolTip().casefold()
