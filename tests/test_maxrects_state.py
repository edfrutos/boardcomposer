"""
Test the MaxRects state.
"""

import pytest
from boardcomposer.solver.maxrects.free_rectangle import FreeRectangle
from boardcomposer.solver.maxrects.maxrects import MaxRects
from boardcomposer.solver.maxrects.state import MaxRectsState
from boardcomposer import Board, BoardPlacement


def test_state_can_be_created():
    """
    Test that the MaxRects state can be created.
    """
    state = MaxRectsState(
        packer=None,  # type: ignore[arg-type]
        placements=[],
        next_board=0,
    )

    assert state.next_board == 0


def test_clone_creates_independent_state():
    """
    Test that the MaxRects state can be cloned.
    """
    state = MaxRectsState(
        packer=MaxRects(),
        placements=[],
        next_board=0,
    )

    clone = state.clone()

    assert clone is not state
    assert clone.packer is not state.packer
    assert clone.placements is not state.placements
    assert clone.next_board == state.next_board


def test_expand_creates_child_states():
    """
    Test that the MaxRects state can be expanded.
    """
    state = MaxRectsState(
        packer=MaxRects(3000, 1000),
        placements=[],
        next_board=0,
    )

    children = state.expand(
        boards=[Board(1000, 500, 20, "A")],
        allow_rotation=False,
    )

    assert len(children) == 1
    assert children[0].next_board == 1
    assert len(children[0].placements) == 1


def test_expand_returns_one_child_per_candidate():
    """
    Test that the MaxRects state can return one child per candidate.
    """
    state = MaxRectsState(
        packer=MaxRects(),
        placements=[],
        next_board=0,
    )
    state.packer.free_rectangles = [
        FreeRectangle(0, 0, 3000, 1000),
        FreeRectangle(0, 1000, 1200, 600),
    ]

    children = state.expand(
        boards=[Board(1000, 500, 20, "A")],
        allow_rotation=False,
    )

    assert len(children) == 2


def test_expand_can_limit_candidate_count():
    """Limit the number of candidates to expand."""
    packer = MaxRects(3000, 2000)
    packer.free_rectangles = [
        FreeRectangle(0, 0, 1500, 1000),
        FreeRectangle(1500, 0, 1500, 1000),
        FreeRectangle(0, 1000, 1500, 1000),
    ]

    state = MaxRectsState(
        packer=packer,
        placements=[],
        next_board=0,
    )

    expanded = state.expand(
        boards=[Board(500, 500, 19, "A")],
        allow_rotation=False,
        candidate_width=2,
    )

    assert len(expanded) == 2


def test_expand_rejects_invalid_candidate_width():
    state = MaxRectsState(
        packer=MaxRects(3000, 1000),
        placements=[],
        next_board=0,
    )

    with pytest.raises(ValueError, match="candidate_width"):
        state.expand(
            boards=[Board(500, 500, 19, "A")],
            allow_rotation=False,
            candidate_width=0,
        )


def test_expand_prefers_candidate_with_more_contact():
    packer = MaxRects(3000, 2000)
    packer.free_rectangles = [
        FreeRectangle(1000, 1000, 500, 300),
        FreeRectangle(500, 0, 500, 300),
    ]

    state = MaxRectsState(
        packer=packer,
        placements=[
            BoardPlacement(
                board_id="A",
                x_mm=0,
                y_mm=0,
                length_mm=500,
                width_mm=300,
            )
        ],
        next_board=0,
    )

    expanded = state.expand(
        boards=[Board(500, 300, 19, "B")],
        allow_rotation=False,
        candidate_width=1,
    )

    assert len(expanded) == 1

    selected = expanded[0].placements[-1]

    assert selected.x_mm == 500
    assert selected.y_mm == 0


def test_expand_prefers_lower_waste_before_contact():
    """Prefer lower waste before contact when both are available."""
    packer = MaxRects(3000, 2000)
    packer.free_rectangles = [
        FreeRectangle(0, 0, 2000, 1000),
        FreeRectangle(2000, 0, 500, 500),
    ]

    state = MaxRectsState(
        packer=packer,
        placements=[
            BoardPlacement(
                board_id="A",
                x_mm=0,
                y_mm=1000,
                length_mm=500,
                width_mm=500,
            )
        ],
        next_board=0,
    )

    expanded = state.expand(
        boards=[Board(500, 500, 19, "B")],
        allow_rotation=False,
        candidate_width=1,
    )

    selected = expanded[0].placements[-1]

    assert selected.x_mm == 2000
    assert selected.y_mm == 0
