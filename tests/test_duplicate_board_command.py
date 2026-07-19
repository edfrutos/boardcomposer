from studio.board_ids import allocate_unique_board_id
from studio.commands import DuplicateBoardCommand
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.services import StudioServices


def _services_with_board() -> StudioServices:
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Dup",
            boards=[StudioBoard("B1", 3000, 1000, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 400, 300, "Demo", 19)],
            placements=[
                StudioPlacement(
                    piece_id="A",
                    x_mm=10,
                    y_mm=20,
                    rotated=False,
                    rotation=0,
                    board_id="B1",
                    board_instance=0,
                    stock_panel_index=0,
                )
            ],
        )
    )
    return services


def test_allocate_unique_board_id_uses_base_when_free():
    assert allocate_unique_board_id("B1-copy", {"b1"}) == "B1-copy"


def test_allocate_unique_board_id_suffixes_when_taken():
    assert allocate_unique_board_id("B1-copy", {"b1-copy", "b1-copy-2"}) == "B1-copy-3"


def test_duplicate_board_redo_and_undo():
    services = _services_with_board()
    clone = StudioBoard("B1-copy", 3000, 1000, "Demo", 19, 1)
    command = DuplicateBoardCommand(services, clone)

    command.redo()
    project = services.projects.current_project
    assert project is not None
    assert [board.board_id for board in project.boards] == ["B1", "B1-copy"]
    cloned = next(board for board in project.boards if board.board_id == "B1-copy")
    assert cloned.length_mm == 3000
    assert cloned.width_mm == 1000
    assert cloned.material == "Demo"
    assert cloned.thickness_mm == 19
    assert cloned.quantity == 1

    command.undo()
    assert [board.board_id for board in project.boards] == ["B1"]


def test_duplicate_board_preserves_pieces_and_placements():
    services = _services_with_board()
    command = DuplicateBoardCommand(
        services,
        StudioBoard("B1-copy", 3000, 1000, "Demo", 19, 1),
    )
    command.redo()
    command.undo()

    project = services.projects.current_project
    assert project is not None
    assert [piece.piece_id for piece in project.pieces] == ["A"]
    placement = project.placement_by_piece_id("A")
    assert placement is not None
    assert placement.board_id == "B1"
    assert placement.x_mm == 10
