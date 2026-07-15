from boardcomposer import Board, BoardPlacement
from boardcomposer.solver.maxrects.adaptive import AdaptiveSelector
from boardcomposer.solver.maxrects.heuristics import (
    best_area_fit,
    best_contact_point_fit,
    best_long_side_fit,
    best_short_side_fit,
)


def test_first_piece_uses_area_fit():
    selector = AdaptiveSelector()

    assert selector.choose(Board(500, 500, 19, "A"), []) is best_area_fit


def test_large_piece_prefers_long_side():
    selector = AdaptiveSelector()
    placed = [BoardPlacement("A", 0, 0, 100, 100)]

    assert selector.choose(Board(2000, 600, 19, "B"), placed) is best_long_side_fit


def test_small_piece_prefers_short_side():
    selector = AdaptiveSelector()
    placed = [BoardPlacement("A", 0, 0, 100, 100)]

    assert selector.choose(Board(300, 300, 19, "B"), placed) is best_short_side_fit


def test_many_pieces_prefers_contact():
    selector = AdaptiveSelector()
    placed = [
        BoardPlacement(str(index), index * 100, 0, 100, 100) for index in range(5)
    ]

    assert selector.choose(Board(800, 500, 19, "B"), placed) is best_contact_point_fit
