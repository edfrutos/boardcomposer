"""Tests for shared import header resolution and manual mapping (FLW-002)."""

from studio.board_csv_importer import import_boards_from_rows
from studio.import_headers import (
    BOARD_HEADER_ALIASES,
    BOARD_REQUIRED_FIELDS,
    missing_required_fields,
    resolve_header_map,
    sanitize_header_map,
)
from studio.piece_csv_importer import import_pieces_from_rows


def test_resolve_header_map_uses_aliases():
    mapping = resolve_header_map(
        ["Identificador", "Largo", "Ancho"],
        BOARD_HEADER_ALIASES,
    )
    assert mapping["board_id"] == "Identificador"
    assert mapping["length_mm"] == "Largo"
    assert mapping["width_mm"] == "Ancho"
    assert missing_required_fields(mapping, BOARD_REQUIRED_FIELDS) == []


def test_missing_required_fields_lists_absent_canonicals():
    mapping = resolve_header_map(["Largo (mm)", "Ancho (mm)"], BOARD_HEADER_ALIASES)
    assert "board_id" in missing_required_fields(mapping, BOARD_REQUIRED_FIELDS)


def test_import_boards_with_manual_header_map():
    fieldnames = ["SKU", "Largo (mm)", "Ancho (mm)", "Espesor"]
    rows = [
        {
            "SKU": "TAB-1",
            "Largo (mm)": "2440",
            "Ancho (mm)": "1220",
            "Espesor": "19",
        }
    ]
    header_map = {
        "board_id": "SKU",
        "length_mm": "Largo (mm)",
        "width_mm": "Ancho (mm)",
        "thickness_mm": "Espesor",
    }
    result = import_boards_from_rows(fieldnames, rows, header_map=header_map)
    assert not result.file_errors
    assert len(result.valid_boards) == 1
    board = result.valid_boards[0]
    assert board.board_id == "TAB-1"
    assert board.length_mm == 2440
    assert board.width_mm == 1220
    assert board.thickness_mm == 19


def test_import_pieces_with_manual_header_map():
    fieldnames = ["Ref", "X", "Y"]
    rows = [{"Ref": "P1", "X": "500", "Y": "300"}]
    header_map = {
        "piece_id": "Ref",
        "length_mm": "X",
        "width_mm": "Y",
    }
    result = import_pieces_from_rows(fieldnames, rows, header_map=header_map)
    assert not result.file_errors
    assert len(result.valid_pieces) == 1
    assert result.valid_pieces[0].piece_id == "P1"


def test_sanitize_header_map_drops_unknown_headers():
    cleaned = sanitize_header_map(
        {"board_id": "SKU", "length_mm": "ghost"},
        ["SKU", "Largo"],
    )
    assert cleaned == {"board_id": "SKU"}
