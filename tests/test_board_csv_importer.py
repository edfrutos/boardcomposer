"""Tests for the CSV board-inventory importer (FLW-002)."""

from pathlib import Path

from studio.board_csv_importer import import_boards_from_csv


def _write_csv(tmp_path: Path, contents: str) -> Path:
    csv_path = tmp_path / "inventory.csv"
    csv_path.write_text(contents, encoding="utf-8")
    return csv_path


def test_import_boards_from_csv_parses_valid_rows(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        "board_id,length_mm,width_mm,thickness_mm,quantity,material\n"
        "TAB-1,2440,1220,19,3,Melamina blanca\n"
        "TAB-2,2750,1830,25,1,MDF\n",
    )

    result = import_boards_from_csv(csv_path)

    assert not result.has_errors
    assert len(result.valid_boards) == 2

    first = result.valid_boards[0]
    assert first.board_id == "TAB-1"
    assert first.length_mm == 2440
    assert first.width_mm == 1220
    assert first.thickness_mm == 19
    assert first.quantity == 3
    assert first.material == "Melamina blanca"


def test_import_boards_from_csv_applies_defaults_for_optional_columns(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm\nTAB-1,2440,1220\n",
    )

    result = import_boards_from_csv(csv_path)

    assert not result.has_errors
    board = result.valid_boards[0]
    assert board.thickness_mm == 19
    assert board.quantity == 1
    assert board.material == "Generico"


def test_import_boards_from_csv_recognizes_spanish_header_aliases(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        "identificador,largo_mm,ancho_mm,espesor_mm,cantidad,material\n"
        "TAB-1,2440,1220,19,2,MDF\n",
    )

    result = import_boards_from_csv(csv_path)

    assert not result.has_errors
    assert result.valid_boards[0].board_id == "TAB-1"


def test_import_boards_from_csv_reports_missing_required_columns(tmp_path):
    csv_path = _write_csv(tmp_path, "length_mm,width_mm\n2440,1220\n")

    result = import_boards_from_csv(csv_path)

    assert result.has_errors
    assert result.file_errors


def test_import_boards_from_csv_flags_non_numeric_dimensions(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        "board_id,length_mm,width_mm\nTAB-1,abc,1220\n",
    )

    result = import_boards_from_csv(csv_path)

    assert result.has_errors
    assert len(result.invalid_rows) == 1
    assert not result.valid_boards


def test_import_boards_from_csv_flags_non_positive_dimensions(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        "board_id,length_mm,width_mm\nTAB-1,0,1220\n",
    )

    result = import_boards_from_csv(csv_path)

    assert result.has_errors
    assert "Largo debe ser mayor que cero" in result.invalid_rows[0].errors[0]


def test_import_boards_from_csv_flags_duplicate_ids_within_the_file(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        "board_id,length_mm,width_mm\nTAB-1,2440,1220\nTAB-1,2000,1000\n",
    )

    result = import_boards_from_csv(csv_path)

    assert len(result.valid_boards) == 1
    assert len(result.invalid_rows) == 1
    assert "duplicado" in result.invalid_rows[0].errors[0]


def test_import_boards_from_csv_flags_ids_already_in_the_project(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        "board_id,length_mm,width_mm\nTAB-1,2440,1220\n",
    )

    result = import_boards_from_csv(csv_path, existing_ids={"tab-1"})

    assert not result.valid_boards
    assert "ya existe" in result.invalid_rows[0].errors[0].casefold()


def test_import_boards_from_csv_reports_missing_file():
    result = import_boards_from_csv("/nonexistent/path/inventory.csv")

    assert result.has_errors
    assert result.file_errors


def test_import_boards_from_csv_reports_empty_file(tmp_path):
    csv_path = _write_csv(tmp_path, "")

    result = import_boards_from_csv(csv_path)

    assert result.has_errors
    assert result.file_errors


def test_import_boards_from_csv_reports_file_with_only_a_header_row(tmp_path):
    csv_path = _write_csv(tmp_path, "board_id,length_mm,width_mm\n")

    result = import_boards_from_csv(csv_path)

    assert result.has_errors
    assert result.file_errors
