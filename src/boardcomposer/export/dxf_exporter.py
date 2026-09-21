"""Render an `AssemblySolution` as an ASCII DXF (AutoCAD R12-compatible).

No external dependencies: CAD tools (LibreCAD, QCAD, AutoCAD) can open the
result as a 2D cutting layout with one closed polyline per panel/piece.
"""

from __future__ import annotations

from datetime import datetime

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.export.common import (
    PANEL_COTA_GAP_MM,
    PANEL_COTA_TICK_MM,
    offcut_plan_label,
    panel_dimension_label,
    panel_dimension_margins,
    panel_offsets,
    piece_plan_label,
    plan_traceability_label,
)
from boardcomposer.export.cut_sequence import piece_sequence_numbers
from boardcomposer.units import DEFAULT_UNITS

LAYER_PANELS = "PANELS"
LAYER_PIECES = "PIECES"
LAYER_OFFCUTS = "OFFCUTS"
LAYER_DIMS = "DIMS"
LAYER_SEQ = "SEQ"
LAYER_META = "META"

_LAYER_ORDER = (
    LAYER_PANELS,
    LAYER_PIECES,
    LAYER_OFFCUTS,
    LAYER_DIMS,
    LAYER_SEQ,
    LAYER_META,
)
_LAYER_COLORS = {
    "0": 7,
    LAYER_PANELS: 8,
    LAYER_PIECES: 4,
    LAYER_OFFCUTS: 1,
    LAYER_DIMS: 6,
    LAYER_SEQ: 2,
    LAYER_META: 8,
}


def _layer_record(name: str) -> list[str]:
    """Emit one LAYER table row (name, on, ACI color, CONTINUOUS)."""
    return [
        "0",
        "LAYER",
        "2",
        name,
        "70",
        "0",
        "62",
        str(_LAYER_COLORS.get(name, 7)),
        "6",
        "CONTINUOUS",
    ]


def _tables_section(used: set[str]) -> list[str]:
    """Declare used role layers so CAD/CNC can toggle them."""
    names = ["0"]
    names.extend(layer for layer in _LAYER_ORDER if layer in used)
    extras = sorted(used.difference(_LAYER_ORDER))
    names.extend(extras)
    records: list[str] = []
    for name in names:
        records.extend(_layer_record(name))
    return [
        "0",
        "SECTION",
        "2",
        "TABLES",
        "0",
        "TABLE",
        "2",
        "LAYER",
        "70",
        str(len(names)),
        *records,
        "0",
        "ENDTAB",
        "0",
        "ENDSEC",
    ]


def _entity_layers(tokens: list[str]) -> set[str]:
    """Return layer names attached to LWPOLYLINE / TEXT / LINE entities."""
    used: set[str] = set()
    for index, token in enumerate(tokens):
        if token not in {"LWPOLYLINE", "TEXT", "LINE"}:
            continue
        if index + 2 < len(tokens) and tokens[index + 1] == "8":
            used.add(tokens[index + 2])
    return used


def _polyline(points: list[tuple[float, float]], layer: str) -> list[str]:
    """Emit a closed LWPOLYLINE entity."""
    lines = [
        "0",
        "LWPOLYLINE",
        "8",
        layer,
        "90",
        str(len(points)),
        "70",
        "1",
    ]
    for x_mm, y_mm in points:
        lines.extend(["10", f"{x_mm:g}", "20", f"{y_mm:g}"])
    return lines


def _rect(
    x_mm: float,
    y_mm: float,
    length_mm: float,
    width_mm: float,
    layer: str,
) -> list[str]:
    return _polyline(
        [
            (x_mm, y_mm),
            (x_mm + length_mm, y_mm),
            (x_mm + length_mm, y_mm + width_mm),
            (x_mm, y_mm + width_mm),
        ],
        layer,
    )


def _text(
    x_mm: float,
    y_mm: float,
    height_mm: float,
    value: str,
    layer: str,
) -> list[str]:
    return [
        "0",
        "TEXT",
        "8",
        layer,
        "10",
        f"{x_mm:g}",
        "20",
        f"{y_mm:g}",
        "40",
        f"{height_mm:g}",
        "1",
        value,
    ]


def _line(x1: float, y1: float, x2: float, y2: float, layer: str) -> list[str]:
    return [
        "0",
        "LINE",
        "8",
        layer,
        "10",
        f"{x1:g}",
        "20",
        f"{y1:g}",
        "11",
        f"{x2:g}",
        "21",
        f"{y2:g}",
    ]


