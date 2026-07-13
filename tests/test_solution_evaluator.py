"""Tests for validating and evaluating layout solutions."""

from boardcomposer import (
    AssemblySolution,
    Board,
    BoardPlacement,
    Project,
    ProjectConstraints,
)
from boardcomposer.solver.solution_evaluator import SolutionEvaluator


def make_project() -> Project:
    """Create a two-piece constrained project."""
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=200,
            max_width_mm=100,
        )
    )
    project.add_board(Board(100, 50, 19, "A"))
    project.add_board(Board(100, 50, 19, "B"))
    return project


def test_evaluator_returns_scored_valid_solution():
    """A valid complete solution is scored."""
    candidate = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 100, 0, 100, 50),
        ]
    )

    result = SolutionEvaluator(make_project()).evaluate(candidate)

    assert result is not None
    assert result.score.total > 0


def test_evaluator_rejects_overlapping_solution():
    """An overlapping solution is rejected."""
    candidate = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 50, 0, 100, 50),
        ]
    )

    result = SolutionEvaluator(make_project()).evaluate(candidate)

    assert result is None


def test_evaluator_rejects_incomplete_solution():
    """An incomplete solution is rejected."""
    candidate = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
        ]
    )

    result = SolutionEvaluator(make_project()).evaluate(candidate)

    assert result is None
