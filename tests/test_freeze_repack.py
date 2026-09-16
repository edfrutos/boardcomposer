"""Freeze OK placements and re-pack omitted pieces (IDE-0030)."""

from boardcomposer import Board, Project, ProjectConstraints, StockPanel
from boardcomposer.domain import AssemblySolution, BoardPlacement, PanelReference
from boardcomposer.solver.freeze_repack import freeze_and_repack_omitted


def test_repack_fills_leftover_on_same_panel_without_moving_frozen():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1"))
    project.add_board(Board(400, 300, 19, "A"))
    project.add_board(Board(200, 100, 19, "B"))
    frozen = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                0,
                0,
                400,
                300,
                panel_reference=PanelReference(0, 0),
            )
        ],
        omitted_piece_ids=("B",),
    )

    result = freeze_and_repack_omitted(project, frozen)

    frozen_a = next(item for item in result.placements if item.board_id == "A")
    assert frozen_a.x_mm == 0
    assert frozen_a.y_mm == 0
    assert frozen_a.length_mm == 400
    assert any(item.board_id == "B" for item in result.placements)
    assert result.omitted_piece_ids == ()
    assert "freeze_repack" in result.explanation.notes


def test_repack_uses_unused_stock_instance_when_leftover_is_too_small():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1", quantity=2))
    project.add_board(Board(900, 400, 19, "A"))
    project.add_board(Board(800, 400, 19, "B"))
    frozen = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                0,
                0,
                900,
                400,
                panel_reference=PanelReference(0, 0),
            )
        ],
        omitted_piece_ids=("B",),
    )

    result = freeze_and_repack_omitted(project, frozen)

    placed_b = next(item for item in result.placements if item.board_id == "B")
    assert placed_b.panel_reference == PanelReference(0, 1)
    frozen_a = next(item for item in result.placements if item.board_id == "A")
    assert frozen_a.panel_reference == PanelReference(0, 0)
    assert result.omitted_piece_ids == ()


def test_repack_without_omitted_returns_same_placements():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1"))
    project.add_board(Board(400, 300, 19, "A"))
    frozen = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                10,
                20,
                400,
                300,
                panel_reference=PanelReference(0, 0),
            )
        ]
    )

    result = freeze_and_repack_omitted(project, frozen)

    assert result is frozen


def test_repack_keeps_omitted_when_nothing_fits():
    project = Project()
    project.add_stock_panel(StockPanel(500, 400, 19, "P1"))
    project.add_board(Board(500, 400, 19, "A"))
    project.add_board(Board(500, 400, 19, "B"))
    frozen = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                0,
                0,
                500,
                400,
                panel_reference=PanelReference(0, 0),
            )
        ],
        omitted_piece_ids=("B",),
    )

    result = freeze_and_repack_omitted(project, frozen)

    assert [item.board_id for item in result.placements] == ["A"]
    assert result.omitted_piece_ids == ("B",)


def test_repack_respects_kerf_gap_around_frozen_piece():
    project = Project(constraints=ProjectConstraints(kerf_mm=10))
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1"))
    project.add_board(Board(400, 300, 19, "A"))
    project.add_board(Board(200, 100, 19, "B"))
    frozen = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                0,
                0,
                400,
                300,
                panel_reference=PanelReference(0, 0),
            )
        ],
        omitted_piece_ids=("B",),
    )

    result = freeze_and_repack_omitted(project, frozen)

    placed_b = next(item for item in result.placements if item.board_id == "B")
    assert placed_b.x_mm >= 410 or placed_b.y_mm >= 310
    assert placed_b.length_mm == 200
    assert placed_b.width_mm == 100
