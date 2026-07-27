"""Qt interaction regression tests for the Workspace (DT-0004).

These exercise `BoardWorkspace` against a real (offscreen) Qt scene, driving
the same code paths a mouse drag would (`DragController`, `itemChange`,
`constrain_piece_position`, `_finish_piece_drag`) without needing to
synthesize raw mouse events, which tends to be flaky under
`QT_QPA_PLATFORM=offscreen`.
"""

# White-box Qt tests intentionally touch private helpers and keep empty
# selection checks explicit (`== []` / `== ()`).
# pylint: disable=protected-access,use-implicit-booleaness-not-comparison

from dataclasses import replace

import pytest
from PySide6.QtCore import QEvent, QPoint, QPointF, Qt
from PySide6.QtGui import QKeyEvent, QMouseEvent

from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from studio.workspace.board_piece_item import BoardPieceItem
from studio.workspace.board_workspace import BoardWorkspace

pytestmark = pytest.mark.usefixtures("qapp")


def _multipanel_services() -> StudioServices:
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Multipanel",
            boards=[StudioBoard("P1", 1000, 500, "Demo", 19, 2)],
            pieces=[StudioPiece("A", 400, 300, "Demo", 19)],
            placements=[
                StudioPlacement("A", 0, 0, False, 0, "P1", 0, 0),
            ],
        )
    )
    return services


def _require_project(services: StudioServices) -> StudioProject:
    project = services.projects.current_project
    assert project is not None
    return project


def _require_piece_item(workspace: BoardWorkspace, piece_id: str) -> BoardPieceItem:
    item = workspace.piece_item_by_id(piece_id)
    assert item is not None
    return item


def _require_placement(services: StudioServices, piece_id: str) -> StudioPlacement:
    placement = _require_project(services).placement_by_piece_id(piece_id)
    assert placement is not None
    return placement


def _drag_to(
    workspace: BoardWorkspace, piece_id: str, x_mm: float, y_mm: float
) -> None:
    """Simulate a full drag: press, move to an absolute scene point, release."""
    item = _require_piece_item(workspace, piece_id)
    workspace._drag.begin(
        piece_id,
        *workspace._local_item_position(item),
        item.board_id,
        item.board_instance,
        item.stock_panel_index,
    )
    item.setPos(x_mm, y_mm)
    workspace._finish_piece_drag()


def test_reload_project_creates_one_item_per_placement():
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.reload_project()

    assert len(workspace._piece_items) == 1
    assert workspace.piece_item_by_id("A") is not None
    assert workspace.piece_item_by_id("does-not-exist") is None
    assert not workspace.empty_overlay.isVisible()


def test_empty_workspace_overlay_shows_for_blank_project():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-EMPTY",
            name="Empty",
            boards=[],
            pieces=[],
            placements=[],
        )
    )
    workspace = BoardWorkspace(services)
    workspace.resize(800, 600)
    workspace.retranslate("en")
    workspace.reload_project()

    assert workspace._project_is_empty()
    assert not workspace.empty_overlay.isHidden()
    assert workspace.empty_overlay.title.text() == "Start your project"
    assert workspace.empty_overlay.add_board_button.text() == "Add board…"
    assert workspace.empty_overlay.add_board_button.objectName() == "primaryButton"
    assert workspace.empty_overlay.add_board_button.minimumHeight() >= 44
    assert workspace.empty_overlay.add_piece_button.minimumHeight() >= 36
    assert workspace.empty_overlay.import_boards_button.minimumHeight() >= 36
    assert workspace.empty_overlay.import_pieces_button.minimumHeight() >= 36


def test_reload_project_creates_a_slot_per_physical_panel_instance():
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.reload_project()

    assert set(workspace._panel_slots.keys()) == {(0, 0), (0, 1)}


def test_zoom_in_and_out_change_camera_zoom():
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.resize(800, 600)
    workspace.reload_project()
    baseline = workspace._camera.zoom

    workspace.zoom_in()
    assert workspace._camera.zoom > baseline

    zoomed = workspace._camera.zoom
    workspace.zoom_out()
    assert workspace._camera.zoom < zoomed


