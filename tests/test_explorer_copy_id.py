"""Copy piece/board id from the Explorador context menu."""

from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def test_copy_id_from_explorer_puts_text_on_clipboard(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Copy",
            boards=[StudioBoard("TAB-007", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("PZ-42", 200, 100, "Demo", 19)],
            placements=[],
        )
    )
    window = MainWindow(services)
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.clear()

    window._run_explorer_context_action("copy_id", "piece:PZ-42")

    assert clipboard.text() == "PZ-42"
    assert "PZ-42" in window.statusBar().currentMessage()

    window._run_explorer_context_action("copy_id", "board:TAB-007")

    assert clipboard.text() == "TAB-007"
    assert "TAB-007" in window.statusBar().currentMessage()
