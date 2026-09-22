"""Shared panel layout for exporters (SVG / DXF / PDF)."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from importlib import metadata

from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    Offcut,
    PanelReference,
    Project,
)
from boardcomposer.units import (
    DEFAULT_UNITS,
    normalize_units,
    plan_length_label,
    plan_size_label,
    unit_label,
)

PANEL_GAP_MM = 50.0
PANEL_COTA_LEFT_MM = 32.0
PANEL_COTA_BOTTOM_MM = 24.0
PANEL_COTA_GAP_MM = 10.0
PANEL_COTA_TICK_MM = 4.0
PLAN_TRACE_LINE_MM = 18.0


def piece_plan_label(placement: BoardPlacement, units: str = DEFAULT_UNITS) -> str:
    """Workshop label: piece id and placed size (prefs units, ASCII ``x``)."""
    return (
        f"{placement.board_id} "
        f"{plan_size_label(placement.length_mm, placement.width_mm, units)}"
    )


def offcut_plan_label(offcut: Offcut, units: str = DEFAULT_UNITS) -> str:
    """Workshop label: offcut size (prefs units, ASCII ``x``)."""
    return plan_size_label(offcut.length_mm, offcut.width_mm, units)


def panel_dimension_label(value_mm: float, units: str = DEFAULT_UNITS) -> str:
    """Workshop dimension: overall panel size (prefs units)."""
    return plan_length_label(value_mm, units)


def report_size_label(
    length_mm: float, width_mm: float, units: str = DEFAULT_UNITS
) -> str:
    """Cut-list / quote PDF LxW. mm keeps ``400x300``; cm/in add suffix."""
    units = normalize_units(units)
    if units == DEFAULT_UNITS:
        return f"{length_mm:g}x{width_mm:g}"
    return plan_size_label(length_mm, width_mm, units)


def report_length_label(value_mm: float, units: str = DEFAULT_UNITS) -> str:
    """Single report length. mm keeps ``:g``; cm/in add suffix."""
    units = normalize_units(units)
    if units == DEFAULT_UNITS:
        return f"{value_mm:g}"
    return plan_length_label(value_mm, units)


def report_unit_label(units: str = DEFAULT_UNITS) -> str:
    """ASCII unit token for report headers (``mm`` / ``cm`` / ``in``)."""
    return unit_label(units)


def panel_dimension_margins(enabled: bool) -> tuple[float, float]:
    """Return ``(left, bottom)`` extra drawing mm when panel cotas are on."""
    if not enabled:
        return 0.0, 0.0
    return PANEL_COTA_LEFT_MM, PANEL_COTA_BOTTOM_MM


def app_version() -> str:
    """Installed BoardComposer version, or a placeholder if unpackaged."""
    try:
        return metadata.version("boardcomposer")
    except metadata.PackageNotFoundError:
        return "0.0.0+unknown"


def format_exported_at(when: datetime | None = None) -> str:
    """Local export stamp ``YYYY-MM-DD HH:MM``."""
    stamp = when if when is not None else datetime.now().astimezone()
    return stamp.strftime("%Y-%m-%d %H:%M")


def plan_traceability_label(
    *,
    version: str | None = None,
    strategy_name: str | None = None,
    exported_at: datetime | str | None = None,
) -> str:
    """Workshop footer: app version, packing strategy and export time."""
    ver = (version or app_version()).strip() or "0.0.0+unknown"
    algo = (strategy_name or "").strip() or "-"
    if isinstance(exported_at, datetime):
        when = format_exported_at(exported_at)
    elif isinstance(exported_at, str) and exported_at.strip():
        when = exported_at.strip()
    else:
        when = format_exported_at()
    return f"BoardComposer {ver} · {algo} · {when}"


def report_traceability_footer(
    *,
    include: bool = True,
    strategy_name: str | None = None,
    version: str | None = None,
    exported_at: datetime | str | None = None,
) -> list[str]:
    """Blank line + workshop footer, or nothing when disabled."""
    if not include:
        return []
    return [
        "",
        plan_traceability_label(
            version=version,
            strategy_name=strategy_name,
            exported_at=exported_at,
        ),
    ]


def prepare_solution_for_export(
    solution: AssemblySolution,
    *,
    include_offcuts: bool = True,
) -> AssemblySolution:
    """Return ``solution``, optionally stripping informative offcuts."""
    if include_offcuts:
        return solution
    return replace(solution, offcuts=())


def panel_offsets(
    solution: AssemblySolution,
    project: Project | None,
) -> dict[PanelReference, float]:
    """Return the X offset of every consumed physical panel, laid out L→R."""
    offsets: dict[PanelReference, float] = {}
    if project is None or not solution.panel_references:
        return offsets

    next_x = 0.0
    for reference in solution.panel_references:
        panel = project.stock_panel_for(reference)
        if panel is None:
            continue
        offsets[reference] = next_x
        next_x += panel.length_mm + PANEL_GAP_MM

    return offsets


def canvas_size_mm(
    solution: AssemblySolution,
    project: Project | None,
    offsets: dict[PanelReference, float],
) -> tuple[float, float]:
    """Return the bounding width/height of the exported drawing in mm."""
    if project is not None and offsets:
        width = 0.0
        height = 0.0
        for reference, offset_x in offsets.items():
            panel = project.stock_panel_for(reference)
            if panel is None:
                continue
            width = max(width, offset_x + panel.length_mm)
            height = max(height, panel.width_mm)
        return width, height

    return solution.total_length_mm, solution.total_width_mm