def test_reload_project_can_preserve_camera_when_toggling_grid(tmp_path):
    services = _multipanel_services()
    services.preferences = PreferencesManager(tmp_path / "preferences.json")
    workspace = BoardWorkspace(services)
    workspace.resize(800, 600)
    workspace.reload_project()
    workspace._camera.zoom = workspace._camera.clamp_zoom(2.5)
    workspace._apply_camera()
    zoom = workspace._camera.zoom

    services.preferences.update(replace(services.preferences.current, show_grid=False))
    workspace.reload_project(fit=False)

    assert workspace._camera.zoom == zoom
    assert services.preferences.current.show_grid is False


def test_dragging_a_piece_within_its_panel_updates_the_placement():
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.reload_project()

    _drag_to(workspace, "A", 100, 50)

    placement = _require_placement(services, "A")
    assert (placement.x_mm, placement.y_mm) == (100, 50)
    assert placement.stock_panel_index == 0
    assert placement.board_instance == 0


def test_dragging_a_piece_into_a_second_physical_panel_reassigns_it():
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.reload_project()

    second_slot = workspace._panel_slots[(0, 1)]
    _drag_to(workspace, "A", second_slot.x_mm + 50, second_slot.y_mm + 30)

    placement = _require_placement(services, "A")
    assert placement.stock_panel_index == 0
    assert placement.board_instance == 1
    assert (placement.x_mm, placement.y_mm) == (50, 30)


def test_moving_a_piece_between_panels_pushes_an_undoable_command():
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.reload_project()

    second_slot = workspace._panel_slots[(0, 1)]
    _drag_to(workspace, "A", second_slot.x_mm + 50, second_slot.y_mm + 30)

    assert services.commands.can_undo()

    services.commands.undo()

    placement = _require_placement(services, "A")
    assert placement.board_instance == 0
    assert (placement.x_mm, placement.y_mm) == (0, 0)


def test_drag_rejects_incompatible_thickness_and_material():
    """18 mm Melamina piece must not land on a 5 mm Tablex panel."""
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-MIX",
            name="Mix",
            boards=[
                StudioBoard("MEL", 1000, 500, "Melamina", 18, 1),
                StudioBoard("TAB", 1000, 500, "Tablex", 5, 1),
            ],
            pieces=[StudioPiece("A", 400, 300, "Melamina", 18)],
            placements=[
                StudioPlacement("A", 0, 0, False, 0, "MEL", 0, 0),
            ],
        )
    )
    workspace = BoardWorkspace(services)
    workspace.reload_project()

    tablex = workspace._panel_slots[(1, 0)]
    _drag_to(workspace, "A", tablex.x_mm + 50, tablex.y_mm + 30)

    placement = _require_placement(services, "A")
    assert placement.board_id == "MEL"
    assert placement.stock_panel_index == 0
    assert placement.board_id != "TAB"
    assert (placement.x_mm, placement.y_mm) == (0, 0)
    assert not services.commands.can_undo()


def test_dropping_a_piece_on_top_of_another_reverts_the_move():
    services = _multipanel_services()
    project = _require_project(services)
    project.pieces.append(StudioPiece("B", 400, 300, "Demo", 19))
    project.placements.append(StudioPlacement("B", 500, 0, False, 0, "P1", 0, 0))

    workspace = BoardWorkspace(services)
    workspace.reload_project()

    _drag_to(workspace, "A", 500, 0)

    placement = _require_placement(services, "A")
    assert (placement.x_mm, placement.y_mm) == (0, 0)
    assert placement.stock_panel_index == 0
    assert placement.board_instance == 0
    assert not services.commands.can_undo()


def test_select_piece_updates_the_shared_selection_manager():
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.reload_project()

    workspace.select_piece("A")

    assert services.selection.selected_ids == ("A",)


def test_select_all_pieces_selects_every_canvas_piece():
    services = _multipanel_services()
    project = _require_project(services)
    project.pieces.append(StudioPiece("B", 200, 100, "Demo", 19))
    project.placements.append(StudioPlacement("B", 500, 0, False, 0, "P1", 0, 0))

    workspace = BoardWorkspace(services)
    workspace.reload_project()
    workspace.select_all_pieces()

    assert set(workspace.selection.selected()) == {"A", "B"}
    assert set(services.selection.selected_ids) == {"A", "B"}
    assert all(item.isSelected() for item in workspace._piece_items)


