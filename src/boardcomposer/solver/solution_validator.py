"""Validation rules for generated layout solutions."""

from boardcomposer.domain import AssemblySolution, ProjectConstraints
from boardcomposer.layout.validation import has_overlaps
from boardcomposer.solver.constraints_validator import respects_constraints


def is_valid_solution(
    solution: AssemblySolution,
    constraints: ProjectConstraints,
) -> bool:
    """Return whether a generated solution satisfies all core rules."""
    return respects_constraints(solution, constraints) and not has_overlaps(
        solution.placements
    )
