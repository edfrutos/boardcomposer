"""Display-unit helpers for Studio dimensions (stored always in mm)."""

from __future__ import annotations

VALID_UNITS = ("mm", "cm", "in")
DEFAULT_UNITS = "mm"

_MM_PER_UNIT = {
    "mm": 1.0,
    "cm": 10.0,
    "in": 25.4,
}

_UNIT_LABELS = {
    "mm": "mm",
    "cm": "cm",
    "in": "in",
}


def normalize_units(units: str) -> str:
    return units if units in VALID_UNITS else DEFAULT_UNITS


def unit_label(units: str) -> str:
    return _UNIT_LABELS[normalize_units(units)]


def mm_to_display(value_mm: float, units: str) -> float:
    """Convert millimetres to the preferred display unit."""
    return float(value_mm) / _MM_PER_UNIT[normalize_units(units)]


def display_to_mm(value: float, units: str) -> float:
    """Convert a display-unit length back to millimetres."""
    return float(value) * _MM_PER_UNIT[normalize_units(units)]


def format_length(value_mm: float, units: str, *, decimals: int | None = None) -> str:
    """Format a millimetre value for UI display."""
    units = normalize_units(units)
    display = mm_to_display(value_mm, units)
    if decimals is None:
        decimals = 0 if units == "mm" else 2
    if decimals == 0:
        text = f"{display:g}"
    else:
        text = f"{display:.{decimals}f}".rstrip("0").rstrip(".")
    return f"{text} {unit_label(units)}"


def format_size(
    length_mm: float,
    width_mm: float,
    units: str,
    *,
    thickness_mm: float | None = None,
) -> str:
    """Format a 2D or 3D size using the preferred units."""
    numbers = [
        format_length(length_mm, units).rsplit(" ", 1)[0],
        format_length(width_mm, units).rsplit(" ", 1)[0],
    ]
    if thickness_mm is not None:
        numbers.append(format_length(thickness_mm, units).rsplit(" ", 1)[0])
    return " x ".join(numbers) + f" {unit_label(units)}"
