"""Parse CSV/Excel files describing a stock-panel inventory (FLW-002).

This module is pure Python (no Qt dependency) so it can be unit tested in
isolation. `ImportBoardsPreviewDialog` builds its preview table on top of
the `ImportBoardsResult` it returns.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from studio.models.board import StudioBoard
from studio.import_headers import (
    BOARD_HEADER_ALIASES,
    BOARD_REQUIRED_FIELDS,
    missing_required_fields,
    resolve_header_map,
    sanitize_header_map,
)
from studio.tabular_file import load_tabular_file
from studio.import_parse import (
    DEFAULT_IMPORT_MATERIAL,
    DEFAULT_IMPORT_QUANTITY,
    DEFAULT_IMPORT_THICKNESS_MM,
    optional_positive_float,
    optional_positive_int,
    optional_string,
    parse_positive_float,
)

_REQUIRED_FIELDS = BOARD_REQUIRED_FIELDS
_HEADER_ALIASES = BOARD_HEADER_ALIASES


@dataclass(frozen=True)
class ImportedBoardRow:
    """The result of parsing a single CSV/Excel row."""

    row_number: int
    raw: dict[str, str]
    board: StudioBoard | None = None
    display_id: str = ""
    errors: tuple[str, ...] = ()

    @property
    def is_valid(self) -> bool:
        return self.board is not None and not self.errors


@dataclass(frozen=True)
class ImportBoardsResult:
    """The complete outcome of importing a CSV/Excel inventory file."""

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


def _resolve_header_map(fieldnames: list[str] | tuple[str, ...]) -> dict[str, str]:
    """Map canonical field names to the actual header found in the file."""
    return resolve_header_map(fieldnames, _HEADER_ALIASES)


def _parse_row(
    row_number: int,
    raw_row: dict[str, str],
    header_map: dict[str, str],
    seen_ids: set[str],
    existing_ids: set[str],
) -> ImportedBoardRow:
    errors: list[str] = []
    display_id = ""
    if "board_id" in header_map:
        display_id = raw_row.get(header_map["board_id"], "").strip()

    missing = [field for field in _REQUIRED_FIELDS if field not in header_map]
    if missing:
        errors.append(f"Faltan columnas obligatorias: {', '.join(missing)}")
        return ImportedBoardRow(
            row_number=row_number,
            raw=raw_row,
            display_id=display_id,
            errors=tuple(errors),
        )

    board_id = display_id
    if not board_id:
        errors.append("El identificador no puede estar vacío")

    normalized_id = board_id.casefold()
    if normalized_id and normalized_id in seen_ids:
        errors.append(f"Identificador duplicado en el archivo: {board_id}")
    if normalized_id and normalized_id in existing_ids:
        errors.append(f"Ya existe un tablero con id {board_id} en el proyecto")

    length_mm = parse_positive_float(
        raw_row.get(header_map["length_mm"], ""), "Largo", errors
    )
    width_mm = parse_positive_float(
        raw_row.get(header_map["width_mm"], ""), "Ancho", errors
    )
    thickness_mm = optional_positive_float(
        raw_row,
        header_map,
        "thickness_mm",
        "Espesor",
        DEFAULT_IMPORT_THICKNESS_MM,
        errors,
    )
    quantity = optional_positive_int(
        raw_row,
        header_map,
        "quantity",
        "Cantidad",
        DEFAULT_IMPORT_QUANTITY,
        errors,
    )
    material = optional_string(raw_row, header_map, "material", DEFAULT_IMPORT_MATERIAL)

    if errors:
        return ImportedBoardRow(
            row_number=row_number,
            raw=raw_row,
            display_id=display_id,
            errors=tuple(errors),
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

    return ImportedBoardRow(
        row_number=row_number,
        raw=raw_row,
        board=board,
        display_id=display_id,
    )


def import_boards_from_rows(
    fieldnames: list[str] | tuple[str, ...],
    data_rows: list[dict[str, str]] | tuple[dict[str, str], ...],
    existing_ids: set[str] | None = None,
    *,
    header_map: dict[str, str] | None = None,
) -> ImportBoardsResult:
    """Parse already-loaded tabular rows into an `ImportBoardsResult`."""
    existing = {board_id.casefold() for board_id in (existing_ids or set())}
    resolved = (
        sanitize_header_map(header_map, fieldnames)
        if header_map is not None
        else _resolve_header_map(fieldnames)
    )
    missing = missing_required_fields(resolved, _REQUIRED_FIELDS)
    if missing:
        return ImportBoardsResult(
            file_errors=(
                f"No se reconocen las columnas obligatorias: {', '.join(missing)}",
            )
        )

    seen_ids: set[str] = set()
    rows = [
        _parse_row(index, raw_row, resolved, seen_ids, existing)
        for index, raw_row in enumerate(data_rows, start=2)
    ]
    if not rows:
        return ImportBoardsResult(
            file_errors=("El archivo no contiene filas de datos",)
        )
    return ImportBoardsResult(rows=tuple(rows))


def import_boards_from_file(
    path: str | Path,
    existing_ids: set[str] | None = None,
    *,
    header_map: dict[str, str] | None = None,
) -> ImportBoardsResult:
    """Parse a CSV or Excel inventory file and return an `ImportBoardsResult`."""
    loaded = load_tabular_file(path)
    if not loaded.ok:
        return ImportBoardsResult(file_errors=loaded.errors)
    return import_boards_from_rows(
        loaded.fieldnames,
        loaded.rows,
        existing_ids=existing_ids,
        header_map=header_map,
    )


def import_boards_from_csv(
    path: str | Path,
    existing_ids: set[str] | None = None,
) -> ImportBoardsResult:
    """Backward-compatible alias for `import_boards_from_file`."""
    return import_boards_from_file(path, existing_ids=existing_ids)
