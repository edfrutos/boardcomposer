from boardcomposer import (
    AssemblySolution,
    Board,
    BoardPlacement,
    Offcut,
    PanelReference,
    Project,
)
from boardcomposer.presenters import solution_to_text
from boardcomposer.solver import GeometrySolver


def test_solution_to_text_contains_summary():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))

    solutions = GeometrySolver(project).solve()
    output = solution_to_text(project, solutions)

    assert "BoardComposer" in output
    assert "Tablas entrada: 1" in output
    assert "Puntuación:" in output


def test_solution_to_text_reports_omitted_pieces_for_a_partial_solution():
    project = Project()
    project.add_board(Board(100, 50, 19, "A"))
    project.add_board(Board(100, 50, 19, "B"))
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
        omitted_piece_ids=("B",),
    )

    output = solution_to_text(project, [solution])

    assert "Piezas sin colocar: B" in output


def test_solution_to_text_reports_offcuts():
    project = Project()
    project.add_board(Board(400, 400, 19, "P"))
    solution = AssemblySolution(
        placements=[BoardPlacement("P", 0, 0, 400, 400)],
        offcuts=(Offcut(PanelReference(0, 0), 400, 0, 600, 1000),),
    )

    output = solution_to_text(project, [solution])

    assert "Retales aprovechables: 1 (área total 600000 mm²)" in output
