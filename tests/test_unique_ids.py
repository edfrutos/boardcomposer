"""Tests for studio.unique_ids — shared board/piece id allocation."""

from studio.board_ids import allocate_unique_board_id
from studio.piece_ids import allocate_unique_piece_id
from studio.unique_ids import allocate_unique_id


def test_allocate_unique_id_returns_base_when_free():
    assert allocate_unique_id("P1", set()) == "P1"
    assert allocate_unique_id("P1", {"other"}) == "P1"


def test_allocate_unique_id_casefold_collision():
    assert allocate_unique_id("P1", {"p1"}) == "P1-2"


def test_allocate_unique_id_skips_taken_suffixes():
    existing = {"demo", "demo-2", "demo-3"}
    assert allocate_unique_id("demo", existing) == "demo-4"


def test_allocate_unique_id_preserves_base_casing():
    assert allocate_unique_id("Board-A", {"board-a"}) == "Board-A-2"


def test_wrappers_delegate_to_shared_helper():
    existing = {"x-copy", "x-copy-2"}
    assert allocate_unique_board_id("X-copy", existing) == "X-copy-3"
    assert allocate_unique_piece_id("X-copy", existing) == "X-copy-3"
