"""Render an `AssemblySolution` as a self-contained SVG document."""

from boardcomposer.domain import AssemblySolution, Offcut, PanelReference, Project
from boardcomposer.export.svg_palette import DEFAULT_SVG_PALETTE, SvgPalette

# Vertical space reserved above each panel row for its label, so it never
# overlaps the pieces placed right at the panel's own origin (y=0).
_PANEL_LABEL_MARGIN = 30
_LEGEND_LINE_HEIGHT = 20


def _panel_layout(
    solution: AssemblySolution,
    project: Project | None,
) -> tuple[dict[PanelReference, float], list[tuple[PanelReference, float, float, str]]]:
    offsets: dict[PanelReference, float] = {}
    panel_rows: list[tuple[PanelReference, float, float, str]] = []

    if project is None or not solution.panel_references:
        return offsets, panel_rows

    next_x = 0.0
    for reference in solution.panel_references:
        panel = project.stock_panel_for(reference)
        if panel is None:
            continue
        offsets[reference] = next_x
        label = panel.id or f"panel-{reference.stock_panel_index + 1}"
        panel_rows.append((reference, next_x, panel.width_mm, label))
        next_x += panel.length_mm + 50

    return offsets, panel_rows


def _canvas_size(
    solution: AssemblySolution,
    project: Project | None,
    panel_rows: list[tuple[PanelReference, float, float, str]],
) -> tuple[float, float]:
    if project is not None and panel_rows:
        width = 0.0
        for reference, offset_x, _panel_width, _label in panel_rows:
            panel = project.stock_panel_for(reference)
            if panel is None:
                continue
            width = max(width, offset_x + panel.length_mm)
        height = max((row[2] for row in panel_rows), default=0.0)
    else:
        width = solution.total_length_mm
        height = solution.total_width_mm

    return width, height + _PANEL_LABEL_MARGIN


def _panel_svg_parts(
    project: Project | None,
    panel_rows: list[tuple[PanelReference, float, float, str]],
    palette: SvgPalette,
) -> list[str]:
    if project is None:
        return []

    parts = []
    for reference, offset_x, _panel_width, label in panel_rows:
        panel = project.stock_panel_for(reference)
        if panel is None:
            continue
        y_offset = _PANEL_LABEL_MARGIN
        parts.append(
            f'<rect x="{offset_x:g}" y="{y_offset:g}" width="{panel.length_mm:g}" '
            f'height="{panel.width_mm:g}" fill="{palette.panel_fill}" '
            f'stroke="{palette.panel_stroke}" />'
        )
        parts.append(
            f'<text x="{offset_x + 5:g}" y="{y_offset - 10:g}" font-size="16" '
            f'fill="{palette.piece_label}">'
            f"{label} · {reference.instance_index + 1}</text>"
        )
    return parts


def _placement_svg_parts(
    solution: AssemblySolution,
    offsets: dict[PanelReference, float],
    palette: SvgPalette,
) -> list[str]:
    parts = []
    for placement in solution.placements:
        offset_x = (
            offsets.get(placement.panel_reference, 0.0)
            if placement.panel_reference is not None
            else 0.0
        )
        y_offset = _PANEL_LABEL_MARGIN
        parts.append(
            f'<rect x="{placement.x_mm + offset_x:g}" '
            f'y="{placement.y_mm + y_offset:g}" '
            f'width="{placement.length_mm:g}" height="{placement.width_mm:g}" '
            f'fill="{palette.piece_fill}" stroke="{palette.piece_stroke}" />'
        )
        parts.append(
            f'<text x="{placement.x_mm + offset_x + 5:g}" '
            f'y="{placement.y_mm + y_offset + 20:g}" font-size="16" '
            f'fill="{palette.piece_label}">'
            f"{placement.board_id}</text>"
        )
    return parts


def _offcut_svg_parts(
    offcuts: tuple[Offcut, ...],
    offsets: dict[PanelReference, float],
    palette: SvgPalette,
) -> list[str]:
    """Draw usable offcuts as dashed rectangles with an area label."""
    parts = []
    for offcut in offcuts:
        offset_x = offsets.get(offcut.panel_reference, 0.0)
        y_offset = _PANEL_LABEL_MARGIN
        parts.append(
            f'<rect x="{offcut.x_mm + offset_x:g}" y="{offcut.y_mm + y_offset:g}" '
            f'width="{offcut.length_mm:g}" height="{offcut.width_mm:g}" '
            f'fill="none" stroke="{palette.offcut_stroke}" stroke-dasharray="8,4" />'
        )
        parts.append(
            f'<text x="{offcut.x_mm + offset_x + 5:g}" '
            f'y="{offcut.y_mm + y_offset + 20:g}" font-size="14" '
            f'fill="{palette.offcut_stroke}">'
            f"{offcut.area_mm2:.0f} mm²</text>"
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


def solution_to_svg(
    solution: AssemblySolution,
    project: Project | None = None,
    *,
    palette: SvgPalette | None = None,
) -> str:
    """Render `solution` as an SVG document.

    Physical panels (if any) are laid out side by side. Placed pieces are
    filled rectangles, usable offcuts (ADR-016) are dashed rectangles,
    and, for partial solutions, a legend lists the pieces that couldn't be
    placed.
    """
    colors = palette or DEFAULT_SVG_PALETTE
    offsets, panel_rows = _panel_layout(solution, project)
    width, height = _canvas_size(solution, project, panel_rows)

    legend_parts = _legend_svg_parts(solution, height + _LEGEND_LINE_HEIGHT, colors)
    if legend_parts:
        height += _LEGEND_LINE_HEIGHT

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:g}" '
        f'height="{height:g}" viewBox="0 0 {width:g} {height:g}">',
        f'<rect width="100%" height="100%" fill="{colors.background}" />',
    ]
    parts.extend(_panel_svg_parts(project, panel_rows, colors))
    parts.extend(_placement_svg_parts(solution, offsets, colors))
    parts.extend(_offcut_svg_parts(solution.offcuts, offsets, colors))
    parts.extend(legend_parts)
    parts.append("</svg>")

    return "\n".join(parts)
