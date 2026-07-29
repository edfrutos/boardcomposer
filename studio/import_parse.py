"""Shared numeric parsers for Studio CSV/XLSX importers (FLW-002)."""

from __future__ import annotations

DEFAULT_IMPORT_THICKNESS_MM = 19.0
DEFAULT_IMPORT_QUANTITY = 1
DEFAULT_IMPORT_MATERIAL = "Generico"


def parse_positive_float(raw_value: str, label: str, errors: list[str]) -> float | None:
    """Parse a positive float; accept comma decimals (``1,5`` → ``1.5``)."""
    try:
        value = float(raw_value.strip().replace(",", "."))
    except (ValueError, AttributeError):
        errors.append(f"{label} no es un número válido: {raw_value!r}")
        return None

    if value <= 0:
        errors.append(f"{label} debe ser mayor que cero")
        return None

    return value


def parse_positive_int(raw_value: str, label: str, errors: list[str]) -> int | None:
    """Parse a positive integer (via float first so ``2.0`` is accepted)."""
    try:
        value = int(float(raw_value.strip()))
    except (ValueError, AttributeError):
        errors.append(f"{label} no es un número entero válido: {raw_value!r}")
        return None

    if value <= 0:
        errors.append(f"{label} debe ser mayor que cero")
        return None

    return value


def optional_positive_float(
    raw_row: dict[str, str],
    header_map: dict[str, str],
    field: str,
    label: str,
    default: float,
    errors: list[str],
) -> float:
    """Return mapped positive float, or ``default`` if missing/blank/invalid."""
    if field not in header_map:
        return default
    raw = raw_row.get(header_map[field], "").strip()
    if not raw:
        return default
    parsed = parse_positive_float(raw, label, errors)
    return default if parsed is None else parsed


def optional_positive_int(
    raw_row: dict[str, str],
    header_map: dict[str, str],
    field: str,
    label: str,
    default: int,
    errors: list[str],
) -> int:
    """Return mapped positive int, or ``default`` if missing/blank/invalid."""
    if field not in header_map:
        return default
    raw = raw_row.get(header_map[field], "").strip()
    if not raw:
        return default
    parsed = parse_positive_int(raw, label, errors)
    return default if parsed is None else parsed


def optional_string(
    raw_row: dict[str, str],
    header_map: dict[str, str],
    field: str,
    default: str,
) -> str:
    """Return mapped non-empty string, or ``default`` if missing/blank."""
    if field not in header_map:
        return default
    raw = raw_row.get(header_map[field], "").strip()
    return raw if raw else default
