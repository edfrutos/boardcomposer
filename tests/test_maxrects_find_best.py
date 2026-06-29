from boardcomposer.solver.maxrects.free_rectangle import FreeRectangle
from boardcomposer.solver.maxrects.maxrects import MaxRects


def test_find_best_rectangle():
    maxrects = MaxRects(3000, 1000)

    placement = maxrects.find_best_rectangle(1000, 500)

    assert placement is not None
    assert placement.x_mm == 0
    assert placement.y_mm == 0
    assert placement.length_mm == 1000
    assert placement.width_mm == 500


def test_find_best_rectangle_returns_none_when_piece_does_not_fit():
    maxrects = MaxRects(3000, 1000)

    placement = maxrects.find_best_rectangle(4000, 500)

    assert placement is None


def test_find_best_rectangle_prefers_less_waste():
    maxrects = MaxRects(3000, 1000)
    maxrects.free_rectangles = [
        FreeRectangle(0, 0, 3000, 1000),
        FreeRectangle(0, 1000, 1000, 500),
    ]

    placement = maxrects.find_best_rectangle(900, 400)

    assert placement is not None
    assert placement.x_mm == 0
    assert placement.y_mm == 1000


def test_find_best_rectangle_can_rotate():
    maxrects = MaxRects(500, 1000)

    placement = maxrects.find_best_rectangle(
        800,
        400,
        allow_rotation=True,
    )

    assert placement is not None
    assert placement.rotated is True


def test_maxrects_accepts_custom_heuristic():
    def select_last(candidates, waste_area):
        return candidates[-1] if candidates else None

    maxrects = MaxRects(
        length_mm=3000,
        width_mm=1000,
        heuristic=select_last,
    )

    placement = maxrects.find_best_rectangle(1000, 300)

    assert placement is not None
