"""Tests for validating and evaluating layout solutions."""

from boardcomposer import (
    AssemblySolution,
    Board,
    BoardPlacement,
    Project,
    ProjectConstraints,
)
from boardcomposer.solver.solution_evaluator import SolutionEvaluator
from boardcomposer.solver.validation_result import ValidationReason


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

    assert result.accepted is True
    assert result.solution is not None
    assert result.solution.score.total > 0
    assert result.validation.valid is True
    assert result.validation.reasons == ()


def test_evaluator_rejects_overlapping_solution():
    """An overlapping solution is rejected."""
    candidate = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 50, 0, 100, 50),
        ]
    )

    result = SolutionEvaluator(make_project()).evaluate(candidate)

    assert result.accepted is False
    assert result.solution is None
    assert ValidationReason.OVERLAP in result.validation.reasons


def test_evaluator_accepts_incomplete_solution_as_partial():
    """An incomplete solution is accepted and scored as a partial one,
    with the missing piece recorded on the solution itself."""
    candidate = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
        ]
    )

    result = SolutionEvaluator(make_project()).evaluate(candidate)

    assert result.accepted is True
    assert result.solution is not None
    assert result.solution.omitted_piece_ids == ("B",)
    assert result.solution.is_complete is False
    assert result.validation.valid is True
    assert result.validation.complete is False
    assert ValidationReason.MISSING_BOARD in result.validation.reasons
