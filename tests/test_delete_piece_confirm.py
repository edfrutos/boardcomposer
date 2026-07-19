"""Confirm dialog before deleting a piece from Studio."""

from PySide6.QtWidgets import QMessageBox

from studio.i18n import tr
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window_with_piece(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Delete",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 400, 300, "Demo", 19)],
            placements=[
                StudioPlacement("A", 10, 20, False, 0, "B1", 0, 0),
            ],
        )
    )
    window = MainWindow(services)
    window.workspace.reload_project()
    window._reload_explorer()
    return window


def test_delete_piece_confirm_i18n_keys():
    assert tr("dialog.delete_piece_title", "es") == "Eliminar pieza"
    assert "A" in tr("dialog.delete_piece_confirm", "es", id="A")
    assert "Workspace" in tr("dialog.delete_piece_confirm_placed", "en", id="A")
    assert tr("status.piece_deleted", "es", id="A") == "Pieza eliminada: A"


def test_delete_piece_yes_removes_piece(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window_with_piece(tmp_path)
    window.workspace.select_piece("A")

    monkeypatch.setattr(
        QMessageBox,
        "question",
        lambda *args, **kwargs: QMessageBox.StandardButton.Yes,
    )
    window._delete_selected_piece()

    project = window.services.projects.current_project
    assert project is not None
    assert [piece.piece_id for piece in project.pieces] == []
    assert project.placement_by_piece_id("A") is None
    assert "Pieza eliminada: A" in window.statusBar().currentMessage()


def test_delete_piece_no_keeps_piece(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window_with_piece(tmp_path)
    window.workspace.select_piece("A")
    was_modified = window.services.projects.is_modified

    monkeypatch.setattr(
        QMessageBox,
        "question",
        lambda *args, **kwargs: QMessageBox.StandardButton.No,
    )
    window._delete_selected_piece()

    project = window.services.projects.current_project
    assert project is not None
    assert [piece.piece_id for piece in project.pieces] == ["A"]
    assert project.placement_by_piece_id("A") is not None
    assert window.services.projects.is_modified == was_modified