def test_left_click_empty_clears_piece_selection():
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.resize(800, 600)
    workspace.reload_project()
    workspace.select_piece("A")
    assert workspace.selection.selected() == ["A"]

    local = QPointF(20, 20)
    press = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        local,
        local,
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    release = QMouseEvent(
        QEvent.Type.MouseButtonRelease,
        local,
        local,
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    original_item_at = workspace.itemAt
    workspace.itemAt = lambda _point: None  # type: ignore[method-assign]
    try:
        workspace.mousePressEvent(press)
        workspace.mouseReleaseEvent(release)
    finally:
        workspace.itemAt = original_item_at  # type: ignore[method-assign]

    assert workspace.selection.selected() == []
    assert services.selection.selected_ids == ()


def test_clear_piece_selection_after_select_all():
    services = _multipanel_services()
    project = _require_project(services)
    project.pieces.append(StudioPiece("B", 200, 100, "Demo", 19))
    project.placements.append(StudioPlacement("B", 500, 0, False, 0, "P1", 0, 0))

    workspace = BoardWorkspace(services)
    workspace.reload_project()
    workspace.select_all_pieces()
    workspace.clear_piece_selection()

    assert workspace.selection.selected() == []
    assert services.selection.selected_ids == ()
    assert all(not item.isSelected() for item in workspace._piece_items)


def test_invert_piece_selection_swaps_selected_set():
    services = _multipanel_services()
    project = _require_project(services)
    project.pieces.append(StudioPiece("B", 200, 100, "Demo", 19))
    project.pieces.append(StudioPiece("C", 150, 100, "Demo", 19))
    project.placements.append(StudioPlacement("B", 500, 0, False, 0, "P1", 0, 0))
    project.placements.append(StudioPlacement("C", 700, 0, False, 0, "P1", 0, 0))

    workspace = BoardWorkspace(services)
    workspace.reload_project()
    workspace.select_piece("A")
    workspace.invert_piece_selection()

    assert set(workspace.selection.selected()) == {"B", "C"}
    assert set(services.selection.selected_ids) == {"B", "C"}


def test_rotating_a_piece_that_would_leave_the_panel_is_rejected():
    services = _multipanel_services()
    project = _require_project(services)
    project.placements[0].x_mm = 950
    project.placements[0].y_mm = 0

    workspace = BoardWorkspace(services)
    workspace.reload_project()

    item = _require_piece_item(workspace, "A")
    assert workspace.can_rotate_item(item, 90) is False


def test_r_key_emits_rotate_requested_when_piece_selected():
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.reload_project()
    workspace.select_piece("A")

    seen: list[bool] = []
    workspace.rotate_requested.connect(lambda: seen.append(True))

    event = QKeyEvent(
        QEvent.Type.KeyPress,
        Qt.Key.Key_R,
        Qt.KeyboardModifier.NoModifier,
    )
    workspace.keyPressEvent(event)

    assert seen == [True]
    assert event.isAccepted()


def test_r_key_ignored_without_selection():
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.reload_project()

    seen: list[bool] = []
    workspace.rotate_requested.connect(lambda: seen.append(True))

    event = QKeyEvent(
        QEvent.Type.KeyPress,
        Qt.Key.Key_R,
        Qt.KeyboardModifier.NoModifier,
    )
    workspace.keyPressEvent(event)

    assert seen == []


def test_middle_button_on_piece_pans_without_moving_placement():
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.resize(800, 600)
    workspace.reload_project()

    piece = _require_piece_item(workspace, "A")
    start = workspace.mapFromScene(piece.sceneBoundingRect().center())
    end = start + QPoint(50, 30)
    center_before = QPointF(workspace._camera.center)
    placement = _require_placement(services, "A")
    position_before = (placement.x_mm, placement.y_mm)

    press = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPointF(start),
        QPointF(workspace.mapToGlobal(start)),
        Qt.MouseButton.MiddleButton,
        Qt.MouseButton.MiddleButton,
        Qt.KeyboardModifier.NoModifier,
    )
    workspace.mousePressEvent(press)
    assert workspace._panning
    assert workspace._drag.drag_start is None

    move = QMouseEvent(
        QEvent.Type.MouseMove,
        QPointF(end),
        QPointF(workspace.mapToGlobal(end)),
        Qt.MouseButton.NoButton,
        Qt.MouseButton.MiddleButton,
        Qt.KeyboardModifier.NoModifier,
    )
    workspace.mouseMoveEvent(move)

    release = QMouseEvent(
        QEvent.Type.MouseButtonRelease,
        QPointF(end),
        QPointF(workspace.mapToGlobal(end)),
        Qt.MouseButton.MiddleButton,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )
    workspace.mouseReleaseEvent(release)

    assert not workspace._panning
    assert workspace._camera.center != center_before
    placement_after = _require_placement(services, "A")
    assert (placement_after.x_mm, placement_after.y_mm) == position_before


