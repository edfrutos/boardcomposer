from studio.commands import SwapPiecesCommand
from studio.events.catalog import PIECE_MOVED
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.services import StudioServices
from studio.swap_pieces import swap_block_reason


def _two_placed(
    *,
    second_board: str = "P1",
    second_instance: int = 0,
    second_index: int = 0,
    a_size: tuple[float, float] = (200, 100),
    b_size: tuple[float, float] = (200, 100),
    a_pos: tuple[float, float] = (0, 0),
    b_pos: tuple[float, float] = (300, 0),
    a_material: str = "Demo",
    b_material: str = "Demo",
    extra: list[StudioPiece] | None = None,
    extra_placements: list[StudioPlacement] | None = None,
) -> StudioServices:
    boards = [
        StudioBoard("P1", 1000, 500, "Demo", 19, 1),
        StudioBoard("P2", 1000, 500, "Demo", 19, 1),
    ]
    pieces = [
        StudioPiece("A", a_size[0], a_size[1], a_material, 19),
        StudioPiece("B", b_size[0], b_size[1], b_material, 19),
        *(extra or []),
    ]
    placements = [
        StudioPlacement("A", a_pos[0], a_pos[1], False, 0, "P1", 0, 0),
        StudioPlacement(
            "B",
            b_pos[0],
            b_pos[1],
            False,
            0,
            second_board,
            second_instance,
            second_index,
        ),
        *(extra_placements or []),
    ]
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Swap",
            boards=boards,
            pieces=pieces,
            placements=placements,
        )
    )
    return services


def test_swap_exchanges_seats_and_undo_restores():
    services = _two_placed(second_board="P2", second_instance=0, second_index=1)
    seen: list[dict] = []
    services.events.subscribe(PIECE_MOVED, lambda _n, payload: seen.append(payload))
    command = SwapPiecesCommand(services, "A", "B")
    services.commands.execute(command)

    project = services.projects.current_project
    a = project.placement_by_piece_id("A")
    b = project.placement_by_piece_id("B")
    assert (a.x_mm, a.y_mm, a.board_id) == (300, 0, "P2")
    assert (b.x_mm, b.y_mm, b.board_id) == (0, 0, "P1")
    assert a.rotation == 0 and b.rotation == 0
    assert {event["piece"] for event in seen} == {"A", "B"}
    assert any(event["kind"] == "reassigned" for event in seen)

    services.commands.undo()
    a = project.placement_by_piece_id("A")
    b = project.placement_by_piece_id("B")
    assert (a.x_mm, a.y_mm, a.board_id) == (0, 0, "P1")
    assert (b.x_mm, b.y_mm, b.board_id) == (300, 0, "P2")


def test_swap_same_panel_keeps_rotation():
    services = _two_placed()
    project = services.projects.current_project
    project.placement_by_piece_id("A").rotation = 90
    command = SwapPiecesCommand(services, "A", "B")
    command.redo()
    a = project.placement_by_piece_id("A")
    b = project.placement_by_piece_id("B")
    assert (a.x_mm, a.y_mm) == (300, 0)
    assert (b.x_mm, b.y_mm) == (0, 0)
    assert a.rotation == 90
    assert b.rotation == 0


def test_swap_blocked_when_piece_unplaced():
    services = _two_placed()
    project = services.projects.current_project
    project.placements = [p for p in project.placements if p.piece_id != "B"]
    assert swap_block_reason(project, "A", "B") == "status.swap_need_placed"


def test_swap_blocked_when_material_incompatible():
    services = _two_placed(b_material="MDF", second_board="P2", second_index=1)
    project = services.projects.current_project
    assert swap_block_reason(project, "A", "B") == "status.swap_incompatible"


def test_swap_blocked_when_piece_overflows_destination():
    services = _two_placed(
        a_size=(800, 400),
        b_size=(100, 80),
        a_pos=(0, 0),
        b_pos=(900, 400),
    )
    project = services.projects.current_project
    assert swap_block_reason(project, "A", "B") == "status.swap_overflow"


def test_swap_blocked_when_new_rects_overlap_third_piece():
    services = _two_placed(
        a_size=(400, 200),
        b_size=(100, 80),
        a_pos=(0, 0),
        b_pos=(450, 0),
        extra=[StudioPiece("C", 80, 80, "Demo", 19)],
        extra_placements=[StudioPlacement("C", 500, 0, False, 0, "P1", 0, 0)],
    )
    project = services.projects.current_project
    assert swap_block_reason(project, "A", "B") == "status.swap_overlap"
