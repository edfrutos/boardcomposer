"""Test the MAXRECTS_BOARD_ORDERINGS tuple."""

from boardcomposer.solver.maxrects.orderings import MAXRECTS_BOARD_ORDERINGS


def test_maxrects_has_board_orderings():
    """Test that the MAXRECTS_BOARD_ORDERINGS tuple has the correct names."""
    assert [name for name, _ in MAXRECTS_BOARD_ORDERINGS] == [
        "original",
        "largest_area",
        "smallest_area",
        "longest_edge",
        "shortest_edge",
        "longest",
        "widest",
    ]