def test_space_left_drag_on_piece_pans_without_moving_placement():
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.resize(800, 600)
    workspace.reload_project()

    piece = _require_piece_item(workspace, "A")
    start = workspace.mapFromScene(piece.sceneBoundingRect().center())
    end = start + QPoint(40, 25)
    center_before = QPointF(workspace._camera.center)
    placement = _require_placement(services, "A")
    position_before = (placement.x_mm, placement.y_mm)

    space_press = QKeyEvent(
        QEvent.Type.KeyPress,
        Qt.Key.Key_Space,
        Qt.KeyboardModifier.NoModifier,
    )
    workspace.keyPressEvent(space_press)
    assert workspace._space_held

    press = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPointF(start),
        QPointF(workspace.mapToGlobal(start)),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    workspace.mousePressEvent(press)
    assert workspace._panning
    assert workspace._drag.drag_start is None

    move = QMouseEvent(
        QEvent.Type.MouseMove,
        QPointF(end),
        QPointF(workspace.mapToGlobal(end)),
        Qt.MouseButton.NoButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    workspace.mouseMoveEvent(move)

    release = QMouseEvent(
        QEvent.Type.MouseButtonRelease,
        QPointF(end),
        QPointF(workspace.mapToGlobal(end)),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )
    workspace.mouseReleaseEvent(release)

    space_release = QKeyEvent(
        QEvent.Type.KeyRelease,
        Qt.Key.Key_Space,
        Qt.KeyboardModifier.NoModifier,
    )
    workspace.keyReleaseEvent(space_release)

    assert not workspace._panning
    assert not workspace._space_held
    assert workspace._camera.center != center_before
    placement_after = _require_placement(services, "A")
    assert (placement_after.x_mm, placement_after.y_mm) == position_before


def test_arrow_nudge_moves_selected_piece():
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.resize(800, 600)
    workspace.reload_project()
    workspace.select_piece("A")

    placement = _require_placement(services, "A")
    x_before, y_before = placement.x_mm, placement.y_mm

    right = QKeyEvent(
        QEvent.Type.KeyPress,
        Qt.Key.Key_Right,
        Qt.KeyboardModifier.NoModifier,
    )
    workspace.keyPressEvent(right)

    placement_after = _require_placement(services, "A")
    assert placement_after.x_mm == x_before + 1.0
    assert placement_after.y_mm == y_before
    assert services.commands.can_undo()


def test_shift_arrow_nudge_uses_grid_size(tmp_path):
    services = _multipanel_services()
    services.preferences = PreferencesManager(tmp_path / "preferences.json")
    services.preferences.update(StudioPreferences(grid_size_mm=50))
    workspace = BoardWorkspace(services)
    workspace.resize(800, 600)
    workspace.reload_project()
    workspace.select_piece("A")

    placement = _require_placement(services, "A")
    y_before = placement.y_mm

    down = QKeyEvent(
        QEvent.Type.KeyPress,
        Qt.Key.Key_Down,
        Qt.KeyboardModifier.ShiftModifier,
    )
    workspace.keyPressEvent(down)

    placement_after = _require_placement(services, "A")
    assert placement_after.y_mm == y_before + 50.0


def test_arrow_without_selection_is_ignored():
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.reload_project()
    workspace.clear_piece_selection()

    placement = _require_placement(services, "A")
    before = (placement.x_mm, placement.y_mm)

    handled = workspace.nudge_selected_piece(1.0, 0.0)
    assert handled is False
    assert (placement.x_mm, placement.y_mm) == before
