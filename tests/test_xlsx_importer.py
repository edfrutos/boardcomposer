"""Tests for CSV/Excel tabular loading and importers (FLW-002)."""

from __future__ import annotations

import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

from studio.board_csv_importer import import_boards_from_file
from studio.piece_csv_importer import import_pieces_from_file
from studio.tabular_file import load_tabular_file


def _write_minimal_xlsx(path: Path, rows: list[list[str]]) -> Path:
    """Build a minimal first-sheet XLSX with shared strings (stdlib only)."""
    shared: list[str] = []
    shared_index: dict[str, int] = {}

    def share(value: str) -> int:
        if value not in shared_index:
            shared_index[value] = len(shared)
            shared.append(value)
        return shared_index[value]

    sheet_rows: list[str] = []
    for row_number, values in enumerate(rows, start=1):
        cells: list[str] = []
        for column_number, value in enumerate(values):
            col = chr(ord("A") + column_number)
            ref = f"{col}{row_number}"
            index = share(str(value))
            cells.append(f'<c r="{ref}" t="s"><v>{index}</v></c>')
        sheet_rows.append(f'<row r="{row_number}">{"".join(cells)}</row>')

    shared_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        f'count="{len(shared)}" uniqueCount="{len(shared)}">'
        + "".join(f"<si><t>{escape(value)}</t></si>" for value in shared)
        + "</sst>"
    )
    sheet_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f"<sheetData>{''.join(sheet_rows)}</sheetData></worksheet>"
    )
    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="Hoja1" sheetId="1" r:id="rId1"/></sheets>'
        "</workbook>"
    )
    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
        'Target="worksheets/sheet1.xml"/></Relationships>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '<Override PartName="/xl/sharedStrings.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
        "</Types>"
    )
    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/></Relationships>'
    )

    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", root_rels)
        archive.writestr("xl/workbook.xml", workbook_xml)
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        archive.writestr("xl/worksheets/sheet1.xml", sheet_xml)
        archive.writestr("xl/sharedStrings.xml", shared_xml)

    return path


def test_load_xlsx_file_reads_first_sheet(tmp_path):
    xlsx_path = _write_minimal_xlsx(
        tmp_path / "pieces.xlsx",
        [
            ["piece_id", "length_mm", "width_mm", "quantity"],
            ["LAT", "700", "300", "2"],
        ],
    )

    loaded = load_tabular_file(xlsx_path)

    assert loaded.ok
    assert loaded.fieldnames == ("piece_id", "length_mm", "width_mm", "quantity")
    assert loaded.rows[0]["piece_id"] == "LAT"


def test_import_pieces_from_xlsx_expands_quantity(tmp_path):
    xlsx_path = _write_minimal_xlsx(
        tmp_path / "pieces.xlsx",
        [
            ["pieza", "largo_mm", "ancho_mm", "cantidad"],
            ["LAT", "700", "300", "3"],
        ],
    )

    result = import_pieces_from_file(xlsx_path)

    assert [piece.piece_id for piece in result.valid_pieces] == [
        "LAT-1",
        "LAT-2",
        "LAT-3",
    ]


def test_import_boards_from_xlsx(tmp_path):
    xlsx_path = _write_minimal_xlsx(
        tmp_path / "boards.xlsx",
        [
            ["board_id", "length_mm", "width_mm", "quantity", "material"],
            ["TAB-1", "2800", "2070", "2", "Melamina"],
        ],
    )

    result = import_boards_from_file(xlsx_path)

    assert not result.has_errors
    board = result.valid_boards[0]
    assert board.board_id == "TAB-1"
    assert board.quantity == 2
    assert board.material == "Melamina"


def test_unsupported_extension_is_rejected(tmp_path):
    path = tmp_path / "data.txt"
    path.write_text("x", encoding="utf-8")

    result = import_pieces_from_file(path)

    assert "formato no soportado" in result.file_errors[0].casefold()
