from boardcomposer import (
    AssemblySolution,
    BoardPlacement,
    PanelReference,
    Project,
    StockPanel,
)
from boardcomposer.solver.objectives import (
    compactness,
    material_utilization,
    placed_board_ratio,
    rotation_ratio,
)


def test_material_utilization():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 0, 50, 100, 50),
        ]
    )

    assert material_utilization(solution) == 1.0


def test_material_utilization_uses_consumed_stock_panel_area():
    project = Project()
    project.add_stock_panel(StockPanel(100, 100, 19, "P1", quantity=2))
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50, panel_reference=PanelReference(0, 0)),
            BoardPlacement("B", 0, 0, 50, 50, panel_reference=PanelReference(0, 1)),
        ]
    )

    assert material_utilization(solution, project) == 0.375


def test_compactness():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    assert compactness(solution) == 0.5


def test_compactness_is_calculated_per_physical_panel():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 10, panel_reference=PanelReference(0, 0)),
            BoardPlacement("B", 0, 0, 10, 100, panel_reference=PanelReference(0, 1)),
        ]
    )

    assert compactness(solution) == 0.1


def test_rotation_ratio():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50, rotated=True),
            BoardPlacement("B", 0, 50, 100, 50, rotated=False),
        ]
    )

    assert rotation_ratio(solution) == 0.5


def test_placed_board_ratio():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    assert placed_board_ratio(solution, total_boards=2) == 0.5
