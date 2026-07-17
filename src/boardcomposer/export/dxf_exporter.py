"""Render an `AssemblySolution` as an ASCII DXF (AutoCAD R12-compatible).

No external dependencies: CAD tools (LibreCAD, QCAD, AutoCAD) can open the
result as a 2D cutting layout with one closed polyline per panel/piece.
"""

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.export.common import panel_offsets


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


def solution_to_dxf(
    solution: AssemblySolution,
    project: Project | None = None,
) -> str:
    """Render `solution` as a DXF document (mm coordinates, Y up)."""
    offsets = panel_offsets(solution, project)
    entities: list[str] = []

    if project is not None:
        for reference, offset_x in offsets.items():
            panel = project.stock_panel_for(reference)
            if panel is None:
                continue
            label = panel.id or f"panel-{reference.stock_panel_index + 1}"
            entities.extend(
                _rect(offset_x, 0.0, panel.length_mm, panel.width_mm, "PANELS")
            )
            entities.extend(
                _text(
                    offset_x + 5.0,
                    panel.width_mm + 5.0,
                    20.0,
                    f"{label} · {reference.instance_index + 1}",
                    "LABELS",
                )
            )

    for placement in solution.placements:
        offset_x = (
            offsets.get(placement.panel_reference, 0.0)
            if placement.panel_reference is not None
            else 0.0
        )
        entities.extend(
            _rect(
                placement.x_mm + offset_x,
                placement.y_mm,
                placement.length_mm,
                placement.width_mm,
                "PIECES",
            )
        )
        entities.extend(
            _text(
                placement.x_mm + offset_x + 5.0,
                placement.y_mm + 5.0,
                16.0,
                placement.board_id,
                "LABELS",
            )
        )

    for offcut in solution.offcuts:
        offset_x = offsets.get(offcut.panel_reference, 0.0)
        entities.extend(
            _rect(
                offcut.x_mm + offset_x,
                offcut.y_mm,
                offcut.length_mm,
                offcut.width_mm,
                "OFFCUTS",
            )
        )

    lines = [
        "0",
        "SECTION",
        "2",
        "HEADER",
        "0",
        "ENDSEC",
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
