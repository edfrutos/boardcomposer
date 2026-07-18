from studio.commands import EditBoardCommand, EditPieceCommand
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.services import StudioServices


def _services() -> StudioServices:
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Edit",
            boards=[StudioBoard("B1", 2800, 2070, "MDF", 19, 2)],
            pieces=[StudioPiece("A", 400, 300, "MDF", 19)],
            placements=[
                StudioPlacement(
                    piece_id="A",
                    x_mm=10,
                    y_mm=20,
                    rotated=False,
                    rotation=0,
                    board_id="B1",
                    board_instance=1,
                    stock_panel_index=0,
                )
            ],
        )
    )
    return services


def test_edit_piece_redo_and_undo_renames_placement():
    services = _services()
    old = StudioPiece("A", 400, 300, "MDF", 19)
    new = StudioPiece("A2", 450, 320, "Roble", 16)
    command = EditPieceCommand(services, old, new)

    command.redo()
    project = services.projects.current_project
    assert project is not None
    assert [p.piece_id for p in project.pieces] == ["A2"]
    assert project.piece_by_id("A2").length_mm == 450
    placement = project.placement_by_piece_id("A2")
    assert placement is not None
    assert project.placement_by_piece_id("A") is None

    command.undo()
    assert [p.piece_id for p in project.pieces] == ["A"]
    assert project.piece_by_id("A").material == "MDF"
    assert project.placement_by_piece_id("A") is not None
    assert project.placement_by_piece_id("A2") is None


def test_edit_board_redo_and_undo_clamps_instance():
    services = _services()
    old = StudioBoard("B1", 2800, 2070, "MDF", 19, 2)
    new = StudioBoard("STOCK", 3000, 2000, "MDF", 19, 1)
    command = EditBoardCommand(services, old, new)

    command.redo()
    project = services.projects.current_project
    assert project is not None
    assert project.boards[0].board_id == "STOCK"
    placement = project.placements[0]
    assert placement.board_id == "STOCK"
    assert placement.board_instance == 0

    command.undo()
    assert project.boards[0].board_id == "B1"
    assert project.placements[0].board_id == "B1"
    assert project.placements[0].board_instance == 1
