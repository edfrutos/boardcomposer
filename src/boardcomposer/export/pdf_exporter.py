"""Render an `AssemblySolution` as a minimal PDF 1.4 document.

Pure Python (no ReportLab): rectangles for panels/pieces plus Helvetica
labels. Coordinates are millimetres, scaled to PDF points (1 mm ≈ 2.834 pt).
"""

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.export.common import (
    canvas_size_mm,
    offcut_plan_label,
    panel_offsets,
    piece_plan_label,
)
from boardcomposer.export.cut_sequence import piece_sequence_numbers

_MM_TO_PT = 72.0 / 25.4
_MARGIN_PT = 36.0


def _escape_pdf_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _rect_ops(x_pt: float, y_pt: float, w_pt: float, h_pt: float) -> str:
    return f"{x_pt:.2f} {y_pt:.2f} {w_pt:.2f} {h_pt:.2f} re S"


def _text_ops(x_pt: float, y_pt: float, size_pt: float, value: str) -> str:
    return (
        f"BT /F1 {size_pt:.2f} Tf {x_pt:.2f} {y_pt:.2f} Td "
        f"({_escape_pdf_text(value)}) Tj ET"
    )


def solution_to_pdf(
    solution: AssemblySolution,
    project: Project | None = None,
    *,
    include_piece_labels: bool = True,
    include_offcut_labels: bool = True,
) -> bytes:
    """Render `solution` as PDF bytes."""
    offsets = panel_offsets(solution, project)
    width_mm, height_mm = canvas_size_mm(solution, project, offsets)
    # Extra headroom for panel labels above the drawing.
    height_mm += 30.0

    page_w = width_mm * _MM_TO_PT + 2 * _MARGIN_PT
    page_h = height_mm * _MM_TO_PT + 2 * _MARGIN_PT

    def to_page(x_mm: float, y_mm: float) -> tuple[float, float]:
        # PDF Y grows upward; our drawing Y grows downward from the top label.
        x_pt = _MARGIN_PT + x_mm * _MM_TO_PT
        y_pt = page_h - _MARGIN_PT - (y_mm + 0.0) * _MM_TO_PT
        return x_pt, y_pt

    ops: list[str] = ["0.2 w"]

    if project is not None:
        for reference, offset_x in offsets.items():
            panel = project.stock_panel_for(reference)
            if panel is None:
                continue
            label = panel.id or f"panel-{reference.stock_panel_index + 1}"
            x_pt, y_top = to_page(offset_x, 0.0)
            _, y_bottom = to_page(offset_x, panel.width_mm)
            h_pt = y_top - y_bottom
            ops.append(_rect_ops(x_pt, y_bottom, panel.length_mm * _MM_TO_PT, h_pt))
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
        x_pt, y_top = to_page(placement.x_mm + offset_x, placement.y_mm)
        _, y_bottom = to_page(
            placement.x_mm + offset_x, placement.y_mm + placement.width_mm
        )
        h_pt = y_top - y_bottom
        ops.append(_rect_ops(x_pt, y_bottom, placement.length_mm * _MM_TO_PT, h_pt))
        sequence = str(numbers.get(index, index + 1))
        ops.append(_text_ops(x_pt + 4, y_top - 12, 10, sequence))
        if include_piece_labels:
            ops.append(
                _text_ops(x_pt + 4, y_bottom + 4, 9, piece_plan_label(placement))
            )

    for offcut in solution.offcuts:
        offset_x = offsets.get(offcut.panel_reference, 0.0)
        x_pt, y_top = to_page(offcut.x_mm + offset_x, offcut.y_mm)
        _, y_bottom = to_page(
            offcut.x_mm + offset_x, offcut.y_mm + offcut.width_mm
        )
        h_pt = y_top - y_bottom
        ops.append("[8 4] 0 d")
        ops.append(_rect_ops(x_pt, y_bottom, offcut.length_mm * _MM_TO_PT, h_pt))
        ops.append("[] 0 d")
        if include_offcut_labels:
            ops.append(
                _text_ops(x_pt + 4, y_top - 12, 9, offcut_plan_label(offcut))
            )

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
