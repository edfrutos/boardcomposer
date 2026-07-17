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
    assert "A" in dxf
    assert dxf.rstrip().endswith("EOF")


def test_solution_to_dxf_works_without_a_project():
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
        explanation=SolutionExplanation(),
    )

    dxf = solution_to_dxf(solution)

    assert "PIECES" in dxf
    assert "A" in dxf


def test_solution_to_pdf_returns_a_valid_pdf_header():
    project, solution = _single_panel_solution()

    pdf = solution_to_pdf(solution, project)

    assert pdf.startswith(b"%PDF-1.4")
    assert b"%%EOF" in pdf
    assert b"/Type /Page" in pdf
    assert b"Helvetica" in pdf
    assert b"A" in pdf


def test_solution_to_pdf_works_without_a_project():
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
        explanation=SolutionExplanation(),
    )

    pdf = solution_to_pdf(solution)

    assert pdf.startswith(b"%PDF-1.4")
    assert b"A" in pdf
