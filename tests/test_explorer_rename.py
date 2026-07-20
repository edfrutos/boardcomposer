"""Rename piece/board from the Explorador context menu."""

from PySide6.QtWidgets import QInputDialog

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
            name="Rename",
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


def test_rename_piece_from_explorer(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    monkeypatch.setattr(
        QInputDialog,
        "getText",
        lambda *args, **kwargs: ("A2", True),
    )

    window._rename_piece("A")

    project = window.services.projects.current_project
    assert project is not None
    assert [piece.piece_id for piece in project.pieces] == ["A2"]
    assert project.placement_by_piece_id("A2") is not None
    assert project.placement_by_piece_id("A") is None
    assert window.workspace.selection.selected() == ["A2"]
    assert "A2" in window.statusBar().currentMessage()


def test_f2_rename_selection_renames_explorer_piece(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    item = window._find_explorer_item_by_role("piece:A")
    assert item is not None
    window.explorer.setCurrentItem(item)
    monkeypatch.setattr(
        QInputDialog,
        "getText",
        lambda *args, **kwargs: ("A2", True),
    )

    window._actions["rename_selection"].trigger()

    project = window.services.projects.current_project
    assert project is not None
    assert [piece.piece_id for piece in project.pieces] == ["A2"]
    assert window._actions["rename_selection"].shortcut().toString() == "F2"


def test_f2_rename_selection_without_target_shows_status(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.explorer.setCurrentItem(None)
    window.workspace.clear_piece_selection()

    window._rename_selection()

    assert window._tr("status.nothing_to_rename_selection") in (
        window.statusBar().currentMessage()
    )


def test_rename_board_from_explorer(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    monkeypatch.setattr(
        QInputDialog,
        "getText",
        lambda *args, **kwargs: ("B2", True),
    )

    window._rename_board("B1")

    project = window.services.projects.current_project
    assert project is not None
    assert [board.board_id for board in project.boards] == ["B2"]
    placement = project.placement_by_piece_id("A")
    assert placement is not None
    assert placement.board_id == "B2"
    assert window.workspace.focused_board_id() == "B2"
    assert "B2" in window.statusBar().currentMessage()


def test_rename_piece_cancel_keeps_id(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    monkeypatch.setattr(
        QInputDialog,
        "getText",
        lambda *args, **kwargs: ("A2", False),
    )

    window._rename_piece("A")

    project = window.services.projects.current_project
    assert project is not None
    assert [piece.piece_id for piece in project.pieces] == ["A"]
