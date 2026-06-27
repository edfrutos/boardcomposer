from boardcomposer import Board, Project
from boardcomposer.solver import GeometrySolver


def test_geometry_solver_returns_three_solutions():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solutions = GeometrySolver(project).solve()

    assert len(solutions) == 3


def test_geometry_solver_includes_horizontal_permutations():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solutions = GeometrySolver(project).solve()
    layouts = [solution.explanation.notes for solution in solutions]

    assert ["horizontal_permutation"] in layouts


def test_geometry_solver_includes_vertical_solution():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solutions = GeometrySolver(project).solve()
    layouts = [solution.explanation.notes for solution in solutions]

    assert ["vertical"] in layouts


def test_geometry_solver_sorts_solutions_by_score():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solutions = GeometrySolver(project).solve()

    assert solutions[0].score.total >= solutions[1].score.total


def test_geometry_solver_respects_constraints():
    from boardcomposer import ProjectConstraints

    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=2500,
            max_width_mm=600,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solutions = GeometrySolver(project).solve()

    assert len(solutions) == 1
    assert solutions[0].explanation.notes == ["vertical"]
