from boardcomposer import Board, Project, ProjectConstraints, StockPanel
from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    Offcut,
    PanelReference,
    SolutionExplanation,
)
from boardcomposer.export import solution_to_dxf, solution_to_pdf


def _single_panel_solution() -> tuple[Project, AssemblySolution]:
    project = Project(
        constraints=ProjectConstraints(allow_rotation=True),
    )
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1", quantity=1))
    project.add_board(Board(400, 300, 19, "A"))

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
        explanation=SolutionExplanation(notes=["test"]),
        offcuts=(Offcut(PanelReference(0, 0), 400, 0, 600, 300),),
    )
    return project, solution


def test_solution_to_dxf_draws_panels_pieces_and_offcuts():
    project, solution = _single_panel_solution()

    dxf = solution_to_dxf(solution, project)

    assert dxf.startswith("0\nSECTION")
    assert "LWPOLYLINE" in dxf
    assert "PANELS" in dxf
    assert "PIECES" in dxf
    assert "OFFCUTS" in dxf
    assert "SEQ" in dxf
    assert "A 400x300" in dxf
    assert "600x300" in dxf
    assert "DIMS" in dxf
    assert "TABLES" in dxf
    assert "LAYER" in dxf
    assert "$INSUNITS" in dxf
    assert "LABELS" not in dxf
    assert dxf.rstrip().endswith("EOF")


def test_solution_to_dxf_works_without_a_project():
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
        explanation=SolutionExplanation(),
    )

    dxf = solution_to_dxf(solution)

    assert "PIECES" in dxf
    assert "A 100x50" in dxf


def test_solution_to_pdf_returns_a_valid_pdf_header():
    project, solution = _single_panel_solution()

    pdf = solution_to_pdf(solution, project)

    assert pdf.startswith(b"%PDF-1.4")
    assert b"%%EOF" in pdf
    assert b"/Type /Page" in pdf
    assert b"Helvetica" in pdf
    assert b"A 400x300" in pdf
    assert b"600x300" in pdf
    assert b"[8 4] 0 d" in pdf
    assert b"(1000)" in pdf
    assert b"(500)" in pdf


def test_solution_to_pdf_works_without_a_project():
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
        explanation=SolutionExplanation(),
    )

    pdf = solution_to_pdf(solution)

    assert pdf.startswith(b"%PDF-1.4")
    assert b"A 100x50" in pdf


def test_solution_to_dxf_can_omit_piece_labels():
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
        explanation=SolutionExplanation(),
    )

    dxf = solution_to_dxf(solution, include_piece_labels=False)

    assert "PIECES" in dxf
    assert "SEQ" in dxf
    assert "A 100x50" not in dxf


def test_solution_to_pdf_can_omit_piece_labels():
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
        explanation=SolutionExplanation(),
    )

    pdf = solution_to_pdf(solution, include_piece_labels=False)

    assert pdf.startswith(b"%PDF-1.4")
    assert b"A 100x50" not in pdf


def test_solution_to_dxf_can_omit_offcut_labels():
    project, solution = _single_panel_solution()

    dxf = solution_to_dxf(solution, project, include_offcut_labels=False)

    assert "OFFCUTS" in dxf
    assert "600x300" not in dxf
    assert "A 400x300" in dxf


def test_solution_to_pdf_can_omit_offcut_labels():
    project, solution = _single_panel_solution()

    pdf = solution_to_pdf(solution, project, include_offcut_labels=False)

    assert pdf.startswith(b"%PDF-1.4")
    assert b"[8 4] 0 d" in pdf
    assert b"600x300" not in pdf
    assert b"A 400x300" in pdf


def test_solution_to_dxf_declares_role_layers_in_table():
    project, solution = _single_panel_solution()

    dxf = solution_to_dxf(solution, project)
    tables, _sep, entities = dxf.partition("ENTITIES")

    assert "2\nLAYER" in tables
    for layer in ("PANELS", "PIECES", "OFFCUTS", "DIMS", "SEQ", "META"):
        assert f"2\n{layer}\n" in tables
        assert f"8\n{layer}\n" in entities


def test_solution_to_dxf_omits_unused_role_layers_from_table():
    project, solution = _single_panel_solution()

    dxf = solution_to_dxf(
        solution,
        project,
        include_panel_dimensions=False,
        include_plan_traceability=False,
    )
    tables, _sep, _entities = dxf.partition("ENTITIES")

    assert "2\nPANELS\n" in tables
    assert "2\nPIECES\n" in tables
    assert "2\nOFFCUTS\n" in tables
    assert "2\nDIMS\n" not in tables
    assert "2\nMETA\n" not in tables


def test_solution_to_dxf_can_omit_panel_dimensions():
    project, solution = _single_panel_solution()

    dxf = solution_to_dxf(solution, project, include_panel_dimensions=False)

    assert "PANELS" in dxf
    assert "DIMS" not in dxf
    assert "A 400x300" in dxf


def test_solution_to_pdf_can_omit_panel_dimensions():
    project, solution = _single_panel_solution()

    pdf = solution_to_pdf(solution, project, include_panel_dimensions=False)

    assert pdf.startswith(b"%PDF-1.4")
    assert b"(1000)" not in pdf
    assert b"(500)" not in pdf
    assert b"A 400x300" in pdf


def test_solution_to_dxf_includes_injected_plan_traceability():
    project, solution = _single_panel_solution()

    dxf = solution_to_dxf(
        solution,
        project,
        strategy_name="material",
        exported_at="2026-09-19 12:00",
        app_version="9.9.9",
    )

    assert "META" in dxf
    assert "BoardComposer 9.9.9 · material · 2026-09-19 12:00" in dxf


def test_solution_to_dxf_omits_plan_traceability_when_disabled():
    project, solution = _single_panel_solution()

    dxf = solution_to_dxf(solution, project, include_plan_traceability=False)

    assert "BoardComposer" not in dxf
    assert "META" not in dxf


def test_solution_to_pdf_includes_injected_plan_traceability():
    project, solution = _single_panel_solution()

    pdf = solution_to_pdf(
        solution,
        project,
        strategy_name="material",
        exported_at="2026-09-19 12:00",
        app_version="9.9.9",
    )

    assert pdf.startswith(b"%PDF-1.4")
    assert b"BoardComposer 9.9.9" in pdf
    assert b"material" in pdf
    assert b"2026-09-19 12:00" in pdf


def test_solution_to_pdf_omits_plan_traceability_when_disabled():
    project, solution = _single_panel_solution()

    pdf = solution_to_pdf(solution, project, include_plan_traceability=False)

    assert pdf.startswith(b"%PDF-1.4")
    assert b"BoardComposer" not in pdf


def test_solution_to_dxf_plan_labels_follow_units():
    project, solution = _single_panel_solution()

    dxf = solution_to_dxf(solution, project, units="cm")

    assert "A 40x30 cm" in dxf
    assert "60x30 cm" in dxf
    assert "100 cm" in dxf
    assert "A 400x300" not in dxf
    assert "$INSUNITS" in dxf
    assert "432" in dxf


def test_solution_to_pdf_plan_labels_follow_units():
    project, solution = _single_panel_solution()

    pdf = solution_to_pdf(solution, project, units="cm")

    assert pdf.startswith(b"%PDF-1.4")
    assert b"A 40x30 cm" in pdf
    assert b"60x30 cm" in pdf
    assert b"A 400x300" not in pdf
