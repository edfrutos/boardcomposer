"""Render an `AssemblySolution` as a self-contained SVG document."""

from html import escape

from boardcomposer.domain import AssemblySolution, Offcut, PanelReference, Project
from boardcomposer.export.common import (
    canvas_size_mm,
    offcut_plan_label,
    panel_dimension_label,
    panel_dimension_margins,
    panel_offsets,
    piece_plan_label,
    PANEL_COTA_GAP_MM,
    PANEL_COTA_TICK_MM,
)
from boardcomposer.export.cut_sequence import piece_sequence_numbers
from boardcomposer.export.svg_palette import DEFAULT_SVG_PALETTE, SvgPalette

# Vertical space reserved above each panel row for its label, so it never
# overlaps the pieces placed right at the panel's own origin (y=0).
_PANEL_LABEL_MARGIN = 30
_LEGEND_LINE_HEIGHT = 20


def _panel_layout(
    solution: AssemblySolution,
    project: Project | None,
) -> tuple[dict[PanelReference, float], list[tuple[PanelReference, float, float, str]]]:
    offsets = panel_offsets(solution, project)
    panel_rows: list[tuple[PanelReference, float, float, str]] = []

    if project is None:
        return offsets, panel_rows

    for reference, offset_x in offsets.items():
        panel = project.stock_panel_for(reference)
        if panel is None:
            continue
        label = panel.id or f"panel-{reference.stock_panel_index + 1}"
        panel_rows.append((reference, offset_x, panel.width_mm, label))

    return offsets, panel_rows


def _canvas_size(
    solution: AssemblySolution,
    project: Project | None,
    offsets: dict[PanelReference, float],
    *,
    origin_x: float = 0.0,
    extra_bottom: float = 0.0,
) -> tuple[float, float]:
    width, height = canvas_size_mm(solution, project, offsets)
    return width + origin_x, height + _PANEL_LABEL_MARGIN + extra_bottom


def _panel_svg_parts(
    project: Project | None,
    panel_rows: list[tuple[PanelReference, float, float, str]],
    palette: SvgPalette,
    *,
    origin_x: float = 0.0,
) -> list[str]:
    if project is None:
        return []

    parts = []
    for reference, offset_x, _panel_width, label in panel_rows:
        panel = project.stock_panel_for(reference)
        if panel is None:
            continue
        y_offset = _PANEL_LABEL_MARGIN
        x0 = offset_x + origin_x
        parts.append(
            f'<rect x="{x0:g}" y="{y_offset:g}" width="{panel.length_mm:g}" '
            f'height="{panel.width_mm:g}" fill="{palette.panel_fill}" '
            f'stroke="{palette.panel_stroke}" />'
        )
        parts.append(
            f'<text x="{x0 + 5:g}" y="{y_offset - 10:g}" font-size="16" '
            f'fill="{palette.piece_label}">'
            f"{label} · {reference.instance_index + 1}</text>"
        )
    return parts


def _placement_svg_parts(
    solution: AssemblySolution,
    offsets: dict[PanelReference, float],
    palette: SvgPalette,
    *,
    include_piece_labels: bool,
    project: Project | None = None,
    origin_x: float = 0.0,
) -> list[str]:
    parts = []
    numbers = piece_sequence_numbers(solution, project)
    for index, placement in enumerate(solution.placements):
        offset_x = (
            offsets.get(placement.panel_reference, 0.0)
            if placement.panel_reference is not None
            else 0.0
        )
        y_offset = _PANEL_LABEL_MARGIN
        x0 = placement.x_mm + offset_x + origin_x
        parts.append(
            f'<rect x="{x0:g}" '
            f'y="{placement.y_mm + y_offset:g}" '
            f'width="{placement.length_mm:g}" height="{placement.width_mm:g}" '
            f'fill="{palette.piece_fill}" stroke="{palette.piece_stroke}" />'
        )
        sequence = numbers.get(index, index + 1)
        parts.append(
            f'<text x="{x0 + 5:g}" '
            f'y="{placement.y_mm + y_offset + 18:g}" font-size="14" '
            f'fill="{palette.piece_label}" data-cut-seq="{sequence}">'
            f"{sequence}</text>"
        )
        if not include_piece_labels:
            continue
        parts.append(
            f'<text x="{x0 + 5:g}" '
            f'y="{placement.y_mm + y_offset + 36:g}" font-size="16" '
            f'fill="{palette.piece_label}">'
            f"{escape(piece_plan_label(placement))}</text>"
        )
    return parts


def _offcut_svg_parts(
    offcuts: tuple[Offcut, ...],
    offsets: dict[PanelReference, float],
    palette: SvgPalette,
    *,
    include_offcut_labels: bool,
    origin_x: float = 0.0,
) -> list[str]:
    """Draw usable offcuts as dashed rectangles with optional LxW labels."""
    parts = []
    for offcut in offcuts:
        offset_x = offsets.get(offcut.panel_reference, 0.0)
        y_offset = _PANEL_LABEL_MARGIN
        x0 = offcut.x_mm + offset_x + origin_x
        parts.append(
            f'<rect x="{x0:g}" y="{offcut.y_mm + y_offset:g}" '
            f'width="{offcut.length_mm:g}" height="{offcut.width_mm:g}" '
            f'fill="none" stroke="{palette.offcut_stroke}" stroke-dasharray="8,4" />'
        )
        if not include_offcut_labels:
            continue
        parts.append(
            f'<text x="{x0 + 5:g}" '
            f'y="{offcut.y_mm + y_offset + 20:g}" font-size="14" '
            f'fill="{palette.offcut_stroke}">'
            f"{escape(offcut_plan_label(offcut))}</text>"
        )
    return parts


