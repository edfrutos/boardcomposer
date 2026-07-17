"""Shared panel layout for exporters (SVG / DXF / PDF)."""

from boardcomposer.domain import AssemblySolution, PanelReference, Project

PANEL_GAP_MM = 50.0


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
