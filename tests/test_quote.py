"""Material quote PDF (IDE-0032)."""

from boardcomposer import Board, Project, ProjectConstraints, StockPanel
from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    PanelReference,
    SolutionExplanation,
    SolutionScore,
)
from boardcomposer.export import QuoteMeta, build_quote, quote_to_pdf
from boardcomposer.inventory.material_cost import estimated_material_cost


def _project_and_solution() -> tuple[Project, AssemblySolution]:
    project = Project(constraints=ProjectConstraints(allow_rotation=True))
    project.add_stock_panel(
        StockPanel(1000, 500, 19, "P1", quantity=2, material="Melamina")
    )
    project.add_stock_panel(StockPanel(800, 400, 19, "P2", quantity=1, material="MDF"))
    project.add_board(Board(400, 300, 19, "A", material="Melamina"))
    project.add_board(Board(200, 100, 19, "B", material="MDF"))
    solution = AssemblySolution(
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
        score=SolutionScore(),
        explanation=SolutionExplanation(),
        omitted_piece_ids=("B",),
    )
    return project, solution


def test_build_quote_matches_estimated_material_cost():
    project, solution = _project_and_solution()
    prices = {"melamina": 25}
    report = build_quote(
        solution,
        project,
        prices,
        QuoteMeta(project_name="Cocina", client="ACME", reference="PED-1"),
    )
    estimate = estimated_material_cost(solution, project, prices)

    assert report.meta.project_name == "Cocina"
    assert report.meta.client == "ACME"
    assert report.placed_count == 1
    assert report.omitted_ids == ("B",)
    assert len(report.lines) == 1
    line = report.lines[0]
    assert line.panel_id == "P1"
    assert line.instance_index == 0
    assert line.area_m2 == 0.5
    assert line.price_per_m2 == 25
    assert line.cost == 12.50
    assert report.estimate == estimate
    assert report.estimate.total == 12.50


def test_build_quote_marks_unpriced_panels():
    project, solution = _project_and_solution()
    extra = BoardPlacement(
        "B",
        0,
        0,
        200,
        100,
        panel_reference=PanelReference(1, 0),
    )
    solution = AssemblySolution(
        placements=list(solution.placements) + [extra],
        omitted_piece_ids=(),
    )
    report = build_quote(solution, project, {"melamina": 25})
    assert [item.material for item in report.lines] == ["Melamina", "MDF"]
    assert report.lines[0].priced
    assert not report.lines[1].priced
    assert report.estimate.missing_materials == ("MDF",)
    assert report.estimate.unpriced_area_m2 == 0.32


def test_build_quote_without_project_has_no_lines():
    _project, solution = _project_and_solution()
    report = build_quote(solution, None, {"melamina": 25})
    assert report.lines == ()
    assert report.placed_count == 1
    assert not report.estimate.has_price


def test_quote_to_pdf_is_pdf_and_lists_cost():
    project, solution = _project_and_solution()
    payload = quote_to_pdf(
        build_quote(
            solution,
            project,
            {"Melamina": 25},
            QuoteMeta(project_name="Cocina", client="ACME"),
        )
    )
    assert payload.startswith(b"%PDF-1.4")
    assert b"Presupuesto de material" in payload
    assert b"Cocina" in payload
    assert b"ACME" in payload
    assert b"12.50 EUR" in payload
    assert b"Melamina" in payload
    assert b"P1#1" in payload
    assert b"mano de obra" in payload
    assert b"Piezas omitidas: B" in payload
