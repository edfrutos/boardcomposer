"""Qt interaction regression tests for the Workspace (DT-0004).

These exercise `BoardWorkspace` against a real (offscreen) Qt scene, driving
the same code paths a mouse drag would (`DragController`, `itemChange`,
`constrain_piece_position`, `_finish_piece_drag`) without needing to
synthesize raw mouse events, which tends to be flaky under
`QT_QPA_PLATFORM=offscreen`.
"""

from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.services import StudioServices
from studio.workspace.board_workspace import BoardWorkspace


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


def _drag_to(
    workspace: BoardWorkspace, piece_id: str, x_mm: float, y_mm: float
) -> None:
    """Simulate a full drag: press, move to an absolute scene point, release."""
    item = workspace.piece_item_by_id(piece_id)
    workspace._drag.begin(
        piece_id,
        *workspace._local_item_position(item),
        item.board_id,
        item.board_instance,
        item.stock_panel_index,
    )
    item.setPos(x_mm, y_mm)
    workspace._finish_piece_drag()


def test_reload_project_creates_one_item_per_placement(qapp):
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.reload_project()

    assert len(workspace._piece_items) == 1
    assert workspace.piece_item_by_id("A") is not None
    assert workspace.piece_item_by_id("does-not-exist") is None
    assert not workspace.empty_overlay.isVisible()


def test_empty_workspace_overlay_shows_for_blank_project(qapp):
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


def test_reload_project_creates_a_slot_per_physical_panel_instance(qapp):
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.reload_project()

    assert set(workspace._panel_slots.keys()) == {(0, 0), (0, 1)}


def test_zoom_in_and_out_change_camera_zoom(qapp):
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


def test_reload_project_can_preserve_camera_when_toggling_grid(qapp, tmp_path):
    from dataclasses import replace

    from studio.preferences import PreferencesManager

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


def test_dragging_a_piece_within_its_panel_updates_the_placement(qapp):
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.reload_project()

    _drag_to(workspace, "A", 100, 50)

    placement = services.projects.current_project.placement_by_piece_id("A")
    assert (placement.x_mm, placement.y_mm) == (100, 50)
    assert placement.stock_panel_index == 0
    assert placement.board_instance == 0


def test_dragging_a_piece_into_a_second_physical_panel_reassigns_it(qapp):
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.reload_project()

    second_slot = workspace._panel_slots[(0, 1)]
    _drag_to(workspace, "A", second_slot.x_mm + 50, second_slot.y_mm + 30)

    placement = services.projects.current_project.placement_by_piece_id("A")
    assert placement.stock_panel_index == 0
    assert placement.board_instance == 1
    assert (placement.x_mm, placement.y_mm) == (50, 30)


def test_moving_a_piece_between_panels_pushes_an_undoable_command(qapp):
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.reload_project()

    second_slot = workspace._panel_slots[(0, 1)]
    _drag_to(workspace, "A", second_slot.x_mm + 50, second_slot.y_mm + 30)

    assert services.commands.can_undo()

    services.commands.undo()

    placement = services.projects.current_project.placement_by_piece_id("A")
    assert placement.board_instance == 0
    assert (placement.x_mm, placement.y_mm) == (0, 0)


def test_dropping_a_piece_on_top_of_another_reverts_the_move(qapp):
    services = _multipanel_services()
    project = services.projects.current_project
    project.pieces.append(StudioPiece("B", 400, 300, "Demo", 19))
    project.placements.append(StudioPlacement("B", 500, 0, False, 0, "P1", 0, 0))

    workspace = BoardWorkspace(services)
    workspace.reload_project()

    _drag_to(workspace, "A", 500, 0)

    placement = services.projects.current_project.placement_by_piece_id("A")
    assert (placement.x_mm, placement.y_mm) == (0, 0)
    assert placement.stock_panel_index == 0
    assert placement.board_instance == 0
    assert not services.commands.can_undo()


def test_select_piece_updates_the_shared_selection_manager(qapp):
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.reload_project()

    workspace.select_piece("A")

    assert services.selection.selected_ids == ("A",)


def test_select_all_pieces_selects_every_canvas_piece(qapp):
    services = _multipanel_services()
    project = services.projects.current_project
    project.pieces.append(StudioPiece("B", 200, 100, "Demo", 19))
    project.placements.append(StudioPlacement("B", 500, 0, False, 0, "P1", 0, 0))

    workspace = BoardWorkspace(services)
    workspace.reload_project()
    workspace.select_all_pieces()

    assert set(workspace.selection.selected()) == {"A", "B"}
    assert set(services.selection.selected_ids) == {"A", "B"}
    assert all(item.isSelected() for item in workspace._piece_items)


def test_left_click_empty_clears_piece_selection(qapp):
    from PySide6.QtCore import QEvent, QPointF, Qt
    from PySide6.QtGui import QMouseEvent

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


def test_clear_piece_selection_after_select_all(qapp):
    services = _multipanel_services()
    project = services.projects.current_project
    project.pieces.append(StudioPiece("B", 200, 100, "Demo", 19))
    project.placements.append(StudioPlacement("B", 500, 0, False, 0, "P1", 0, 0))

    workspace = BoardWorkspace(services)
    workspace.reload_project()
    workspace.select_all_pieces()
    workspace.clear_piece_selection()

    assert workspace.selection.selected() == []
    assert services.selection.selected_ids == ()
    assert all(not item.isSelected() for item in workspace._piece_items)


def test_invert_piece_selection_swaps_selected_set(qapp):
    services = _multipanel_services()
    project = services.projects.current_project
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


def test_rotating_a_piece_that_would_leave_the_panel_is_rejected(qapp):
    services = _multipanel_services()
    project = services.projects.current_project
    project.placements[0].x_mm = 950
    project.placements[0].y_mm = 0

    workspace = BoardWorkspace(services)
    workspace.reload_project()

    item = workspace.piece_item_by_id("A")
    assert workspace.can_rotate_item(item, 90) is False


def test_middle_button_on_piece_pans_without_moving_placement(qapp):
    from PySide6.QtCore import QEvent, QPoint, QPointF, Qt
    from PySide6.QtGui import QMouseEvent

    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.resize(800, 600)
    workspace.reload_project()

    piece = workspace.piece_item_by_id("A")
    assert piece is not None
    start = workspace.mapFromScene(piece.sceneBoundingRect().center())
    end = start + QPoint(50, 30)
    center_before = QPointF(workspace._camera.center)
    placement = services.projects.current_project.placement_by_piece_id("A")
    assert placement is not None
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
    placement_after = services.projects.current_project.placement_by_piece_id("A")
    assert placement_after is not None
    assert (placement_after.x_mm, placement_after.y_mm) == position_before


def test_space_left_drag_on_piece_pans_without_moving_placement(qapp):
    from PySide6.QtCore import QEvent, QPoint, QPointF, Qt
    from PySide6.QtGui import QKeyEvent, QMouseEvent

    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.resize(800, 600)
    workspace.reload_project()

    piece = workspace.piece_item_by_id("A")
    assert piece is not None
    start = workspace.mapFromScene(piece.sceneBoundingRect().center())
    end = start + QPoint(40, 25)
    center_before = QPointF(workspace._camera.center)
    placement = services.projects.current_project.placement_by_piece_id("A")
    assert placement is not None
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
    placement_after = services.projects.current_project.placement_by_piece_id("A")
    assert placement_after is not None
    assert (placement_after.x_mm, placement_after.y_mm) == position_before
