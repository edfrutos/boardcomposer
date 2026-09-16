"""Minimal A4 Helvetica PDF from text lines (cut list / quote)."""

from __future__ import annotations

_PAGE_W = 595.28
_PAGE_H = 841.89
_MARGIN = 48.0
_LINE_H = 14.0
_LINES_PER_PAGE = 52


def pdf_from_text_lines(lines: list[str]) -> bytes:
    """Return a printable A4 PDF 1.4 document for ``lines``."""
    wrapped: list[str] = []
    for line in lines:
        wrapped.extend(_wrap_line(line))
    if not wrapped:
        wrapped = [""]

    page_streams: list[bytes] = []
    for start in range(0, len(wrapped), _LINES_PER_PAGE):
        chunk = wrapped[start : start + _LINES_PER_PAGE]
        ops = ["BT /F1 10 Tf"]
        y = _PAGE_H - _MARGIN
        for line in chunk:
            ops.append(
                f"1 0 0 1 {_MARGIN:.1f} {y:.1f} Tm ({_escape_pdf_text(line)}) Tj"
            )
            y -= _LINE_H
        ops.append("ET")
        page_streams.append("\n".join(ops).encode("latin-1", errors="replace"))

    page_count = len(page_streams)
    font_id = 3 + page_count * 2
    objects: list[bytes] = []
    objects.append(b"1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n")
    kids = " ".join(f"{3 + index * 2} 0 R" for index in range(page_count))
    objects.append(
        (
            f"2 0 obj<< /Type /Pages /Kids [{kids}] /Count {page_count} >>endobj\n"
        ).encode("ascii")
    )
    for index, content in enumerate(page_streams):
        page_id = 3 + index * 2
        content_id = page_id + 1
        objects.append(
            (
                f"{page_id} 0 obj<< /Type /Page /Parent 2 0 R "
                f"/MediaBox [0 0 {_PAGE_W:.2f} {_PAGE_H:.2f}] "
                f"/Contents {content_id} 0 R "
                f"/Resources << /Font << /F1 {font_id} 0 R >> >> >>endobj\n"
            ).encode("ascii")
        )
        objects.append(
            b"%d 0 obj<< /Length %d >>stream\n" % (content_id, len(content))
            + content
            + b"\nendstream\nendobj\n"
        )
    objects.append(
        (
            f"{font_id} 0 obj<< /Type /Font /Subtype /Type1 "
            f"/BaseFont /Helvetica >>endobj\n"
        ).encode("ascii")
    )

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj)
    xref_pos = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets)}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        (
            f"trailer<< /Size {len(offsets)} /Root 1 0 R >>\n"
            f"startxref\n{xref_pos}\n%%EOF\n"
        ).encode("ascii")
    )
    return bytes(pdf)


def _escape_pdf_text(value: str) -> str:
    latin = value.encode("latin-1", errors="replace").decode("latin-1")
    return latin.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _wrap_line(text: str, width: int = 92) -> list[str]:
    if len(text) <= width:
        return [text]
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        trial = f"{current} {word}"
        if len(trial) <= width:
            current = trial
            continue
        lines.append(current)
        current = word
    lines.append(current)
    return lines
