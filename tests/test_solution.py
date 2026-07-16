from boardcomposer import (
    AssemblySolution,
    BoardPlacement,
    Offcut,
    PanelReference,
    Project,
    SolutionScore,
    StockPanel,
)


def test_solution_dimensions_and_area():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 2000, 300),
            BoardPlacement("B", 2000, 0, 1000, 300),
        ],
        score=SolutionScore(waste_score=30),
    )

    assert solution.total_length_mm == 3000
    assert solution.total_width_mm == 300
    assert solution.used_area_mm2 == 900000
    assert solution.bounding_area_mm2 == 900000
    assert solution.waste_area_mm2 == 0
    assert solution.waste_ratio == 0


def test_solution_with_empty_placements():
    solution = AssemblySolution(placements=[])

    assert solution.total_length_mm == 0
    assert solution.total_width_mm == 0
    assert solution.used_area_mm2 == 0
    assert solution.bounding_area_mm2 == 0
    assert solution.waste_ratio == 0


def test_solution_reports_waste_for_each_used_physical_panel():
    project = Project()
    project.add_stock_panel(StockPanel(100, 100, 19, "P1", quantity=2))
    first = PanelReference(0, 0)
    second = PanelReference(0, 1)
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50, panel_reference=first),
            BoardPlacement("B", 0, 0, 50, 50, panel_reference=second),
        ]
    )

    assert solution.panel_references == (first, second)
    assert solution.panel_waste_area_mm2(project, first) == 5_000
    assert solution.panel_waste_area_mm2(project, second) == 7_500
    assert solution.total_panel_waste_area_mm2(project) == 12_500
    assert solution.panel_waste_ratio(project) == 0.625
    assert solution.bounding_area_mm2 == 7_500
    assert solution.waste_ratio == 0


def test_solution_without_offcuts_reports_zero_total_area():
    solution = AssemblySolution(placements=[])

    assert solution.offcuts == ()
    assert solution.total_offcut_area_mm2 == 0
    assert solution.is_complete is True


def test_solution_sums_the_area_of_every_offcut():
    solution = AssemblySolution(
        placements=[],
        offcuts=(
            Offcut(PanelReference(0, 0), 0, 0, 100, 100),
            Offcut(PanelReference(0, 0), 100, 0, 50, 100),
        ),
    )

    assert solution.total_offcut_area_mm2 == 15_000


def test_solution_with_omitted_pieces_is_not_complete():
    solution = AssemblySolution(placements=[], omitted_piece_ids=("A",))

    assert solution.is_complete is False
