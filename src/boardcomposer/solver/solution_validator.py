"""Validation rules for generated layout solutions."""

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.layout.validation import has_overlaps
from boardcomposer.solver.constraints_validator import respects_constraints
from boardcomposer.solver.validation_result import (
    ValidationReason,
    ValidationResult,
)


def validate_solution(
    solution: AssemblySolution,
    project: Project,
) -> ValidationResult:
    """Validate a generated solution and report every detected problem."""
    expected_ids = [board.id for board in project.boards]
    placed_ids = [placement.board_id for placement in solution.placements]

    expected_set = set(expected_ids)
    placed_set = set(placed_ids)

    reasons: list[ValidationReason] = []

    if len(placed_ids) != len(placed_set):
        reasons.append(ValidationReason.DUPLICATE_BOARD)

    if expected_set - placed_set:
        reasons.append(ValidationReason.MISSING_BOARD)

    if placed_set - expected_set:
        reasons.append(ValidationReason.UNKNOWN_BOARD)

    if not respects_constraints(solution, project.constraints):
        reasons.append(ValidationReason.EXCEEDS_CONSTRAINTS)

    if has_overlaps(solution.placements):
        reasons.append(ValidationReason.OVERLAP)

    return ValidationResult(
        valid=not reasons,
        reasons=tuple(reasons),
    )


def is_valid_solution(
    solution: AssemblySolution,
    project: Project,
) -> bool:
    """Return whether a generated solution satisfies all core rules."""
    return validate_solution(solution, project).valid
