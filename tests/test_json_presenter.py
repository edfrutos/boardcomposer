import json

from boardcomposer import (
    AssemblySolution,
    Board,
    BoardPlacement,
    Offcut,
    PanelReference,
    Project,
    StockPanel,
)
from boardcomposer.presenters import solutions_to_json
from boardcomposer.solver import GeometrySolver
from boardcomposer.solver.strategies import compact_first_strategy


def test_solutions_to_json_contains_strategy_metadata():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))

    strategy = compact_first_strategy()
    solutions = GeometrySolver(project, strategy=strategy).solve()

    payload = json.loads(
        solutions_to_json(
            project=project,
            strategy=strategy,
            solutions=solutions,
            top=3,
        )
    )

    assert payload["strategy"] == "compact"
    assert payload["generators"] == ["vertical", "free_space"]
    assert "best_solution" in payload
    assert len(payload["solutions"]) <= 3


def test_solutions_to_json_contains_stock_panel_assignment():
    project = Project()
    project.add_stock_panel(StockPanel(100, 100, 19, "P1", quantity=2))
    project.add_board(Board(50, 50, 19, "A"))
    strategy = compact_first_strategy()
    solution = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                0,
                0,
                50,
                50,
                panel_reference=PanelReference(0, 1),
            )
        ]
    )

    payload = json.loads(solutions_to_json(project, strategy, [solution], top=1))

    assert payload["stock_panels"][0]["quantity"] == 2
    assert payload["solutions"][0]["placements"][0]["panel_reference"] == {
        "stock_panel_index": 0,
        "instance_index": 1,
    }


def test_solutions_to_json_reports_omitted_boards_for_a_partial_solution():
    project = Project()
    project.add_board(Board(50, 50, 19, "A"))
    project.add_board(Board(50, 50, 19, "B"))
    strategy = compact_first_strategy()
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 50, 50)],
        omitted_piece_ids=("B",),
    )

    payload = json.loads(solutions_to_json(project, strategy, [solution], top=1))

    assert payload["best_solution"]["omitted_boards"] == ["B"]
    assert payload["solutions"][0]["omitted_boards"] == ["B"]


def test_solutions_to_json_reports_offcuts():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 1000, 19, "P1"))
    project.add_board(Board(400, 400, 19, "A"))
    strategy = compact_first_strategy()
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 400, 400, panel_reference=PanelReference(0, 0))
        ],
        offcuts=(Offcut(PanelReference(0, 0), 400, 0, 600, 1000),),
    )

    payload = json.loads(solutions_to_json(project, strategy, [solution], top=1))

    assert payload["best_solution"]["offcuts_area_mm2"] == 600_000
    assert payload["solutions"][0]["offcuts"][0]["area_mm2"] == 600_000
