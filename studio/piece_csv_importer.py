"""Parse CSV files describing pieces to import into a Studio project (FLW-002).

Pure Python (no Qt). Quantity > 1 expands into several `StudioPiece` ids
(`P-1`, `P-2`, …) the same way as the New Piece dialog.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

from studio.models.piece import StudioPiece

_HEADER_ALIASES: dict[str, tuple[str, ...]] = {
    "piece_id": ("piece_id", "id", "identificador", "pieza", "referencia"),
    "length_mm": ("length_mm", "length", "largo_mm", "largo"),
    "width_mm": ("width_mm", "width", "ancho_mm", "ancho"),
    "thickness_mm": ("thickness_mm", "thickness", "espesor_mm", "espesor"),
    "quantity": ("quantity", "qty", "cantidad"),
    "material": ("material",),
}

_DEFAULT_THICKNESS_MM = 19.0
_DEFAULT_QUANTITY = 1
_DEFAULT_MATERIAL = "Generico"
_REQUIRED_FIELDS = ("piece_id", "length_mm", "width_mm")


@dataclass(frozen=True)
class ImportedPieceRow:
    """The result of parsing a single CSV row."""

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
    """The complete outcome of importing a pieces CSV file."""

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


def _resolve_header_map(fieldnames: list[str]) -> dict[str, str]:
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


def _expand_piece_ids(
    base_id: str,
    quantity: int,
    reserved: set[str],
) -> list[str] | None:
    if base_id.casefold() in reserved:
        return None
    if quantity <= 1:
        reserved.add(base_id.casefold())
        return [base_id]

    generated: list[str] = []
    suffix = 1
    while len(generated) < quantity:
        candidate = f"{base_id}-{suffix}"
        suffix += 1
        if candidate.casefold() in reserved:
            continue
        reserved.add(candidate.casefold())
        generated.append(candidate)
    return generated


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

    if errors or not piece_id or length_mm is None or width_mm is None:
        return ImportedPieceRow(
            row_number=row_number,
            raw=raw_row,
            base_id=piece_id,
            quantity=quantity,
            errors=tuple(errors),
        )

    piece_ids = _expand_piece_ids(piece_id, quantity, reserved_ids)
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


def import_pieces_from_csv(
    path: str | Path,
    existing_ids: set[str] | None = None,
) -> ImportPiecesResult:
    """Parse `path` and return an `ImportPiecesResult`."""
    reserved = {piece_id.casefold() for piece_id in (existing_ids or set())}

    try:
        with open(path, newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            fieldnames = reader.fieldnames

            if not fieldnames:
                return ImportPiecesResult(file_errors=("El archivo está vacío",))

            header_map = _resolve_header_map(fieldnames)
            missing = [field for field in _REQUIRED_FIELDS if field not in header_map]
            if missing:
                return ImportPiecesResult(
                    file_errors=(
                        "No se reconocen las columnas obligatorias: "
                        f"{', '.join(missing)}",
                    )
                )

            rows = [
                _parse_row(index, raw_row, header_map, reserved)
                for index, raw_row in enumerate(reader, start=2)
            ]
    except OSError as error:
        return ImportPiecesResult(file_errors=(f"No se pudo leer el archivo: {error}",))
    except csv.Error as error:
        return ImportPiecesResult(
            file_errors=(f"El archivo CSV no es válido: {error}",)
        )

    if not rows:
        return ImportPiecesResult(
            file_errors=("El archivo no contiene filas de datos",)
        )

    return ImportPiecesResult(rows=tuple(rows))
