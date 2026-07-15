"""Tests for MaxRects beam-state scoring."""

from boardcomposer import BoardPlacement
from boardcomposer.solver.maxrects.maxrects import MaxRects
from boardcomposer.solver.maxrects.scoring import score_state
from boardcomposer.solver.maxrects.state import MaxRectsState


def make_state(
    placements: list[BoardPlacement],
) -> MaxRectsState:
    """Create a MaxRects state with controlled placements."""
    return MaxRectsState(
        packer=MaxRects(3000, 1000),
        placements=placements,
        next_board=len(placements),
    )


def test_score_state_prefers_more_placements():
    """States containing more placed boards rank first."""
    empty = make_state([])
    placed = make_state([BoardPlacement("A", 0, 0, 100, 50)])

    assert score_state(placed) > score_state(empty)


def test_score_state_prefers_compact_placements():
    """A compact partial layout outranks one containing internal waste."""
    compact = make_state(
        [
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 100, 0, 100, 50),
        ]
    )
    separated = make_state(
        [
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 200, 0, 100, 50),
        ]
    )

    assert score_state(compact) > score_state(separated)


def test_score_state_prefers_fewer_rotations_when_geometry_matches():
    """Rotation count breaks ties between equivalent geometries."""
    normal = make_state([BoardPlacement("A", 0, 0, 100, 50, rotated=False)])
    rotated = make_state([BoardPlacement("A", 0, 0, 100, 50, rotated=True)])

    assert score_state(normal) > score_state(rotated)
