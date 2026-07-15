from boardcomposer.domain import Board, BoardPlacement
from boardcomposer.solver.maxrects.heuristics import (
    best_area_fit,
    best_bottom_left_fit,
    best_contact_point_fit,
    best_long_side_fit,
    best_short_side_fit,
)


class AdaptiveSelector:
    def choose(
        self,
        board: Board,
        placed: list[BoardPlacement],
    ):
        area = board.length_mm * board.width_mm

        if not placed:
            return best_area_fit

        if area > 1_000_000:
            return best_long_side_fit

        if area < 250_000:
            return best_short_side_fit

        if len(placed) >= 5:
            return best_contact_point_fit

        return best_bottom_left_fit
