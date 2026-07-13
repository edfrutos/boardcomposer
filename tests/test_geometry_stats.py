"""Tests for statistics exposed by GeometrySolver."""

from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.geometry_solver import GeometrySolver


def test_geometry_solver_exposes_pipeline_statistics():
    """The solver exposes statistics after solving a project."""
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=200,
            max_width_mm=100,
        )
    )
    project.add_board(Board(100, 50, 19, "A"))
    project.add_board(Board(100, 50, 19, "B"))

    solver = GeometrySolver(project)

    solutions = solver.solve()

    assert solver.stats.generated >= 1
    assert solver.stats.unique >= 1
    assert solver.stats.accepted == len(solutions)
    assert solver.stats.rejected == (solver.stats.unique - solver.stats.accepted)
