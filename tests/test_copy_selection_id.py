"""Copy selection ID via Edit menu / Ctrl+Shift+C."""

from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="CopyId",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 200, 100, "Demo", 19)],
            placements=[
                StudioPlacement("A", 10, 20, False, 0, "B1", 0, 0),
            ],
        )
    )
    window = MainWindow(services)
    window.workspace.reload_project()
    window._reload_explorer()
    return window


def test_copy_selection_id_shortcut(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    assert "Ctrl+Shift+C" in window._actions["copy_selection_id"].shortcut().toString()


def test_copy_selection_id_from_explorer_piece(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    item = window._find_explorer_item_by_role("piece:A")
    assert item is not None
    window.explorer.setCurrentItem(item)

    window._actions["copy_selection_id"].trigger()

    clipboard = QApplication.clipboard()
    assert clipboard is not None
    assert clipboard.text() == "A"
    assert "A" in window.statusBar().currentMessage()


def test_copy_selection_id_from_canvas_piece(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.explorer.setCurrentItem(None)
    window.workspace.select_piece("A")

    window._copy_selection_id()

    clipboard = QApplication.clipboard()
    assert clipboard is not None
    assert clipboard.text() == "A"


def test_copy_selection_id_without_target_shows_status(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.explorer.setCurrentItem(None)
    window.workspace.clear_piece_selection()

    window._copy_selection_id()

    assert window._tr("status.nothing_to_copy_id") in (
        window.statusBar().currentMessage()
    )
