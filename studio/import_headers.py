"""Shared CSV/Excel header resolution for Studio imports (FLW-002)."""

from __future__ import annotations

BOARD_HEADER_ALIASES: dict[str, tuple[str, ...]] = {
    "board_id": ("board_id", "id", "identificador", "tablero"),
    "length_mm": ("length_mm", "length", "largo_mm", "largo"),
    "width_mm": ("width_mm", "width", "ancho_mm", "ancho"),
    "thickness_mm": ("thickness_mm", "thickness", "espesor_mm", "espesor"),
    "quantity": ("quantity", "qty", "cantidad"),
    "material": ("material",),
}

PIECE_HEADER_ALIASES: dict[str, tuple[str, ...]] = {
    "piece_id": ("piece_id", "id", "identificador", "pieza", "referencia"),
    "length_mm": ("length_mm", "length", "largo_mm", "largo"),
    "width_mm": ("width_mm", "width", "ancho_mm", "ancho"),
    "thickness_mm": ("thickness_mm", "thickness", "espesor_mm", "espesor"),
    "quantity": ("quantity", "qty", "cantidad"),
    "material": ("material",),
}

BOARD_REQUIRED_FIELDS = ("board_id", "length_mm", "width_mm")
PIECE_REQUIRED_FIELDS = ("piece_id", "length_mm", "width_mm")

BOARD_FIELD_ORDER = (
    "board_id",
    "length_mm",
    "width_mm",
    "thickness_mm",
    "quantity",
    "material",
)
PIECE_FIELD_ORDER = (
    "piece_id",
    "length_mm",
    "width_mm",
    "thickness_mm",
    "quantity",
    "material",
)


def resolve_header_map(
    fieldnames: list[str] | tuple[str, ...],
    aliases: dict[str, tuple[str, ...]],
) -> dict[str, str]:
    """Map canonical field names to the actual header found in the file."""
    normalized = {name.strip().casefold(): name for name in fieldnames}
    resolved: dict[str, str] = {}
    for canonical, names in aliases.items():
        for alias in names:
            if alias in normalized:
                resolved[canonical] = normalized[alias]
                break
    return resolved


def missing_required_fields(
    header_map: dict[str, str],
    required: tuple[str, ...] | list[str],
) -> list[str]:
    """Return required canonical fields absent from ``header_map``."""
    return [field for field in required if field not in header_map]


def sanitize_header_map(
    header_map: dict[str, str],
    fieldnames: list[str] | tuple[str, ...],
) -> dict[str, str]:
    """Keep only mappings whose value is a real header in the file."""
    allowed = set(fieldnames)
    return {
        canonical: header
        for canonical, header in header_map.items()
        if header in allowed
    }


EMPTY_DATA_ROWS_ERROR = "El archivo no contiene filas de datos"


def prepare_import_header_map(
    fieldnames: list[str] | tuple[str, ...],
    aliases: dict[str, tuple[str, ...]],
    required: tuple[str, ...] | list[str],
    header_map: dict[str, str] | None = None,
) -> tuple[dict[str, str] | None, str | None]:
    """Resolve or sanitize headers; return ``(map, None)`` or ``(None, error)``."""
    resolved = (
        sanitize_header_map(header_map, fieldnames)
        if header_map is not None
        else resolve_header_map(fieldnames, aliases)
    )
    missing = missing_required_fields(resolved, required)
    if missing:
        return (
            None,
            f"No se reconocen las columnas obligatorias: {', '.join(missing)}",
        )
    return resolved, None
