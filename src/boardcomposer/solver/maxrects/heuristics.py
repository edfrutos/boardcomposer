from collections.abc import Callable

from boardcomposer.solver.maxrects.placement import MaxRectsPlacement

WasteAreaFn = Callable[[MaxRectsPlacement], float]


def best_area_fit(
    candidates: list[MaxRectsPlacement],
    waste_area: WasteAreaFn,
) -> MaxRectsPlacement | None:
    if not candidates:
        return None

    return min(
        candidates,
        key=lambda candidate: (
            waste_area(candidate),
            candidate.y_mm,
            candidate.x_mm,
        ),
    )
