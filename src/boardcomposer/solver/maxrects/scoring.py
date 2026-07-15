"""Scoring criteria for partial MaxRects beam-search states."""
from boardcomposer.solver.maxrects.state import MaxRectsState


def score_state(
    state: MaxRectsState,
) -> tuple[int, float, float, int, float, int, float, float]:
    """Score the state based on the number of placements, waste, and free rectangles."""
    if not state.placements:
        occupied_length = 0.0
        occupied_width = 0.0
    else:
        occupied_length = max(placement.right_mm for placement in state.placements)
        occupied_width = max(placement.top_mm for placement in state.placements)

    occupied_area = occupied_length * occupied_width
    used_area = sum(placement.area_mm2 for placement in state.placements)
    internal_waste = occupied_area - used_area

    free_rectangle_count = len(state.packer.free_rectangles)
    largest_free_area = max(
        (rectangle.area_mm2 for rectangle in state.packer.free_rectangles),
        default=0.0,
    )

    rotations = sum(1 for placement in state.placements if placement.rotated)

    return (
        len(state.placements),
        -internal_waste,
        -occupied_area,
        -free_rectangle_count,
        largest_free_area,
        -rotations,
        -occupied_length,
        -occupied_width,
    )
