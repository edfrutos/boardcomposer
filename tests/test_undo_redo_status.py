"""Undo/redo announce honest status bar feedback."""

from studio.commands.duplicate_piece_command import DuplicatePieceCommand
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
            name="UndoStatus",
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


def _duplicate_once(window: MainWindow) -> None:
    project = window.services.projects.current_project
    assert project is not None
    source = next(piece for piece in project.pieces if piece.piece_id == "A")
    clone = StudioPiece(
        "A1",
        source.length_mm,
        source.width_mm,
        source.material,
        source.thickness_mm,
    )
    placement = StudioPlacement("A1", 50, 50, False, 0, "B1", 0, 0)
    window.services.commands.execute(
        DuplicatePieceCommand(window.services, clone, placement)
    )
    window.workspace.reload_project()
    window._reload_explorer()
    window.update_undo_redo()


def test_undo_without_stack_shows_status(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)

    window._undo()

    assert window._tr("status.nothing_to_undo") in window.statusBar().currentMessage()


def test_redo_without_stack_shows_status(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)

    window._redo()

    assert window._tr("status.nothing_to_redo") in window.statusBar().currentMessage()


def test_undo_announces_status(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    _duplicate_once(window)

    window._undo()

    assert window._tr("status.undone") in window.statusBar().currentMessage()


def test_redo_announces_status(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    _duplicate_once(window)
    window._undo()

    window._redo()

    assert window._tr("status.redone") in window.statusBar().currentMessage()
