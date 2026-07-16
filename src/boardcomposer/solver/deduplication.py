"""Deduplicate geometrically equivalent layout solutions."""

from dataclasses import replace

from boardcomposer.domain import AssemblySolution, PanelReference

_POSITION_TOLERANCE_MM = 1.0


def _quantize(value: float) -> int:
    """Convert a numeric value to a tolerance-aware integer bucket."""
    return round(value / _POSITION_TOLERANCE_MM)


def solution_signature(solution: AssemblySolution) -> tuple:
    """Return a translation-invariant geometric signature."""
    if not solution.placements:
        return ()

    panel_origins: dict[PanelReference | None, tuple[float, float]] = {}
    for placement in solution.placements:
        reference = placement.panel_reference
        current = panel_origins.get(reference)
        if current is None:
            panel_origins[reference] = (placement.x_mm, placement.y_mm)
            continue
        panel_origins[reference] = (
            min(current[0], placement.x_mm),
            min(current[1], placement.y_mm),
        )

    return tuple(
        sorted(
            (
                placement.board_id,
                (
                    placement.panel_reference.stock_panel_index,
                    placement.panel_reference.instance_index,
                )
                if placement.panel_reference is not None
                else (-1, -1),
                _quantize(placement.x_mm - panel_origins[placement.panel_reference][0]),
                _quantize(placement.y_mm - panel_origins[placement.panel_reference][1]),
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
    """Keep the first solution for each geometric signature.

    Different candidate generators can reach the same geometric layout
    with different amounts of side information (offcuts, ...) attached.
    If the solution we keep for a signature lacks offcuts but a later
    duplicate has them, borrow them instead of silently discarding them.
    """
    seen: dict[tuple, int] = {}
    unique: list[AssemblySolution] = []

    for solution in solutions:
        signature = solution_signature(solution)
        existing_index = seen.get(signature)

        if existing_index is None:
            seen[signature] = len(unique)
            unique.append(solution)
            continue

        kept = unique[existing_index]
        if not kept.offcuts and solution.offcuts:
            unique[existing_index] = replace(kept, offcuts=solution.offcuts)

    return unique
