"""Tests for AddBoardCommand / AddPieceCommand (FLW-006)."""

from studio.commands import AddBoardCommand, AddPieceCommand
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.services import StudioServices


def _empty_project_services() -> tuple[StudioServices, StudioProject]:
    services = StudioServices()
    project = StudioProject(
        project_id="PRJ-1",
        name="Add",
        boards=[],
        pieces=[],
        placements=[],
    )
    services.projects.new_project(project)
    return services, project


def test_add_board_redo_and_undo():
    services, project = _empty_project_services()
    board = StudioBoard("B1", 2800, 2070, "MDF", 19, 2)
    command = AddBoardCommand(services, board)

    services.commands.execute(command)
    assert [b.board_id for b in project.boards] == ["B1"]
    assert services.commands.can_undo()

    services.commands.undo()
    assert project.boards == []
    assert services.commands.can_redo()

    services.commands.redo()
    assert [b.board_id for b in project.boards] == ["B1"]


def test_add_board_redo_skips_if_id_already_present():
    services, project = _empty_project_services()
    project.boards.append(StudioBoard("B1", 1000, 500, "MDF", 19, 1))
    command = AddBoardCommand(services, StudioBoard("B1", 2800, 2070, "MDF", 16, 1))

    command.redo()
    assert len(project.boards) == 1
    assert project.boards[0].length_mm == 1000


def test_add_piece_redo_and_undo_with_placements():
    services, project = _empty_project_services()
    project.boards.append(StudioBoard("TAB", 2800, 2070, "MDF", 19, 1))
    pieces = [
        StudioPiece("P-1", 400, 300, "MDF", 19),
        StudioPiece("P-2", 400, 300, "MDF", 19),
    ]
    placements = [
        StudioPlacement(
            piece_id="P-1",
            x_mm=0,
            y_mm=0,
            rotated=False,
            rotation=0,
            board_id="TAB",
            board_instance=0,
            stock_panel_index=0,
        ),
        StudioPlacement(
            piece_id="P-2",
            x_mm=400,
            y_mm=0,
            rotated=False,
            rotation=0,
            board_id="TAB",
            board_instance=0,
            stock_panel_index=0,
        ),
    ]
    command = AddPieceCommand(services, pieces, placements)
    assert command.name == "Añadir piezas"

    services.commands.execute(command)
    assert [p.piece_id for p in project.pieces] == ["P-1", "P-2"]
    assert [pl.piece_id for pl in project.placements] == ["P-1", "P-2"]

    services.commands.undo()
    assert project.pieces == []
    assert project.placements == []


def test_add_piece_undo_preserves_preexisting():
    services, project = _empty_project_services()
    project.pieces.append(StudioPiece("KEEP", 100, 100, "MDF", 19))
    project.placements.append(
        StudioPlacement(
            piece_id="KEEP",
            x_mm=0,
            y_mm=0,
            rotated=False,
            rotation=0,
            board_id=None,
            board_instance=0,
            stock_panel_index=None,
        )
    )
    command = AddPieceCommand(
        services,
        [StudioPiece("NEW", 200, 200, "MDF", 19)],
        [
            StudioPlacement(
                piece_id="NEW",
                x_mm=10,
                y_mm=10,
                rotated=False,
                rotation=0,
                board_id=None,
                board_instance=0,
                stock_panel_index=None,
            )
        ],
    )

    command.redo()
    command.undo()
    assert [p.piece_id for p in project.pieces] == ["KEEP"]
    assert [pl.piece_id for pl in project.placements] == ["KEEP"]
