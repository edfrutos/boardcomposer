"""Tests for structured solution validation."""

from boardcomposer import (
    AssemblySolution,
    Board,
    BoardPlacement,
    Project,
    ProjectConstraints,
)
from boardcomposer.solver.solution_validator import validate_solution
from boardcomposer.solver.validation_result import ValidationReason


def make_project() -> Project:
    """Create a constrained project containing two boards."""
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=200,
            max_width_mm=100,
        )
    )
    project.add_board(Board(100, 50, 19, "A"))
    project.add_board(Board(100, 50, 19, "B"))
    return project


def test_valid_solution_has_no_reasons():
    """A valid solution returns an empty reason collection."""
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 100, 0, 100, 50),
        ]
    )

    result = validate_solution(solution, make_project())

    assert result.valid is True
    assert result.reasons == ()


def test_missing_board_is_reported():
    """A missing board is identified."""
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    result = validate_solution(solution, make_project())

    assert result.valid is False
    assert ValidationReason.MISSING_BOARD in result.reasons


def test_duplicate_board_is_reported():
    """A duplicated board identifier is identified."""
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("A", 100, 0, 100, 50),
        ]
    )

    result = validate_solution(solution, make_project())

    assert ValidationReason.DUPLICATE_BOARD in result.reasons
    assert ValidationReason.MISSING_BOARD in result.reasons


def test_unknown_board_is_reported():
    """An unknown board identifier is identified."""
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("X", 100, 0, 100, 50),
        ]
    )

    result = validate_solution(solution, make_project())

    assert ValidationReason.UNKNOWN_BOARD in result.reasons
    assert ValidationReason.MISSING_BOARD in result.reasons


def test_multiple_validation_reasons_are_reported():
    """All detected validation problems are returned together."""
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 150, 100),
            BoardPlacement("A", 100, 0, 150, 100),
        ]
    )

    result = validate_solution(solution, make_project())

    assert ValidationReason.DUPLICATE_BOARD in result.reasons
    assert ValidationReason.MISSING_BOARD in result.reasons
    assert ValidationReason.EXCEEDS_CONSTRAINTS in result.reasons
    assert ValidationReason.OVERLAP in result.reasons
