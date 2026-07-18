from studio.commands import DuplicatePieceCommand
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.piece_ids import allocate_unique_piece_id
from studio.services import StudioServices


def _services_with_piece() -> StudioServices:
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Dup",
            boards=[StudioBoard("P1", 1000, 500, "Demo", 19, 1)],
            pieces=[StudioPiece("A", 400, 300, "Demo", 19)],
            placements=[
                StudioPlacement(
                    piece_id="A",
                    x_mm=10,
                    y_mm=20,
                    rotated=False,
                    rotation=0,
                    board_id="P1",
                    board_instance=0,
                    stock_panel_index=0,
                )
            ],
        )
    )
    return services


def test_allocate_unique_piece_id_uses_base_when_free():
    assert allocate_unique_piece_id("A-copy", {"a"}) == "A-copy"


def test_allocate_unique_piece_id_suffixes_when_taken():
    assert allocate_unique_piece_id("A-copy", {"a-copy", "a-copy-2"}) == "A-copy-3"


def test_duplicate_piece_redo_and_undo():
    services = _services_with_piece()
    clone = StudioPiece("A-copy", 400, 300, "Demo", 19)
    placement = StudioPlacement(
        piece_id="A-copy",
        x_mm=30,
        y_mm=40,
        rotated=False,
        rotation=0,
        board_id="P1",
        board_instance=0,
        stock_panel_index=0,
    )
    command = DuplicatePieceCommand(services, clone, placement)

    command.redo()
    project = services.projects.current_project
    assert project is not None
    assert [p.piece_id for p in project.pieces] == ["A", "A-copy"]
    duplicated = project.placement_by_piece_id("A-copy")
    assert duplicated is not None
    assert duplicated.x_mm == 30

    command.undo()
    assert [p.piece_id for p in project.pieces] == ["A"]
    assert project.placement_by_piece_id("A-copy") is None


def test_duplicate_piece_preserves_source_on_undo():
    services = _services_with_piece()
    command = DuplicatePieceCommand(
        services,
        StudioPiece("A-copy", 400, 300, "Demo", 19),
        StudioPlacement(
            piece_id="A-copy",
            x_mm=30,
            y_mm=40,
            rotated=True,
            rotation=90,
            board_id="P1",
            board_instance=0,
            stock_panel_index=0,
        ),
    )
    command.redo()
    command.undo()

    project = services.projects.current_project
    assert project is not None
    source = project.piece_by_id("A")
    assert source.length_mm == 400
    source_placement = project.placement_by_piece_id("A")
    assert source_placement is not None
    assert source_placement.x_mm == 10
