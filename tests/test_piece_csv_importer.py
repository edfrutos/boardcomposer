"""Tests for the CSV pieces importer (FLW-002)."""

from pathlib import Path

from studio.piece_csv_importer import import_pieces_from_csv


def _write_csv(tmp_path: Path, contents: str) -> Path:
    csv_path = tmp_path / "pieces.csv"
    csv_path.write_text(contents, encoding="utf-8")
    return csv_path


def test_import_pieces_from_csv_parses_valid_rows(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        "piece_id,length_mm,width_mm,thickness_mm,quantity,material\n"
        "LAT-1,700,300,19,1,Melamina blanca\n",
    )

    result = import_pieces_from_csv(csv_path)

    assert not result.has_errors
    piece = result.valid_pieces[0]
    assert piece.piece_id == "LAT-1"
    assert piece.length_mm == 700
    assert piece.material == "Melamina blanca"


def test_import_pieces_from_csv_expands_quantity_into_correlative_ids(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        "piece_id,length_mm,width_mm,quantity\nLAT,700,300,3\n",
    )

    result = import_pieces_from_csv(csv_path)

    assert [piece.piece_id for piece in result.valid_pieces] == [
        "LAT-1",
        "LAT-2",
        "LAT-3",
    ]


def test_import_pieces_from_csv_flags_existing_ids(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        "piece_id,length_mm,width_mm\nLAT-1,700,300\n",
    )

    result = import_pieces_from_csv(csv_path, existing_ids={"lat-1"})

    assert not result.valid_pieces
    assert "ya existe" in result.invalid_rows[0].errors[0].casefold()


def test_import_pieces_from_csv_recognizes_spanish_aliases(tmp_path):
    csv_path = _write_csv(
        tmp_path,
        "pieza,largo_mm,ancho_mm,cantidad\nA,100,50,1\n",
    )

    result = import_pieces_from_csv(csv_path)

    assert result.valid_pieces[0].piece_id == "A"
