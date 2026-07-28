"""Fit camera to the current piece/board selection."""

from PySide6.QtCore import QPointF

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from studio.workspace.board_workspace import BoardWorkspace


def _multipanel_services() -> StudioServices:
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="FitSel",
            boards=[
                StudioBoard("B1", 1000, 500, "Demo", 19, 1),
                StudioBoard("B2", 800, 400, "Demo", 19, 1),
            ],
            pieces=[StudioPiece("A", 200, 150, "Demo", 19)],
            placements=[
                StudioPlacement("A", 10, 20, False, 0, "B1", 0, 0),
            ],
        )
    )
    return services


def test_fit_selection_zooms_to_piece(qapp):
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.resize(800, 600)
    workspace.reload_project()
    workspace.fit_board()
    zoom_before = workspace._camera.zoom
    center_before = QPointF(workspace._camera.center)

    workspace.select_piece("A")
    assert workspace.fit_selection() is True

    piece = workspace.piece_item_by_id("A")
    assert piece is not None
    assert workspace._camera.center == piece.sceneBoundingRect().center()
    assert (
        workspace._camera.zoom != zoom_before
        or workspace._camera.center != center_before
    )
    assert workspace._camera.zoom >= zoom_before


def test_fit_selection_zooms_to_focused_board(qapp):
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.resize(800, 600)
    workspace.reload_project()
    workspace.fit_board()
    zoom_all = workspace._camera.zoom

    workspace.focus_board("B2")
    assert workspace.fit_selection() is True

    b2_slots = [
        slot for slot in workspace._panel_slots.values() if slot.board_id == "B2"
    ]
    assert len(b2_slots) == 1
    expected = workspace._board_items[b2_slots[0].key].sceneBoundingRect()
    assert workspace._camera.center == expected.center()
    assert workspace._camera.zoom > zoom_all


def test_fit_selection_without_target_returns_false(qapp):
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.resize(800, 600)
    workspace.reload_project()
    workspace.clear_piece_selection()

    assert workspace.fit_selection() is False


def test_fit_selection_action_and_status(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-2",
            name="FitAction",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 200, 100, "Demo", 19)],
            placements=[StudioPlacement("A", 0, 0, False, 0, "B1", 0, 0)],
        )
    )
    window = MainWindow(services)
    window.workspace.resize(800, 600)
    window.workspace.reload_project()
    window.workspace.clear_piece_selection()

    assert window._actions["fit_selection"].shortcut().toString() in {
        "Ctrl+Shift+0",
        "Ctrl+⇧+0",
    }

    window._fit_selection()
    assert window._tr("status.nothing_to_fit_selection") in (
        window.statusBar().currentMessage()
    )

    window.workspace.select_piece("A")
    window._fit_selection()
    piece = window.workspace.piece_item_by_id("A")
    assert piece is not None
    assert window.workspace._camera.center == piece.sceneBoundingRect().center()


def test_fit_board_without_boards_returns_false(qapp):
    services = StudioServices()
    services.projects.new_project(
        StudioProject(project_id="PRJ-EMPTY", name="Empty", boards=[], pieces=[])
    )
    workspace = BoardWorkspace(services)
    workspace.resize(800, 600)
    workspace.reload_project()

    assert workspace.fit_board() is False


def test_fit_board_action_status_without_boards(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(project_id="PRJ-EMPTY", name="Empty", boards=[], pieces=[])
    )
    window = MainWindow(services)
    window.workspace.resize(800, 600)
    window.workspace.reload_project()

    window._fit_board()
    assert window._tr("status.nothing_to_fit_board") in (
        window.statusBar().currentMessage()
    )


def test_fit_board_returns_true_with_boards(qapp):
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.resize(800, 600)
    workspace.reload_project()

    assert workspace.fit_board() is True
