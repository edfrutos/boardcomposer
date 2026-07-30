"""Tests for studio.unique_ids — shared board/piece id allocation."""

from types import SimpleNamespace

from studio.board_ids import allocate_unique_board_id, casefolded_board_ids
from studio.piece_ids import allocate_unique_piece_id, casefolded_piece_ids
from studio.unique_ids import allocate_unique_id, expand_ids_for_quantity, id_taken


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


def test_casefolded_piece_and_board_ids():
    project = SimpleNamespace(
        pieces=[SimpleNamespace(piece_id="A"), SimpleNamespace(piece_id="b")],
        boards=[SimpleNamespace(board_id="TAB-1"), SimpleNamespace(board_id="tab-2")],
    )
    assert casefolded_piece_ids(project) == {"a", "b"}
    assert casefolded_board_ids(project) == {"tab-1", "tab-2"}


def test_casefolded_piece_ids_strip_option():
    project = SimpleNamespace(
        pieces=[SimpleNamespace(piece_id="  LAT  "), SimpleNamespace(piece_id="X")],
    )
    assert casefolded_piece_ids(project, strip=True) == {"lat", "x"}
    assert "  lat  " in casefolded_piece_ids(project)


def test_id_taken_detects_casefold_and_strip_collisions():
    existing = ["A", "B"]
    assert id_taken("a", existing) is True
    assert id_taken("  b  ", existing) is True
    assert id_taken("C", existing) is False


def test_id_taken_excluding_skips_exact_current_id():
    existing = ["Panel-1", "Panel-2"]
    assert id_taken("panel-1", existing, excluding="Panel-1") is False
    assert id_taken("panel-2", existing, excluding="Panel-1") is True


def test_expand_ids_qty_one_reserves_base():
    reserved: set[str] = set()
    assert expand_ids_for_quantity("LAT", 1, reserved) == ["LAT"]
    assert "lat" in reserved
    assert expand_ids_for_quantity("LAT", 1, reserved) is None


def test_expand_ids_qty_many_uses_numeric_suffixes():
    reserved: set[str] = set()
    assert expand_ids_for_quantity("LAT", 3, reserved) == ["LAT-1", "LAT-2", "LAT-3"]
    assert reserved == {"lat", "lat-1", "lat-2", "lat-3"}


def test_expand_ids_qty_many_skips_taken_suffixes():
    reserved = {"lat-2"}
    assert expand_ids_for_quantity("LAT", 2, reserved) == ["LAT-1", "LAT-3"]


def test_expand_ids_qty_many_blocks_bare_base_afterwards():
    reserved: set[str] = set()
    assert expand_ids_for_quantity("LAT", 3, reserved) == ["LAT-1", "LAT-2", "LAT-3"]
    assert expand_ids_for_quantity("LAT", 1, reserved) is None


def test_expand_ids_occupied_base_returns_none():
    assert expand_ids_for_quantity("LAT", 3, {"lat"}) is None
    assert expand_ids_for_quantity("LAT", 1, {"LAT".casefold()}) is None
