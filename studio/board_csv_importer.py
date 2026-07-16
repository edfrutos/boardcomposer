"""Parse CSV files describing a stock-panel inventory (FLW-002).

This module is pure Python (no Qt dependency) so it can be unit tested in
isolation. `ImportBoardsPreviewDialog` builds its preview table on top of
the `ImportBoardsResult` it returns.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

from studio.models.board import StudioBoard

_HEADER_ALIASES: dict[str, tuple[str, ...]] = {
    "board_id": ("board_id", "id", "identificador", "tablero"),
    "length_mm": ("length_mm", "length", "largo_mm", "largo"),
    "width_mm": ("width_mm", "width", "ancho_mm", "ancho"),
    "thickness_mm": ("thickness_mm", "thickness", "espesor_mm", "espesor"),
    "quantity": ("quantity", "qty", "cantidad"),
    "material": ("material",),
}

_DEFAULT_THICKNESS_MM = 19.0
_DEFAULT_QUANTITY = 1
_DEFAULT_MATERIAL = "Generico"

_REQUIRED_FIELDS = ("board_id", "length_mm", "width_mm")


@dataclass(frozen=True)
class ImportedBoardRow:
    """The result of parsing a single CSV row."""

    row_number: int
    raw: dict[str, str]
    board: StudioBoard | None = None
    errors: tuple[str, ...] = ()

    @property
    def is_valid(self) -> bool:
        return self.board is not None and not self.errors


@dataclass(frozen=True)
class ImportBoardsResult:
    """The complete outcome of importing a CSV inventory file."""

    rows: tuple[ImportedBoardRow, ...] = field(default_factory=tuple)
    file_errors: tuple[str, ...] = ()

    @property
    def valid_rows(self) -> tuple[ImportedBoardRow, ...]:
        return tuple(row for row in self.rows if row.is_valid)

    @property
    def invalid_rows(self) -> tuple[ImportedBoardRow, ...]:
        return tuple(row for row in self.rows if not row.is_valid)

    @property
    def valid_boards(self) -> tuple[StudioBoard, ...]:
        return tuple(row.board for row in self.valid_rows if row.board is not None)

    @property
    def has_errors(self) -> bool:
        return bool(self.file_errors) or bool(self.invalid_rows)


def _resolve_header_map(fieldnames: list[str]) -> dict[str, str]:
    """Map canonical field names to the actual header found in the file."""
    normalized = {name.strip().casefold(): name for name in fieldnames}
    resolved: dict[str, str] = {}

    for canonical, aliases in _HEADER_ALIASES.items():
        for alias in aliases:
            if alias in normalized:
                resolved[canonical] = normalized[alias]
                break

    return resolved


def _parse_positive_float(
    raw_value: str, label: str, errors: list[str]
) -> float | None:
    try:
        value = float(raw_value.strip().replace(",", "."))
    except (ValueError, AttributeError):
        errors.append(f"{label} no es un número válido: {raw_value!r}")
        return None

    if value <= 0:
        errors.append(f"{label} debe ser mayor que cero")
        return None

    return value


def _parse_positive_int(raw_value: str, label: str, errors: list[str]) -> int | None:
    try:
        value = int(float(raw_value.strip()))
    except (ValueError, AttributeError):
        errors.append(f"{label} no es un número entero válido: {raw_value!r}")
        return None

    if value <= 0:
        errors.append(f"{label} debe ser mayor que cero")
        return None

    return value


def _parse_row(
    row_number: int,
    raw_row: dict[str, str],
    header_map: dict[str, str],
    seen_ids: set[str],
    existing_ids: set[str],
) -> ImportedBoardRow:
    errors: list[str] = []

    missing = [field for field in _REQUIRED_FIELDS if field not in header_map]
    if missing:
        errors.append(f"Faltan columnas obligatorias: {', '.join(missing)}")
        return ImportedBoardRow(
            row_number=row_number, raw=raw_row, errors=tuple(errors)
        )

    board_id = raw_row.get(header_map["board_id"], "").strip()
    if not board_id:
        errors.append("El identificador no puede estar vacío")

    normalized_id = board_id.casefold()
    if normalized_id and normalized_id in seen_ids:
        errors.append(f"Identificador duplicado en el archivo: {board_id}")
    if normalized_id and normalized_id in existing_ids:
        errors.append(f"Ya existe un tablero con id {board_id} en el proyecto")

    length_mm = _parse_positive_float(
        raw_row.get(header_map["length_mm"], ""), "Largo", errors
    )
    width_mm = _parse_positive_float(
        raw_row.get(header_map["width_mm"], ""), "Ancho", errors
    )

    thickness_mm = _DEFAULT_THICKNESS_MM
    if "thickness_mm" in header_map:
        raw_thickness = raw_row.get(header_map["thickness_mm"], "").strip()
        if raw_thickness:
            parsed = _parse_positive_float(raw_thickness, "Espesor", errors)
            if parsed is not None:
                thickness_mm = parsed

    quantity = _DEFAULT_QUANTITY
    if "quantity" in header_map:
        raw_quantity = raw_row.get(header_map["quantity"], "").strip()
        if raw_quantity:
            parsed_qty = _parse_positive_int(raw_quantity, "Cantidad", errors)
            if parsed_qty is not None:
                quantity = parsed_qty

    material = _DEFAULT_MATERIAL
    if "material" in header_map:
        raw_material = raw_row.get(header_map["material"], "").strip()
        if raw_material:
            material = raw_material

    if errors:
        return ImportedBoardRow(
            row_number=row_number, raw=raw_row, errors=tuple(errors)
        )

    seen_ids.add(normalized_id)

    board = StudioBoard(
        board_id=board_id,
        length_mm=length_mm,
        width_mm=width_mm,
        material=material,
        thickness_mm=thickness_mm,
        quantity=quantity,
    )

    return ImportedBoardRow(row_number=row_number, raw=raw_row, board=board)


def import_boards_from_csv(
    path: str | Path,
    existing_ids: set[str] | None = None,
) -> ImportBoardsResult:
    """Parse `path` and return an `ImportBoardsResult`.

    `existing_ids` should contain the case-folded ids already present in
    the target project, so duplicates against it can be flagged per row.
    """
    existing = {board_id.casefold() for board_id in (existing_ids or set())}

    try:
        with open(path, newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            fieldnames = reader.fieldnames

            if not fieldnames:
                return ImportBoardsResult(file_errors=("El archivo está vacío",))

            header_map = _resolve_header_map(fieldnames)
            missing = [field for field in _REQUIRED_FIELDS if field not in header_map]
            if missing:
                return ImportBoardsResult(
                    file_errors=(
                        "No se reconocen las columnas obligatorias: "
                        f"{', '.join(missing)}",
                    )
                )

            seen_ids: set[str] = set()
            rows = [
                _parse_row(index, raw_row, header_map, seen_ids, existing)
                for index, raw_row in enumerate(reader, start=2)
            ]
    except OSError as error:
        return ImportBoardsResult(
            file_errors=(f"No se pudo leer el archivo: {error}",)
        )
    except csv.Error as error:
        return ImportBoardsResult(
            file_errors=(f"El archivo CSV no es válido: {error}",)
        )

    if not rows:
        return ImportBoardsResult(
            file_errors=("El archivo no contiene filas de datos",)
        )

    return ImportBoardsResult(rows=tuple(rows))
