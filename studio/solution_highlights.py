"""Highlight, per metric, which candidate solution scores best.

Pure helper for the Studio solution comparator (SCR-003): given the list of
solutions Studio is showing side by side, return which ones are the best
for each comparable metric, so the UI can flag them without re-deriving
the comparison logic itself.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from boardcomposer.domain import AssemblySolution


@dataclass(frozen=True)
class _Metric:
    label: str
    value: Callable[[AssemblySolution], float]
    higher_is_better: bool


_BASE_METRICS = (
    _Metric("highlight.pieces", lambda s: float(len(s.placements)), True),
    _Metric("highlight.waste", lambda s: s.waste_ratio, False),
    _Metric("highlight.score", lambda s: s.score.total, True),
    _Metric("highlight.length", lambda s: s.total_length_mm, False),
    _Metric("highlight.width", lambda s: s.total_width_mm, False),
)


def solution_highlights(
    solutions: list[AssemblySolution],
    *,
    board_waste: Callable[[AssemblySolution], float] | None = None,
) -> dict[int, list[str]]:
    """Return, for each solution index, the metrics where it's the best.

    With a single solution there's nothing to compare against, so an empty
    mapping is returned. Optional ``board_waste`` adds the free-board metric
    (same ratio the comparator table shows).
    """
    if len(solutions) < 2:
        return {}

    metrics: list[_Metric] = list(_BASE_METRICS)
    if board_waste is not None:
        metrics.append(_Metric("highlight.board_free", board_waste, False))

    highlights: dict[int, list[str]] = {}

    for metric in metrics:
        values = [metric.value(solution) for solution in solutions]
        best_value = max(values) if metric.higher_is_better else min(values)

        for index, value in enumerate(values):
            if value == best_value:
                highlights.setdefault(index, []).append(metric.label)

    return highlights
