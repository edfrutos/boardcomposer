"""Shared numeric parsers for Studio CSV/XLSX importers (FLW-002)."""

from __future__ import annotations


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
