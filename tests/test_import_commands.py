from studio.commands import ImportBoardsCommand, ImportPiecesCommand
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.services import StudioServices


def _empty_project_services() -> tuple[StudioServices, StudioProject]:
    services = StudioServices()
    project = StudioProject(
        project_id="PRJ-1",
        name="Import",
        boards=[],
        pieces=[],
        placements=[],
    )
    services.projects.new_project(project)
    return services, project


def test_import_boards_redo_appends_and_undo_removes():
    services, project = _empty_project_services()
    boards = [
        StudioBoard("B1", 2800, 2070, "MDF", 19, 1),
        StudioBoard("B2", 2800, 2070, "MDF", 19, 2),
    ]
    command = ImportBoardsCommand(services, boards)

    command.redo()
    assert [b.board_id for b in project.boards] == ["B1", "B2"]

    command.undo()
    assert project.boards == []


def test_import_boards_redo_skips_duplicate_ids():
    services, project = _empty_project_services()
    project.boards.append(StudioBoard("B1", 1000, 500, "MDF", 19, 1))
    command = ImportBoardsCommand(
        services,
        [
            StudioBoard("B1", 2800, 2070, "MDF", 19, 1),
            StudioBoard("B2", 1000, 500, "MDF", 16, 1),
        ],
    )

    command.redo()
    ids = [b.board_id for b in project.boards]
    assert ids == ["B1", "B2"]
    assert project.boards[0].length_mm == 1000


def test_import_pieces_redo_and_undo_with_placements():
    services, project = _empty_project_services()
    project.boards.append(StudioBoard("P1", 2800, 2070, "MDF", 19, 1))
    pieces = [
        StudioPiece("A", 400, 300, "MDF", 19),
        StudioPiece("B", 500, 200, "MDF", 19),
    ]
    placements = [
        StudioPlacement(
            piece_id="A",
            x_mm=0,
            y_mm=0,
            rotated=False,
            rotation=0,
            board_id="P1",
            board_instance=0,
            stock_panel_index=0,
        ),
        StudioPlacement(
            piece_id="B",
            x_mm=400,
            y_mm=0,
            rotated=False,
            rotation=0,
            board_id="P1",
            board_instance=0,
            stock_panel_index=0,
        ),
    ]
    command = ImportPiecesCommand(services, pieces, placements)

    command.redo()
    assert [p.piece_id for p in project.pieces] == ["A", "B"]
    assert [pl.piece_id for pl in project.placements] == ["A", "B"]

    command.undo()
    assert project.pieces == []
    assert project.placements == []


def test_import_pieces_undo_preserves_preexisting_pieces():
    services, project = _empty_project_services()
    project.boards.append(StudioBoard("P1", 2800, 2070, "MDF", 19, 1))
    project.pieces.append(StudioPiece("KEEP", 100, 100, "MDF", 19))
    project.placements.append(
        StudioPlacement(
            piece_id="KEEP",
            x_mm=0,
            y_mm=0,
            rotated=False,
            rotation=0,
            board_id="P1",
            board_instance=0,
            stock_panel_index=0,
        )
    )
    command = ImportPiecesCommand(
        services,
        [StudioPiece("NEW", 200, 200, "MDF", 19)],
        [
            StudioPlacement(
                piece_id="NEW",
                x_mm=100,
                y_mm=0,
                rotated=False,
                rotation=0,
                board_id="P1",
                board_instance=0,
                stock_panel_index=0,
            )
        ],
    )

    command.redo()
    command.undo()

    assert [p.piece_id for p in project.pieces] == ["KEEP"]
    assert [pl.piece_id for pl in project.placements] == ["KEEP"]
