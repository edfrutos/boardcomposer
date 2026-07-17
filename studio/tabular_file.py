"""Load simple tabular files (CSV or Excel .xlsx) as string dictionaries.

Excel support covers the common case used by FLW-002: first worksheet,
header row, shared strings / inline strings / numbers. No third-party
dependency — only the standard library OOXML zip + XML parser.
"""

from __future__ import annotations

import csv
import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree as ET

_XLSX_NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}

_CELL_REF_RE = re.compile(r"^([A-Z]+)(\d+)$")


@dataclass(frozen=True)
class TabularLoadResult:
    """Outcome of reading a CSV or XLSX file into string rows."""

    fieldnames: tuple[str, ...] = ()
    rows: tuple[dict[str, str], ...] = ()
    errors: tuple[str, ...] = field(default_factory=tuple)

    @property
    def ok(self) -> bool:
        return not self.errors and bool(self.fieldnames)


def _column_index(cell_ref: str) -> int | None:
    match = _CELL_REF_RE.match(cell_ref.upper())
    if match is None:
        return None
    letters = match.group(1)
    index = 0
    for char in letters:
        index = index * 26 + (ord(char) - ord("A") + 1)
    return index - 1


def _cell_text(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "s":
        value = cell.find("m:v", _XLSX_NS)
        if value is None or value.text is None:
            return ""
        try:
            return shared_strings[int(value.text)]
        except (ValueError, IndexError):
            return value.text
    if cell_type == "inlineStr":
        texts = cell.findall(".//m:t", _XLSX_NS)
        return "".join(part.text or "" for part in texts)
    value = cell.find("m:v", _XLSX_NS)
    if value is None or value.text is None:
        return ""
    return value.text


def _read_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    try:
        raw = archive.read("xl/sharedStrings.xml")
    except KeyError:
        return []

    root = ET.fromstring(raw)
    strings: list[str] = []
    for item in root.findall("m:si", _XLSX_NS):
        texts = item.findall(".//m:t", _XLSX_NS)
        strings.append("".join(part.text or "" for part in texts))
    return strings


def _first_sheet_path(archive: zipfile.ZipFile) -> str | None:
    try:
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    except KeyError:
        return None

    sheets = workbook.findall("m:sheets/m:sheet", _XLSX_NS)
    if not sheets:
        return None

    rel_id = sheets[0].attrib.get(
        "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    )
    if not rel_id:
        return None

    for relationship in rels.findall("pr:Relationship", _XLSX_NS):
        if relationship.attrib.get("Id") == rel_id:
            target = relationship.attrib.get("Target", "")
            if target.startswith("/"):
                return target.lstrip("/")
            return f"xl/{target}"
    return None


def _sheet_matrix(
    archive: zipfile.ZipFile, sheet_path: str, shared_strings: list[str]
) -> list[list[str]]:
    root = ET.fromstring(archive.read(sheet_path))
    matrix: list[list[str]] = []

    for row in root.findall("m:sheetData/m:row", _XLSX_NS):
        cells_by_index: dict[int, str] = {}
        max_index = -1
        for cell in row.findall("m:c", _XLSX_NS):
            ref = cell.attrib.get("r", "")
            index = _column_index(ref)
            if index is None:
                continue
            cells_by_index[index] = _cell_text(cell, shared_strings)
            max_index = max(max_index, index)

        if max_index < 0:
            matrix.append([])
            continue
        values = [cells_by_index.get(i, "") for i in range(max_index + 1)]
        matrix.append(values)

    return matrix


def _matrix_to_tabular(matrix: list[list[str]]) -> TabularLoadResult:
    if not matrix:
        return TabularLoadResult(errors=("El archivo está vacío",))

    header = [value.strip() for value in matrix[0]]
    while header and header[-1] == "":
        header.pop()
    if not any(header):
        return TabularLoadResult(errors=("El archivo está vacío",))

    width = len(header)
    rows: list[dict[str, str]] = []
    for values in matrix[1:]:
        padded = list(values) + [""] * max(0, width - len(values))
        padded = padded[:width]
        if not any(cell.strip() for cell in padded):
            continue
        rows.append({header[index]: padded[index].strip() for index in range(width)})

    if not rows:
        return TabularLoadResult(
            fieldnames=tuple(header),
            errors=("El archivo no contiene filas de datos",),
        )

    return TabularLoadResult(fieldnames=tuple(header), rows=tuple(rows))


def load_csv_file(path: Path) -> TabularLoadResult:
    try:
        with open(path, newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            fieldnames = reader.fieldnames
            if not fieldnames:
                return TabularLoadResult(errors=("El archivo está vacío",))
            rows = [
                {
                    key: (value or "").strip() if value is not None else ""
                    for key, value in raw.items()
                    if key is not None
                }
                for raw in reader
            ]
    except OSError as error:
        return TabularLoadResult(errors=(f"No se pudo leer el archivo: {error}",))
    except csv.Error as error:
        return TabularLoadResult(errors=(f"El archivo CSV no es válido: {error}",))

    if not rows:
        return TabularLoadResult(
            fieldnames=tuple(fieldnames),
            errors=("El archivo no contiene filas de datos",),
        )

    return TabularLoadResult(fieldnames=tuple(fieldnames), rows=tuple(rows))


def load_xlsx_file(path: Path) -> TabularLoadResult:
    try:
        with zipfile.ZipFile(path) as archive:
            sheet_path = _first_sheet_path(archive)
            if sheet_path is None:
                return TabularLoadResult(
                    errors=("El archivo Excel no contiene hojas legibles",)
                )
            shared_strings = _read_shared_strings(archive)
            matrix = _sheet_matrix(archive, sheet_path, shared_strings)
    except zipfile.BadZipFile:
        return TabularLoadResult(errors=("El archivo Excel no es un .xlsx válido",))
    except (OSError, ET.ParseError, KeyError) as error:
        return TabularLoadResult(errors=(f"No se pudo leer el archivo Excel: {error}",))

    return _matrix_to_tabular(matrix)


def load_tabular_file(path: str | Path) -> TabularLoadResult:
    """Dispatch CSV / XLSX loaders by file extension."""
    file_path = Path(path)
    suffix = file_path.suffix.casefold()
    if suffix == ".csv":
        return load_csv_file(file_path)
    if suffix in {".xlsx", ".xlsm"}:
        return load_xlsx_file(file_path)
    return TabularLoadResult(
        errors=("Formato no soportado. Usa un archivo .csv o .xlsx.",)
    )
