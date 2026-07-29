"""Parse CSV/Excel files describing pieces to import into a Studio project (FLW-002).

Pure Python (no Qt). Quantity > 1 expands into several `StudioPiece` ids
(`P-1`, `P-2`, …) the same way as the New Piece dialog.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from studio.models.piece import StudioPiece
from studio.import_headers import (
    EMPTY_DATA_ROWS_ERROR,
    PIECE_HEADER_ALIASES,
    PIECE_REQUIRED_FIELDS,
    prepare_import_header_map,
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
from studio.unique_ids import expand_ids_for_quantity

_REQUIRED_FIELDS = PIECE_REQUIRED_FIELDS
_HEADER_ALIASES = PIECE_HEADER_ALIASES


@dataclass(frozen=True)
class ImportedPieceRow:
    """The result of parsing a single CSV/Excel row."""

    row_number: int
    raw: dict[str, str]
    base_id: str = ""
    pieces: tuple[StudioPiece, ...] = ()
    quantity: int = 1
    errors: tuple[str, ...] = ()

    @property
    def is_valid(self) -> bool:
        return bool(self.pieces) and not self.errors


@dataclass(frozen=True)
class ImportPiecesResult:
    """The complete outcome of importing a pieces CSV/Excel file."""

    rows: tuple[ImportedPieceRow, ...] = field(default_factory=tuple)
    file_errors: tuple[str, ...] = ()

    @property
    def valid_rows(self) -> tuple[ImportedPieceRow, ...]:
        return tuple(row for row in self.rows if row.is_valid)

    @property
    def invalid_rows(self) -> tuple[ImportedPieceRow, ...]:
        return tuple(row for row in self.rows if not row.is_valid)

    @property
    def valid_pieces(self) -> tuple[StudioPiece, ...]:
        return tuple(piece for row in self.valid_rows for piece in row.pieces)

    @property
    def has_errors(self) -> bool:
        return bool(self.file_errors) or bool(self.invalid_rows)


def _parse_row(
    row_number: int,
    raw_row: dict[str, str],
    header_map: dict[str, str],
    reserved_ids: set[str],
) -> ImportedPieceRow:
    errors: list[str] = []

    piece_id = raw_row.get(header_map["piece_id"], "").strip()
    if not piece_id:
        errors.append("El identificador no puede estar vacío")

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

    if errors or not piece_id or length_mm is None or width_mm is None:
        return ImportedPieceRow(
            row_number=row_number,
            raw=raw_row,
            base_id=piece_id,
            quantity=quantity,
            errors=tuple(errors),
        )

    piece_ids = expand_ids_for_quantity(piece_id, quantity, reserved_ids)
    if piece_ids is None:
        return ImportedPieceRow(
            row_number=row_number,
            raw=raw_row,
            base_id=piece_id,
            quantity=quantity,
            errors=(f"Ya existe una pieza con id {piece_id}",),
        )

    pieces = tuple(
        StudioPiece(
            piece_id=generated_id,
            length_mm=length_mm,
            width_mm=width_mm,
            material=material,
            thickness_mm=thickness_mm,
        )
        for generated_id in piece_ids
    )
    return ImportedPieceRow(
        row_number=row_number,
        raw=raw_row,
        base_id=piece_id,
        pieces=pieces,
        quantity=quantity,
    )


def import_pieces_from_rows(
    fieldnames: list[str] | tuple[str, ...],
    data_rows: list[dict[str, str]] | tuple[dict[str, str], ...],
    existing_ids: set[str] | None = None,
    *,
    header_map: dict[str, str] | None = None,
) -> ImportPiecesResult:
    """Parse already-loaded tabular rows into an `ImportPiecesResult`."""
    reserved = {piece_id.casefold() for piece_id in (existing_ids or set())}
    resolved, header_error = prepare_import_header_map(
        fieldnames, _HEADER_ALIASES, _REQUIRED_FIELDS, header_map
    )
    if resolved is None:
        return ImportPiecesResult(
            file_errors=(header_error or "Columnas obligatorias no reconocidas",)
        )

    rows = [
        _parse_row(index, raw_row, resolved, reserved)
        for index, raw_row in enumerate(data_rows, start=2)
    ]
    if not rows:
        return ImportPiecesResult(file_errors=(EMPTY_DATA_ROWS_ERROR,))
    return ImportPiecesResult(rows=tuple(rows))


def import_pieces_from_file(
    path: str | Path,
    existing_ids: set[str] | None = None,
    *,
    header_map: dict[str, str] | None = None,
) -> ImportPiecesResult:
    """Parse a CSV or Excel file and return an `ImportPiecesResult`."""
    loaded = load_tabular_file(path)
    if not loaded.ok:
        return ImportPiecesResult(file_errors=loaded.errors)
    return import_pieces_from_rows(
        loaded.fieldnames,
        loaded.rows,
        existing_ids=existing_ids,
        header_map=header_map,
    )


def import_pieces_from_csv(
    path: str | Path,
    existing_ids: set[str] | None = None,
) -> ImportPiecesResult:
    """Backward-compatible alias for `import_pieces_from_file`."""
    return import_pieces_from_file(path, existing_ids=existing_ids)
