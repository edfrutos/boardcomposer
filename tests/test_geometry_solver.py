from boardcomposer import Board, Project
from boardcomposer.solver import GeometrySolver


def test_geometry_solver_returns_solution():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))

    solutions = GeometrySolver(project).solve()

    assert len(solutions) == 1
    assert len(solutions[0].placements) == 1
