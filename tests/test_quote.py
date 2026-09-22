"""Material quote PDF (IDE-0032)."""

from boardcomposer import Board, Project, ProjectConstraints, StockPanel
from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    PanelReference,
    SolutionExplanation,
    SolutionScore,
)
from boardcomposer.export import (
    QuoteMeta,
    build_quote,
    normalize_labor_minutes,
    normalize_labor_rate,
    quote_to_pdf,
)
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


def test_normalize_labor_clamps_and_falls_back():
    assert normalize_labor_rate("30") == 30.0
    assert normalize_labor_rate(-5) == 0.0
    assert normalize_labor_rate(2000) == 999.0
    assert normalize_labor_rate("x") == 0.0
    assert normalize_labor_minutes(15) == 15.0
    assert normalize_labor_minutes(-1) == 0.0
    assert normalize_labor_minutes(300) == 180.0


def test_build_quote_adds_labor_from_meta():
    project, solution = _project_and_solution()
    report = build_quote(
        solution,
        project,
        {"melamina": 25},
        QuoteMeta(labor_rate_eur_per_hour=30, labor_minutes_per_piece=15),
    )
    assert report.labor_hours == 0.25
    assert report.labor_cost == 7.50
    assert report.has_labor
    assert report.grand_total == 20.00


def test_build_quote_omits_labor_when_rate_or_minutes_are_zero():
    project, solution = _project_and_solution()
    report = build_quote(
        solution,
        project,
        {"melamina": 25},
        QuoteMeta(labor_rate_eur_per_hour=30, labor_minutes_per_piece=0),
    )
    assert report.labor_cost == 0
    assert not report.has_labor
    assert report.grand_total == 12.50


def test_quote_to_pdf_lists_labor_and_grand_total():
    project, solution = _project_and_solution()
    payload = quote_to_pdf(
        build_quote(
            solution,
            project,
            {"Melamina": 25},
            QuoteMeta(
                project_name="Cocina",
                labor_rate_eur_per_hour=30,
                labor_minutes_per_piece=15,
            ),
        )
    )
    assert payload.startswith(b"%PDF-1.4")
    assert b"12.50 EUR" in payload
    assert b"7.50 EUR" in payload
    assert b"20.00 EUR" in payload
    assert b"Mano de obra" in payload
    assert b"30.00 EUR/h" in payload
    assert b"herrajes" in payload


def test_quote_pdf_uses_prefs_units_area_stays_m2():
    project, solution = _project_and_solution()
    mm_text = quote_to_pdf(
        build_quote(
            solution,
            project,
            {"Melamina": 25},
            QuoteMeta(project_name="Cocina"),
        )
    ).decode("latin-1", errors="replace")
    assert "1000x500" in mm_text
    assert " 19 " in mm_text
    assert "0.500" in mm_text

    cm_text = quote_to_pdf(
        build_quote(
            solution,
            project,
            {"Melamina": 25},
            QuoteMeta(project_name="Cocina", units="cm"),
        )
    ).decode("latin-1", errors="replace")
    assert "100x50 cm" in cm_text
    assert "1.9 cm" in cm_text
    assert "0.500" in cm_text
    assert "1000x500" not in cm_text


def test_quote_pdf_includes_or_omits_traceability():
    project, solution = _project_and_solution()
    stamped = QuoteMeta(
        project_name="Cocina",
        strategy_name="skyline",
        version="9.9.9",
        exported_at="2026-09-21 12:00",
    )
    payload = quote_to_pdf(build_quote(solution, project, {"Melamina": 25}, stamped))
    text = payload.decode("latin-1", errors="replace")
    assert "BoardComposer 9.9.9" in text
    assert "skyline" in text
    assert "2026-09-21 12:00" in text

    omitted = quote_to_pdf(
        build_quote(
            solution,
            project,
            {"Melamina": 25},
            QuoteMeta(project_name="Cocina", include_traceability=False),
        )
    )
    assert b"9.9.9" not in omitted
