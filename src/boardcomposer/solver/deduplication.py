"""Deduplicate geometrically equivalent layout solutions."""

from boardcomposer.domain import AssemblySolution

_POSITION_TOLERANCE_MM = 1.0


def _quantize(value: float) -> int:
    """Convert a numeric value to a tolerance-aware integer bucket."""
    return round(value / _POSITION_TOLERANCE_MM)


def solution_signature(solution: AssemblySolution) -> tuple:
    """Return a translation-invariant geometric signature."""
    if not solution.placements:
        return ()

    min_x = min(placement.x_mm for placement in solution.placements)
    min_y = min(placement.y_mm for placement in solution.placements)

    return tuple(
        sorted(
            (
                placement.board_id,
                _quantize(placement.x_mm - min_x),
                _quantize(placement.y_mm - min_y),
                _quantize(placement.length_mm),
                _quantize(placement.width_mm),
                placement.rotated,
            )
            for placement in solution.placements
        )
    )


def deduplicate_solutions(
    solutions: list[AssemblySolution],
) -> list[AssemblySolution]:
    """Keep the first solution for each geometric signature."""
    seen: set[tuple] = set()
    unique: list[AssemblySolution] = []

    for solution in solutions:
        signature = solution_signature(solution)

        if signature in seen:
            continue

        seen.add(signature)
        unique.append(solution)

    return unique
