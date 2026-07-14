"""Stable ranking criteria for evaluated solutions."""

from boardcomposer.domain import AssemblySolution
from boardcomposer.solver.objectives import compactness, rotation_ratio


def solution_ranking_key(
    solution: AssemblySolution,
) -> tuple[float, float, float, float, float, float, float]:
    """Return a key where greater values represent better solutions."""
    return (
        solution.score.total,
        -solution.waste_ratio,
        -solution.bounding_area_mm2,
        -rotation_ratio(solution),
        compactness(solution),
        -solution.total_length_mm,
        -solution.total_width_mm,
    )
