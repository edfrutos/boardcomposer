from studio.commands import MovePieceCommand
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.services import StudioServices


def _services_with_piece_on_panel(panel_index: int, instance: int) -> StudioServices:
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Multipanel",
            boards=[
                StudioBoard("P1", 1000, 500, "Demo", 19, 1),
                StudioBoard("P2", 1000, 500, "Demo", 19, 2),
            ],
            pieces=[StudioPiece("A", 400, 300, "Demo", 19)],
            placements=[
                StudioPlacement(
                    piece_id="A",
                    x_mm=0,
                    y_mm=0,
                    rotated=False,
                    rotation=0,
                    board_id="P1" if panel_index == 0 else "P2",
                    board_instance=instance,
                    stock_panel_index=panel_index,
                )
            ],
        )
    )
    return services


def test_redo_moves_the_piece_to_the_new_position():
    services = _services_with_piece_on_panel(0, 0)
    command = MovePieceCommand(
        services,
        "A",
        old_x=0,
        old_y=0,
        new_x=200,
        new_y=150,
        old_board_id="P1",
        old_board_instance=0,
        old_stock_panel_index=0,
        new_board_id="P1",
        new_board_instance=0,
        new_stock_panel_index=0,
    )

    command.redo()

    placement = services.projects.current_project.placement_by_piece_id("A")
    assert (placement.x_mm, placement.y_mm) == (200, 150)


def test_undo_restores_the_original_position():
    services = _services_with_piece_on_panel(0, 0)
    command = MovePieceCommand(
        services,
        "A",
        old_x=0,
        old_y=0,
        new_x=200,
        new_y=150,
        old_board_id="P1",
        old_board_instance=0,
        old_stock_panel_index=0,
        new_board_id="P1",
        new_board_instance=0,
        new_stock_panel_index=0,
    )

    command.redo()
    command.undo()

    placement = services.projects.current_project.placement_by_piece_id("A")
    assert (placement.x_mm, placement.y_mm) == (0, 0)


def test_redo_reassigns_the_piece_to_a_different_physical_panel():
    services = _services_with_piece_on_panel(0, 0)
    command = MovePieceCommand(
        services,
        "A",
        old_x=0,
        old_y=0,
        new_x=100,
        new_y=100,
        old_board_id="P1",
        old_board_instance=0,
        old_stock_panel_index=0,
        new_board_id="P2",
        new_board_instance=1,
        new_stock_panel_index=1,
    )

    command.redo()

    placement = services.projects.current_project.placement_by_piece_id("A")
    assert placement.board_id == "P2"
    assert placement.board_instance == 1
    assert placement.stock_panel_index == 1


def test_undo_restores_the_original_physical_panel_assignment():
    services = _services_with_piece_on_panel(0, 0)
    command = MovePieceCommand(
        services,
        "A",
        old_x=0,
        old_y=0,
        new_x=100,
        new_y=100,
        old_board_id="P1",
        old_board_instance=0,
        old_stock_panel_index=0,
        new_board_id="P2",
        new_board_instance=1,
        new_stock_panel_index=1,
    )

    command.redo()
    command.undo()

    placement = services.projects.current_project.placement_by_piece_id("A")
    assert placement.board_id == "P1"
    assert placement.board_instance == 0
    assert placement.stock_panel_index == 0


def test_move_command_is_a_noop_when_the_project_has_no_matching_placement():
    services = _services_with_piece_on_panel(0, 0)
    command = MovePieceCommand(
        services,
        "does-not-exist",
        old_x=0,
        old_y=0,
        new_x=100,
        new_y=100,
    )

    command.redo()

    placement = services.projects.current_project.placement_by_piece_id("A")
    assert (placement.x_mm, placement.y_mm) == (0, 0)