def _legend_svg_parts(
    solution: AssemblySolution,
    top_y: float,
    palette: SvgPalette,
) -> list[str]:
    if not solution.omitted_piece_ids:
        return []

    text = f"Piezas omitidas: {', '.join(solution.omitted_piece_ids)}"
    return [
        f'<text x="5" y="{top_y:g}" font-size="14" fill="{palette.legend}">'
        f"{text}</text>"
    ]


def _svg_line(x1: float, y1: float, x2: float, y2: float, color: str) -> str:
    return (
        f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" '
        f'stroke="{color}" stroke-width="1" />'
    )


def _panel_dimension_svg_parts(
    project: Project | None,
    panel_rows: list[tuple[PanelReference, float, float, str]],
    palette: SvgPalette,
    *,
    origin_x: float,
) -> list[str]:
    if project is None:
        return []
    parts: list[str] = []
    y0 = _PANEL_LABEL_MARGIN
    gap = PANEL_COTA_GAP_MM
    tick = PANEL_COTA_TICK_MM
    color = palette.piece_label
    for reference, offset_x, _panel_width, _label in panel_rows:
        panel = project.stock_panel_for(reference)
        if panel is None:
            continue
        left = offset_x + origin_x
        right = left + panel.length_mm
        top = y0
        bottom = y0 + panel.width_mm
        hy = bottom + gap
        parts.append(_svg_line(left, hy - tick, left, hy + tick, color))
        parts.append(_svg_line(right, hy - tick, right, hy + tick, color))
        parts.append(_svg_line(left, hy, right, hy, color))
        parts.append(
            f'<text x="{(left + right) / 2:g}" y="{hy + 14:g}" '
            f'font-size="14" text-anchor="middle" fill="{color}">'
            f"{escape(panel_dimension_label(panel.length_mm))}</text>"
        )
        vx = left - gap
        parts.append(_svg_line(vx - tick, top, vx + tick, top, color))
        parts.append(_svg_line(vx - tick, bottom, vx + tick, bottom, color))
        parts.append(_svg_line(vx, top, vx, bottom, color))
        parts.append(
            f'<text x="{vx - 6:g}" y="{(top + bottom) / 2 + 5:g}" '
            f'font-size="14" text-anchor="end" fill="{color}">'
            f"{escape(panel_dimension_label(panel.width_mm))}</text>"
        )
    return parts


def solution_to_svg(
    solution: AssemblySolution,
    project: Project | None = None,
    *,
    palette: SvgPalette | None = None,
    include_piece_labels: bool = True,
    include_offcut_labels: bool = True,
    include_panel_dimensions: bool = True,
) -> str:
    """Render `solution` as an SVG document.

    Physical panels (if any) are laid out side by side. Placed pieces are
    filled rectangles, usable offcuts (ADR-016) are dashed rectangles,
    and, for partial solutions, a legend lists the pieces that couldn't be
    placed. Piece labels (id + placed LxW mm) and offcut LxW labels can
    be omitted. Panel overall L/W dimension lines (IDE-0037) can too.
    """
    colors = palette or DEFAULT_SVG_PALETTE
    offsets, panel_rows = _panel_layout(solution, project)
    origin_x, extra_bottom = panel_dimension_margins(
        include_panel_dimensions and bool(panel_rows)
    )
    width, height = _canvas_size(
        solution,
        project,
        offsets,
        origin_x=origin_x,
        extra_bottom=extra_bottom,
    )

    legend_parts = _legend_svg_parts(solution, height + _LEGEND_LINE_HEIGHT, colors)
    if legend_parts:
        height += _LEGEND_LINE_HEIGHT

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:g}" '
        f'height="{height:g}" viewBox="0 0 {width:g} {height:g}">',
        f'<rect width="100%" height="100%" fill="{colors.background}" />',
    ]
    parts.extend(_panel_svg_parts(project, panel_rows, colors, origin_x=origin_x))
    parts.extend(
        _placement_svg_parts(
            solution,
            offsets,
            colors,
            include_piece_labels=include_piece_labels,
            project=project,
            origin_x=origin_x,
        )
    )
    parts.extend(
        _offcut_svg_parts(
            solution.offcuts,
            offsets,
            colors,
            include_offcut_labels=include_offcut_labels,
            origin_x=origin_x,
        )
    )
    if include_panel_dimensions:
        parts.extend(
            _panel_dimension_svg_parts(project, panel_rows, colors, origin_x=origin_x)
        )
    parts.extend(legend_parts)
    parts.append("</svg>")

    return "\n".join(parts)
