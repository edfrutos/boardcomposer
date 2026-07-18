from studio.commands import DeleteBoardCommand
from studio.explorer_actions import explorer_context_actions
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.services import StudioServices


def _services() -> StudioServices:
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Boards",
            boards=[
                StudioBoard("B1", 2800, 2070, "MDF", 19, 1),
                StudioBoard("B2", 2800, 2070, "MDF", 19, 1),
            ],
            pieces=[
                StudioPiece("A", 400, 300, "MDF", 19),
                StudioPiece("B", 500, 200, "MDF", 19),
            ],
            placements=[
                StudioPlacement(
                    piece_id="A",
                    x_mm=0,
                    y_mm=0,
                    rotated=False,
                    rotation=0,
                    board_id="B1",
                    board_instance=0,
                    stock_panel_index=0,
                ),
                StudioPlacement(
                    piece_id="B",
                    x_mm=0,
                    y_mm=0,
                    rotated=False,
                    rotation=0,
                    board_id="B2",
                    board_instance=0,
                    stock_panel_index=1,
                ),
            ],
        )
    )
    return services


def test_explorer_board_context_includes_delete():
    assert explorer_context_actions("board:B1") == ("edit", "delete")


def test_delete_board_removes_board_and_its_placements_keeps_pieces():
    services = _services()
    command = DeleteBoardCommand(services, "B1")

    command.redo()
    project = services.projects.current_project
    assert project is not None
    assert [board.board_id for board in project.boards] == ["B2"]
    assert [piece.piece_id for piece in project.pieces] == ["A", "B"]
    assert [placement.piece_id for placement in project.placements] == ["B"]

    command.undo()
    assert [board.board_id for board in project.boards] == ["B1", "B2"]
    assert [placement.piece_id for placement in project.placements] == ["A", "B"]
    assert project.placement_by_piece_id("A").board_id == "B1"
