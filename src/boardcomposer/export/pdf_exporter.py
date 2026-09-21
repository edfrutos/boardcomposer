"""Render an `AssemblySolution` as a minimal PDF 1.4 document.

Pure Python (no ReportLab): rectangles for panels/pieces plus Helvetica
labels. Coordinates are millimetres, scaled to PDF points (1 mm ≈ 2.834 pt).
"""

from __future__ import annotations

from datetime import datetime

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.export.common import (
    canvas_size_mm,
    offcut_plan_label,
    PANEL_COTA_GAP_MM,
    PANEL_COTA_TICK_MM,
    panel_dimension_label,
    panel_dimension_margins,
    panel_offsets,
    piece_plan_label,
    plan_traceability_label,
)
from boardcomposer.export.cut_sequence import piece_sequence_numbers
from boardcomposer.export.pdf_page import PdfPageOptions, resolve_pdf_page
from boardcomposer.units import DEFAULT_UNITS


def _escape_pdf_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _rect_ops(x_pt: float, y_pt: float, w_pt: float, h_pt: float) -> str:
    return f"{x_pt:.2f} {y_pt:.2f} {w_pt:.2f} {h_pt:.2f} re S"


def _text_ops(x_pt: float, y_pt: float, size_pt: float, value: str) -> str:
    return (
        f"BT /F1 {size_pt:.2f} Tf {x_pt:.2f} {y_pt:.2f} Td "
        f"({_escape_pdf_text(value)}) Tj ET"
    )


def _line_ops(x1: float, y1: float, x2: float, y2: float) -> str:
    return f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S"


