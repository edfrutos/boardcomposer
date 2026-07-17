"""Load simple tabular files (CSV or Excel .xlsx) as string dictionaries.

Excel support covers FLW-002: selectable worksheet (default first sheet),
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
_REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


@dataclass(frozen=True)
class TabularLoadResult:
    """Outcome of reading a CSV or XLSX file into string rows."""

    fieldnames: tuple[str, ...] = ()
    rows: tuple[dict[str, str], ...] = ()
    errors: tuple[str, ...] = field(default_factory=tuple)
    sheet_name: str | None = None

    @property
    def ok(self) -> bool:
        return not self.errors and bool(self.fieldnames)


@dataclass(frozen=True)
class XlsxSheetInfo:
    """One worksheet entry from an Excel workbook."""

    name: str
    path: str


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


def _sheet_target_path(target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    return f"xl/{target}"


def list_xlsx_sheets(path: str | Path) -> tuple[XlsxSheetInfo, ...]:
    """Return worksheet names and archive paths for an .xlsx file."""
    file_path = Path(path)
    try:
        with zipfile.ZipFile(file_path) as archive:
            return _list_sheets(archive)
    except (OSError, zipfile.BadZipFile, ET.ParseError, KeyError):
        return ()


def _list_sheets(archive: zipfile.ZipFile) -> tuple[XlsxSheetInfo, ...]:
    try:
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    except KeyError:
        return ()

    targets = {
        relationship.attrib.get("Id"): relationship.attrib.get("Target", "")
        for relationship in rels.findall("pr:Relationship", _XLSX_NS)
    }
    sheets: list[XlsxSheetInfo] = []
    for sheet in workbook.findall("m:sheets/m:sheet", _XLSX_NS):
        name = sheet.attrib.get("name", "").strip()
        rel_id = sheet.attrib.get(_REL_NS)
        target = targets.get(rel_id, "") if rel_id else ""
        if not name or not target:
            continue
        sheets.append(XlsxSheetInfo(name=name, path=_sheet_target_path(target)))
    return tuple(sheets)


def _resolve_sheet_path(
    archive: zipfile.ZipFile,
    sheet: str | int | None,
) -> tuple[str | None, str | None, str | None]:
    """Return ``(sheet_path, sheet_name, error)``."""
    sheets = _list_sheets(archive)
    if not sheets:
        return None, None, "El archivo Excel no contiene hojas legibles"

    if sheet is None:
        return sheets[0].path, sheets[0].name, None

    if isinstance(sheet, int):
        if sheet < 0 or sheet >= len(sheets):
            return None, None, f"Índice de hoja fuera de rango: {sheet}"
        return sheets[sheet].path, sheets[sheet].name, None

    wanted = sheet.strip().casefold()
    for info in sheets:
        if info.name.casefold() == wanted:
            return info.path, info.name, None
    available = ", ".join(info.name for info in sheets)
    return None, None, f"Hoja no encontrada: {sheet!r}. Disponibles: {available}"


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


def _matrix_to_tabular(
    matrix: list[list[str]],
    *,
    sheet_name: str | None = None,
) -> TabularLoadResult:
    if not matrix:
        return TabularLoadResult(
            errors=("El archivo está vacío",),
            sheet_name=sheet_name,
        )

    header = [value.strip() for value in matrix[0]]
    while header and header[-1] == "":
        header.pop()
    if not any(header):
        return TabularLoadResult(
            errors=("El archivo está vacío",),
            sheet_name=sheet_name,
        )

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
            sheet_name=sheet_name,
        )

    return TabularLoadResult(
        fieldnames=tuple(header),
        rows=tuple(rows),
        sheet_name=sheet_name,
    )


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


def load_xlsx_file(
    path: Path,
    *,
    sheet: str | int | None = None,
) -> TabularLoadResult:
    try:
        with zipfile.ZipFile(path) as archive:
            sheet_path, sheet_name, error = _resolve_sheet_path(archive, sheet)
            if error or sheet_path is None:
                return TabularLoadResult(errors=(error or "Hoja no legible",))
            shared_strings = _read_shared_strings(archive)
            matrix = _sheet_matrix(archive, sheet_path, shared_strings)
    except zipfile.BadZipFile:
        return TabularLoadResult(errors=("El archivo Excel no es un .xlsx válido",))
    except (OSError, ET.ParseError, KeyError) as error:
        return TabularLoadResult(errors=(f"No se pudo leer el archivo Excel: {error}",))

    return _matrix_to_tabular(matrix, sheet_name=sheet_name)


def load_tabular_file(
    path: str | Path,
    *,
    sheet: str | int | None = None,
) -> TabularLoadResult:
    """Dispatch CSV / XLSX loaders by file extension."""
    file_path = Path(path)
    suffix = file_path.suffix.casefold()
    if suffix == ".csv":
        return load_csv_file(file_path)
    if suffix in {".xlsx", ".xlsm"}:
        return load_xlsx_file(file_path, sheet=sheet)
    return TabularLoadResult(
        errors=("Formato no soportado. Usa un archivo .csv o .xlsx.",)
    )
