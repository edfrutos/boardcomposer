"""Validation rules for generated layout solutions."""

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.layout.validation import has_overlaps
from boardcomposer.solver.constraints_validator import respects_constraints


def is_valid_solution(
    solution: AssemblySolution,
    project: Project,
) -> bool:
    """Return whether a generated solution satisfies all core rules."""
    expected_ids = [board.id for board in project.boards]
    placed_ids = [placement.board_id for placement in solution.placements]

    if len(placed_ids) != len(expected_ids):
        return False

    if len(set(placed_ids)) != len(placed_ids):
        return False

    if set(placed_ids) != set(expected_ids):
        return False

    return respects_constraints(solution, project.constraints) and not has_overlaps(
        solution.placements
    )