def solution_to_pdf(
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
    page: PdfPageOptions | None = None,
    units: str = DEFAULT_UNITS,
) -> bytes:
    """Render `solution` as PDF bytes. TEXT uses ``units``; geometry stays mm."""
    offsets = panel_offsets(solution, project)
    origin_x, extra_bottom = panel_dimension_margins(
        include_panel_dimensions and bool(offsets)
    )
    width_mm, height_mm = canvas_size_mm(solution, project, offsets)
    # Extra headroom for panel labels above the drawing.
    width_mm += origin_x
    height_mm += 30.0 + extra_bottom
    footer_y = height_mm - 30.0 + 12.0
    if include_plan_traceability:
        height_mm += 16.0
        footer_y = height_mm - 30.0 - 4.0

    layout = resolve_pdf_page(width_mm, height_mm, page)
    page_w = layout.page_w_pt
    page_h = layout.page_h_pt
    scale = layout.scale_pt_per_mm

    def to_page(x_mm: float, y_mm: float) -> tuple[float, float]:
        # PDF Y grows upward; our drawing Y grows downward from the top label.
        x_pt = layout.origin_x_pt + x_mm * scale
        y_pt = page_h - layout.origin_y_top_pt - y_mm * scale
        return x_pt, y_pt

    ops: list[str] = ["0.2 w"]

    if project is not None:
        for reference, offset_x in offsets.items():
            panel = project.stock_panel_for(reference)
            if panel is None:
                continue
            label = panel.id or f"panel-{reference.stock_panel_index + 1}"
            x_pt, y_top = to_page(offset_x + origin_x, 0.0)
            _, y_bottom = to_page(offset_x + origin_x, panel.width_mm)
            h_pt = y_top - y_bottom
            ops.append(_rect_ops(x_pt, y_bottom, panel.length_mm * scale, h_pt))
            ops.append(
                _text_ops(
                    x_pt + 4,
                    y_top + 4,
                    10,
                    f"{label} · {reference.instance_index + 1}",
                )
            )

    numbers = piece_sequence_numbers(solution, project)
    for index, placement in enumerate(solution.placements):
        offset_x = (
            offsets.get(placement.panel_reference, 0.0)
            if placement.panel_reference is not None
            else 0.0
        )
        x_pt, y_top = to_page(placement.x_mm + offset_x + origin_x, placement.y_mm)
        _, y_bottom = to_page(
            placement.x_mm + offset_x + origin_x,
            placement.y_mm + placement.width_mm,
        )
        h_pt = y_top - y_bottom
        ops.append(_rect_ops(x_pt, y_bottom, placement.length_mm * scale, h_pt))
        sequence = str(numbers.get(index, index + 1))
        ops.append(_text_ops(x_pt + 4, y_top - 12, 10, sequence))
        if include_piece_labels:
            ops.append(
                _text_ops(x_pt + 4, y_bottom + 4, 9, piece_plan_label(placement, units))
            )

    for offcut in solution.offcuts:
        offset_x = offsets.get(offcut.panel_reference, 0.0)
        x_pt, y_top = to_page(offcut.x_mm + offset_x + origin_x, offcut.y_mm)
        _, y_bottom = to_page(
            offcut.x_mm + offset_x + origin_x, offcut.y_mm + offcut.width_mm
        )
        h_pt = y_top - y_bottom
        ops.append("[8 4] 0 d")
        ops.append(_rect_ops(x_pt, y_bottom, offcut.length_mm * scale, h_pt))
        ops.append("[] 0 d")
        if include_offcut_labels:
            ops.append(
                _text_ops(x_pt + 4, y_top - 12, 9, offcut_plan_label(offcut, units))
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
            hy = panel.width_mm + gap
            vx = left - gap
            x1, y_h = to_page(left, hy)
            x2, _ = to_page(right, hy)
            _, y_h_tick_a = to_page(left, hy - tick)
            _, y_h_tick_b = to_page(left, hy + tick)
            ops.append(_line_ops(x1, y_h, x2, y_h))
            ops.append(_line_ops(x1, y_h_tick_a, x1, y_h_tick_b))
            x_right, _ = to_page(right, hy)
            ops.append(_line_ops(x_right, y_h_tick_a, x_right, y_h_tick_b))
            mid_x, mid_y = to_page((left + right) / 2, hy + 8)
            ops.append(
                _text_ops(
                    mid_x - 12, mid_y, 9, panel_dimension_label(panel.length_mm, units)
                )
            )
            vx_pt, y_top = to_page(vx, 0.0)
            _, y_bot = to_page(vx, panel.width_mm)
            ops.append(_line_ops(vx_pt, y_top, vx_pt, y_bot))
            x_tick_a, _ = to_page(vx - tick, 0.0)
            x_tick_b, _ = to_page(vx + tick, 0.0)
            ops.append(_line_ops(x_tick_a, y_top, x_tick_b, y_top))
            _, y_bot2 = to_page(vx, panel.width_mm)
            ops.append(_line_ops(x_tick_a, y_bot2, x_tick_b, y_bot2))
            label_x, label_y = to_page(vx - 8, panel.width_mm / 2)
            ops.append(
                _text_ops(
                    label_x - 18,
                    label_y,
                    9,
                    panel_dimension_label(panel.width_mm, units),
                )
            )

    if include_plan_traceability:
        label = plan_traceability_label(
            version=app_version,
            strategy_name=strategy_name,
            exported_at=exported_at,
        )
        x_pt, y_pt = to_page(5.0, footer_y)
        ops.append(_text_ops(x_pt, y_pt, 8, label))

    content = "\n".join(ops).encode("latin-1", errors="replace")

    objects: list[bytes] = []
    objects.append(b"1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n")
    objects.append(b"2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj\n")
    objects.append(
        (
            f"3 0 obj<< /Type /Page /Parent 2 0 R "
            f"/MediaBox [0 0 {page_w:.2f} {page_h:.2f}] "
            f"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>endobj\n"
        ).encode("ascii")
    )
    objects.append(
        b"4 0 obj<< /Length "
        + str(len(content)).encode("ascii")
        + b" >>stream\n"
        + content
        + b"\nendstream\nendobj\n"
    )
    objects.append(
        b"5 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj\n"
    )

    pdf = bytearray(b"%PDF-1.4\n")
    offsets_table = [0]
    for obj in objects:
        offsets_table.append(len(pdf))
        pdf.extend(obj)

    xref_pos = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets_table)}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets_table[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        (
            f"trailer<< /Size {len(offsets_table)} /Root 1 0 R >>\n"
            f"startxref\n{xref_pos}\n%%EOF\n"
        ).encode("ascii")
    )
    return bytes(pdf)
