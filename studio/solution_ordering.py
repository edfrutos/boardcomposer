"""Sort and filter helpers for the Studio solution comparator (SCR-003).

Pure functions: the UI only decides *which* criterion to apply; this module
computes the resulting display order as indexes into the original solutions
list so the LayoutService ranking stays untouched.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from boardcomposer.domain import AssemblySolution


@dataclass(frozen=True)
class SortCriterion:
    key: str
    label: str
    value: Callable[[AssemblySolution], float]
    higher_is_better: bool


def _default_criteria(
    board_waste: Callable[[AssemblySolution], float] | None = None,
) -> dict[str, SortCriterion]:
    criteria = {
        "pieces": SortCriterion(
            "pieces",
            "Piezas colocadas",
            lambda s: float(len(s.placements)),
            True,
        ),
        "waste": SortCriterion(
            "waste",
            "Huecos internos",
            lambda s: s.waste_ratio,
            False,
        ),
        "score": SortCriterion(
            "score",
            "Puntuación",
            lambda s: s.score.total,
            True,
        ),
    }
    if board_waste is not None:
        criteria["board_waste"] = SortCriterion(
            "board_waste",
            "Tablero libre",
            board_waste,
            False,
        )
    return criteria


SORT_LABELS: tuple[tuple[str, str], ...] = (
    ("ranking", "Orden del solver"),
    ("pieces", "Piezas colocadas"),
    ("waste", "Huecos internos"),
    ("board_waste", "Tablero libre"),
    ("score", "Puntuación"),
)


def ordered_solution_indexes(
    solutions: list[AssemblySolution],
    *,
    sort_by: str = "ranking",
    complete_only: bool = False,
    board_waste: Callable[[AssemblySolution], float] | None = None,
) -> list[int]:
    """Return indexes into `solutions` in the requested display order.

    `ranking` preserves the pipeline order (already sorted by score).
    Unknown `sort_by` keys fall back to ranking.
    """
    indexes = list(range(len(solutions)))

    if complete_only:
        indexes = [index for index in indexes if solutions[index].is_complete]

    if sort_by == "ranking" or not indexes:
        return indexes

    criteria = _default_criteria(board_waste)
    criterion = criteria.get(sort_by)
    if criterion is None:
        return indexes

    return sorted(
        indexes,
        key=lambda index: criterion.value(solutions[index]),
        reverse=criterion.higher_is_better,
    )


def step_display_index(
    display_indexes: list[int],
    current: int,
    *,
    delta: int,
) -> int | None:
    """Next/previous index in the visible comparator order (wraps).

    If ``current`` is filtered out of the display list, jump to the first
    visible row when moving forward, or the last when moving backward.
    """
    if not display_indexes:
        return None
    if current in display_indexes:
        position = display_indexes.index(current)
    else:
        return display_indexes[0 if delta > 0 else -1]
    return display_indexes[(position + delta) % len(display_indexes)]
