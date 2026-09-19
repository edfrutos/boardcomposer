from boardcomposer import (
    AssemblySolution,
    BoardPlacement,
    Offcut,
    PanelReference,
    Project,
    StockPanel,
)
from boardcomposer.export import solution_to_svg


def test_solution_to_svg_uses_industrial_palette():
    from boardcomposer.export import DEFAULT_SVG_PALETTE

    svg = solution_to_svg(
        AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])
    )

    assert DEFAULT_SVG_PALETTE.piece_fill in svg
    assert DEFAULT_SVG_PALETTE.piece_stroke in svg
    assert DEFAULT_SVG_PALETTE.background in svg
    assert "#64748b" not in svg
    assert 'stroke="black"' not in svg


def test_solution_to_svg():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    svg = solution_to_svg(solution)

    assert svg.startswith("<svg")
    assert "<rect" in svg
    assert "A 100x50" in svg


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

    assert 'width="2082"' in svg
    assert '<rect x="1082" y="30" width="900" height="400"' in svg
    assert 'text-anchor="middle"' in svg
    assert ">1000</text>" in svg
    assert ">500</text>" in svg


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
    piece_label_y = svg.index(">A 900x400<")
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
    assert "600x1000" in svg
    assert "600000 mm" not in svg


def test_solution_to_svg_has_no_offcuts_when_solution_reports_none():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    svg = solution_to_svg(solution)

    assert "stroke-dasharray" not in svg


def test_solution_to_svg_omits_piece_labels_when_disabled():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    svg = solution_to_svg(solution, include_piece_labels=False)

    assert "<rect" in svg
    assert "A 100x50" not in svg
    assert ">A<" not in svg
    assert 'data-cut-seq="1"' in svg


def test_solution_to_svg_omits_offcut_labels_when_disabled():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 1000, 19, "P1"))
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 400, 400, panel_reference=PanelReference(0, 0)),
        ],
        offcuts=(Offcut(PanelReference(0, 0), 400, 0, 600, 1000),),
    )

    svg = solution_to_svg(solution, project, include_offcut_labels=False)

    assert "stroke-dasharray" in svg
    assert "600x1000" not in svg


def test_solution_to_svg_omits_panel_dimensions_when_disabled():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1", quantity=2))
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 900, 400, panel_reference=PanelReference(0, 0)),
            BoardPlacement("B", 0, 0, 900, 400, panel_reference=PanelReference(0, 1)),
        ]
    )

    svg = solution_to_svg(solution, project, include_panel_dimensions=False)

    assert 'width="2050"' in svg
    assert '<rect x="1050" y="30" width="900" height="400"' in svg
    assert 'text-anchor="middle"' not in svg
    assert ">1000</text>" not in svg
    assert ">500</text>" not in svg


def test_solution_to_svg_includes_injected_plan_traceability():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    svg = solution_to_svg(
        solution,
        strategy_name="material",
        exported_at="2026-09-19 12:00",
        app_version="9.9.9",
    )

    assert "BoardComposer 9.9.9 · material · 2026-09-19 12:00" in svg
    assert 'width="100"' in svg


def test_solution_to_svg_omits_plan_traceability_when_disabled():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    svg = solution_to_svg(solution, include_plan_traceability=False)

    assert "BoardComposer" not in svg
