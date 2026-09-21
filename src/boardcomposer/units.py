"""Display-unit helpers (stored always in mm)."""

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


def _format_display_number(display: float, units: str, decimals: int | None) -> str:
    if decimals is None:
        decimals = 0 if units == "mm" else 2
    if decimals == 0:
        return f"{display:g}"
    return f"{display:.{decimals}f}".rstrip("0").rstrip(".")


def format_length(value_mm: float, units: str, *, decimals: int | None = None) -> str:
    """Format a millimetre value for UI display."""
    units = normalize_units(units)
    display = mm_to_display(value_mm, units)
    return f"{_format_display_number(display, units, decimals)} {unit_label(units)}"


def format_area(value_mm2: float, units: str, *, decimals: int | None = None) -> str:
    """Format a millimetre-squared value for UI display."""
    units = normalize_units(units)
    factor = _MM_PER_UNIT[units] ** 2
    display = float(value_mm2) / factor
    return f"{_format_display_number(display, units, decimals)} {unit_label(units)}²"


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


def format_plan_number(
    value_mm: float, units: str, *, decimals: int | None = None
) -> str:
    """Format a millimetre length for compact plan labels."""
    units = normalize_units(units)
    display = mm_to_display(value_mm, units)
    return _format_display_number(display, units, decimals)


def plan_size_label(
    length_mm: float, width_mm: float, units: str = DEFAULT_UNITS
) -> str:
    """Compact LxW for plan TEXT. mm omits the unit suffix."""
    units = normalize_units(units)
    size = (
        f"{format_plan_number(length_mm, units)}x{format_plan_number(width_mm, units)}"
    )
    if units == "mm":
        return size
    return f"{size} {unit_label(units)}"


def plan_length_label(value_mm: float, units: str = DEFAULT_UNITS) -> str:
    """Compact single length for panel cotas. mm omits the unit suffix."""
    units = normalize_units(units)
    number = format_plan_number(value_mm, units)
    if units == "mm":
        return number
    return f"{number} {unit_label(units)}"
