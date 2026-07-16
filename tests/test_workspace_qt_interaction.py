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


def test_reload_project_creates_a_slot_per_physical_panel_instance(qapp):
    services = _multipanel_services()
    workspace = BoardWorkspace(services)
    workspace.reload_project()

    assert set(workspace._panel_slots.keys()) == {(0, 0), (0, 1)}


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


def test_rotating_a_piece_that_would_leave_the_panel_is_rejected(qapp):
    services = _multipanel_services()
    project = services.projects.current_project
    project.placements[0].x_mm = 950
    project.placements[0].y_mm = 0

    workspace = BoardWorkspace(services)
    workspace.reload_project()

    item = workspace.piece_item_by_id("A")
    assert workspace.can_rotate_item(item, 90) is False
