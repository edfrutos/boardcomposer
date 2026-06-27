from boardcomposer import Board, Project
from boardcomposer.solver import GeometrySolver


def test_geometry_solver_returns_two_solutions():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solutions = GeometrySolver(project).solve()

    assert len(solutions) == 2


def test_geometry_solver_horizontal_solution():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solution = GeometrySolver(project).solve()[0]

    assert solution.explanation.notes == ["horizontal"]
    assert solution.total_length_mm == 3000
    assert solution.total_width_mm == 300


def test_geometry_solver_vertical_solution():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solution = GeometrySolver(project).solve()[1]

    assert solution.explanation.notes == ["vertical"]
    assert solution.total_length_mm == 2000
    assert solution.total_width_mm == 600