def solution_to_dxf(
    solution: AssemblySolution,
    project: Project | None = None,
    *,
    include_piece_labels: bool = True,
    include_offcut_labels: bool = True,
    include_panel_dimensions: bool = True,
    include_plan_traceability: bool = True,
    strategy_name: str | None = None,
    exported_at: datetime | str | None = None,
    app_version: str | None = None,
    units: str = DEFAULT_UNITS,
) -> str:
    """Render `solution` as a DXF document (mm coordinates, Y up).

    Role layers (IDE-0041): ``PANELS``, ``PIECES``, ``OFFCUTS``, ``DIMS``,
    ``SEQ``, ``META``. Declared in a LAYER table so CAD/CNC can toggle them.
    """
    offsets = panel_offsets(solution, project)
    origin_x, extra_bottom = panel_dimension_margins(
        include_panel_dimensions and bool(offsets)
    )
    entities: list[str] = []

    if project is not None:
        for reference, offset_x in offsets.items():
            panel = project.stock_panel_for(reference)
            if panel is None:
                continue
            label = panel.id or f"panel-{reference.stock_panel_index + 1}"
            entities.extend(
                _rect(
                    offset_x + origin_x,
                    0.0,
                    panel.length_mm,
                    panel.width_mm,
                    LAYER_PANELS,
                )
            )
            entities.extend(
                _text(
                    offset_x + origin_x + 5.0,
                    panel.width_mm + 5.0,
                    20.0,
                    f"{label} · {reference.instance_index + 1}",
                    LAYER_PANELS,
                )
            )

    numbers = piece_sequence_numbers(solution, project)
    for index, placement in enumerate(solution.placements):
        offset_x = (
            offsets.get(placement.panel_reference, 0.0)
            if placement.panel_reference is not None
            else 0.0
        )
        entities.extend(
            _rect(
                placement.x_mm + offset_x + origin_x,
                placement.y_mm,
                placement.length_mm,
                placement.width_mm,
                LAYER_PIECES,
            )
        )
        sequence = str(numbers.get(index, index + 1))
        entities.extend(
            _text(
                placement.x_mm + offset_x + origin_x + 5.0,
                placement.y_mm + placement.width_mm - 20.0,
                16.0,
                sequence,
                LAYER_SEQ,
            )
        )
        if include_piece_labels:
            entities.extend(
                _text(
                    placement.x_mm + offset_x + origin_x + 5.0,
                    placement.y_mm + 5.0,
                    16.0,
                    piece_plan_label(placement, units),
                    LAYER_PIECES,
                )
            )

    for offcut in solution.offcuts:
        offset_x = offsets.get(offcut.panel_reference, 0.0)
        entities.extend(
            _rect(
                offcut.x_mm + offset_x + origin_x,
                offcut.y_mm,
                offcut.length_mm,
                offcut.width_mm,
                LAYER_OFFCUTS,
            )
        )
        if include_offcut_labels:
            entities.extend(
                _text(
                    offcut.x_mm + offset_x + origin_x + 5.0,
                    offcut.y_mm + 5.0,
                    16.0,
                    offcut_plan_label(offcut, units),
                    LAYER_OFFCUTS,
                )
            )

    if include_panel_dimensions and project is not None:
        gap = PANEL_COTA_GAP_MM
        tick = PANEL_COTA_TICK_MM
        for reference, offset_x in offsets.items():
            panel = project.stock_panel_for(reference)
            if panel is None:
                continue
            left = offset_x + origin_x
            right = left + panel.length_mm
            hy = -gap
            entities.extend(_line(left, hy, right, hy, LAYER_DIMS))
            entities.extend(_line(left, hy - tick, left, hy + tick, LAYER_DIMS))
            entities.extend(_line(right, hy - tick, right, hy + tick, LAYER_DIMS))
            entities.extend(
                _text(
                    left + panel.length_mm / 2.0,
                    hy - 16.0,
                    16.0,
                    panel_dimension_label(panel.length_mm, units),
                    LAYER_DIMS,
                )
            )
            vx = left - gap
            entities.extend(_line(vx, 0.0, vx, panel.width_mm, LAYER_DIMS))
            entities.extend(_line(vx - tick, 0.0, vx + tick, 0.0, LAYER_DIMS))
            entities.extend(
                _line(vx - tick, panel.width_mm, vx + tick, panel.width_mm, LAYER_DIMS)
            )
            entities.extend(
                _text(
                    vx - 20.0,
                    panel.width_mm / 2.0,
                    16.0,
                    panel_dimension_label(panel.width_mm, units),
                    LAYER_DIMS,
                )
            )

    if include_plan_traceability:
        fy = -(extra_bottom + 18.0) if extra_bottom else -18.0
        entities.extend(
            _text(
                5.0,
                fy,
                16.0,
                plan_traceability_label(
                    version=app_version,
                    strategy_name=strategy_name,
                    exported_at=exported_at,
                ),
                LAYER_META,
            )
        )

    used_layers = _entity_layers(entities)
    lines = [
        "0",
        "SECTION",
        "2",
        "HEADER",
        "9",
        "$INSUNITS",
        "70",
        "4",
        "0",
        "ENDSEC",
        *_tables_section(used_layers),
        "0",
        "SECTION",
        "2",
        "ENTITIES",
        *entities,
        "0",
        "ENDSEC",
        "0",
        "EOF",
        "",
    ]
    return "\n".join(lines)
