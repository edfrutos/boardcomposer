from boardcomposer.solver.maxrects.heuristics import best_area_fit
from boardcomposer.solver.maxrects.placement import MaxRectsPlacement


def test_best_area_fit_returns_none_without_candidates():
    assert best_area_fit([], lambda _: 0) is None


def test_best_area_fit_prefers_less_waste():
    candidates = [
        MaxRectsPlacement(0, 0, 1000, 500),
        MaxRectsPlacement(0, 500, 500, 500),
    ]

    selected = best_area_fit(
        candidates,
        waste_area=lambda placement: 100 if placement.length_mm == 1000 else 10,
    )

    assert selected == candidates[1]
