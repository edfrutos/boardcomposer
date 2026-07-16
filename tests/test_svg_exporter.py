from boardcomposer import (
    AssemblySolution,
    BoardPlacement,
    Offcut,
    PanelReference,
    Project,
    StockPanel,
)
from boardcomposer.export import solution_to_svg


def test_solution_to_svg():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    svg = solution_to_svg(solution)

    assert svg.startswith("<svg")
    assert "<rect" in svg
    assert "A" in svg


def test_solution_to_svg_places_physical_panels_side_by_side():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1", quantity=2))
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 900, 400, panel_reference=PanelReference(0, 0)),
            BoardPlacement("B", 0, 0, 900, 400, panel_reference=PanelReference(0, 1)),
        ]
    )

    svg = solution_to_svg(solution, project)

    assert 'width="2050"' in svg
    assert '<rect x="1050" y="30" width="900" height="400"' in svg


def test_solution_to_svg_does_not_overlap_panel_and_piece_labels():
    """Regression: panel and piece labels used to be drawn at the same
    y coordinate, right on top of each other."""
    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1"))
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 900, 400, panel_reference=PanelReference(0, 0)),
        ]
    )

    svg = solution_to_svg(solution, project)

    panel_label_y = svg.index("P1")
    piece_label_y = svg.index(">A<")
    assert panel_label_y < piece_label_y


def test_solution_to_svg_lists_omitted_pieces_for_a_partial_solution():
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
        omitted_piece_ids=("B",),
    )

    svg = solution_to_svg(solution)

    assert "Piezas omitidas" in svg
    assert "B" in svg


def test_solution_to_svg_omits_legend_when_solution_is_complete():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    svg = solution_to_svg(solution)

    assert "Piezas omitidas" not in svg


def test_solution_to_svg_draws_offcuts_dashed_and_offset_by_panel():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 1000, 19, "P1"))
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 400, 400, panel_reference=PanelReference(0, 0)),
        ],
        offcuts=(Offcut(PanelReference(0, 0), 400, 0, 600, 1000),),
    )

    svg = solution_to_svg(solution, project)

    assert "stroke-dasharray" in svg
    assert "600000 mm" in svg


def test_solution_to_svg_has_no_offcuts_when_solution_reports_none():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    svg = solution_to_svg(solution)

    assert "stroke-dasharray" not in svg
