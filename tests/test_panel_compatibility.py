"""Tests for studio.panel_compatibility — piece ↔ board material/thickness logic."""


from studio.models import StudioBoard, StudioPiece
from studio.panel_compatibility import (
    incompatibility_reason,
    material_key,
    piece_compatible_with_board,
)


def _piece(material: str = "MDF", thickness: float = 19.0) -> StudioPiece:
    return StudioPiece("P-1", 400, 200, material, thickness)


def _board(material: str = "MDF", thickness: float = 19.0) -> StudioBoard:
    return StudioBoard("B-1", 2000, 1000, material, thickness, 1)


# ---------------------------------------------------------------------------
# material_key
# ---------------------------------------------------------------------------


def test_material_key_strips_and_casefolds():
    assert material_key("  MDF  ") == "mdf"
    assert material_key("Oak") == "oak"


def test_material_key_none_returns_empty():
    assert material_key(None) == ""


def test_material_key_empty_string():
    assert material_key("") == ""


# ---------------------------------------------------------------------------
# piece_compatible_with_board
# ---------------------------------------------------------------------------


def test_compatible_same_material_thickness():
    assert piece_compatible_with_board(_piece(), _board()) is True


def test_incompatible_different_material():
    assert piece_compatible_with_board(_piece("MDF"), _board("Oak")) is False


def test_incompatible_different_thickness():
    assert (
        piece_compatible_with_board(_piece(thickness=19.0), _board(thickness=18.0))
        is False
    )


def test_incompatible_both_differ():
    assert (
        piece_compatible_with_board(_piece("MDF", 19.0), _board("Oak", 18.0)) is False
    )


def test_compatible_case_insensitive_material():
    assert piece_compatible_with_board(_piece("mdf"), _board("MDF")) is True


def test_compatible_empty_material_both():
    assert piece_compatible_with_board(_piece(""), _board("")) is True


def test_incompatible_one_material_empty():
    assert piece_compatible_with_board(_piece(""), _board("MDF")) is False


# ---------------------------------------------------------------------------
# incompatibility_reason
# ---------------------------------------------------------------------------


def test_reason_none_when_compatible():
    assert incompatibility_reason(_piece(), _board()) is None


def test_reason_material_only():
    assert incompatibility_reason(_piece("MDF"), _board("Oak")) == "material"


def test_reason_thickness_only():
    assert (
        incompatibility_reason(_piece(thickness=19.0), _board(thickness=18.0))
        == "thickness"
    )


def test_reason_both():
    assert incompatibility_reason(_piece("MDF", 19.0), _board("Oak", 18.0)) == "both"


def test_reason_floating_point_close_thickness():
    # math.isclose default rel_tol=1e-9; 19.0 + 1e-11 is within tolerance
    piece = _piece(thickness=19.0 + 1e-11)
    board = _board(thickness=19.0)
    assert incompatibility_reason(piece, board) is None
