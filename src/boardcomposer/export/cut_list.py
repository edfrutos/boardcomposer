"""Workshop cut list (IDE-0023): pieces, stock panels, and placed cuts."""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass

from boardcomposer.domain import AssemblySolution, Project

DEFAULT_CUT_LIST_FORMAT = "csv"
VALID_CUT_LIST_FORMATS = ("csv", "pdf")

_FIELDNAMES = (
    "section",
    "id",
    "value",
    "material",
    "thickness_mm",
    "length_mm",
    "width_mm",
    "quantity",
    "instance_index",
    "rotated",
    "panel_id",
    "x_mm",
    "y_mm",
    "omitted",
)

_PAGE_W = 595.28
_PAGE_H = 841.89
_MARGIN = 48.0
_LINE_H = 14.0
_LINES_PER_PAGE = 52


@dataclass(frozen=True)
class CutListMeta:
    """Optional project header printed on the workshop report."""

    project_name: str = ""
    client: str = ""
    reference: str = ""
    notes: str = ""
    kerf_mm: float = 0.0


@dataclass(frozen=True)
class CutListPanel:
    """Stock panel available or used in the selected solution."""

    panel_id: str
    material: str
    thickness_mm: float
    length_mm: float
    width_mm: float
    quantity: int
    instances_used: int


@dataclass(frozen=True)
class CutListPiece:
    """Inventory piece and whether the solution omitted it."""

    piece_id: str
    material: str
    thickness_mm: float
    length_mm: float
    width_mm: float
    omitted: bool


@dataclass(frozen=True)
class CutListCut:
    """One placed piece on a physical panel instance."""

    piece_id: str
    material: str
    thickness_mm: float
    length_mm: float
    width_mm: float
    rotated: bool
    panel_id: str
    stock_panel_index: int
    instance_index: int
    x_mm: float
    y_mm: float


@dataclass(frozen=True)
class CutList:
    """Structured cut list for CSV / PDF workshop export."""

    meta: CutListMeta
    panels: tuple[CutListPanel, ...]
    pieces: tuple[CutListPiece, ...]
    cuts: tuple[CutListCut, ...]


def normalize_cut_list_format(value: object) -> str:
    """Return ``csv`` or ``pdf``; unknown input becomes ``csv``."""
    if isinstance(value, str) and value.strip().lower() in VALID_CUT_LIST_FORMATS:
        return value.strip().lower()
    return DEFAULT_CUT_LIST_FORMAT


def build_cut_list(
    solution: AssemblySolution,
    project: Project | None = None,
    meta: CutListMeta | None = None,
) -> CutList:
    """Build a cut list from the selected solution and optional project."""
    header = meta or CutListMeta()
    if project is not None and header.kerf_mm == 0:
        header = CutListMeta(
            project_name=header.project_name,
            client=header.client,
            reference=header.reference,
            notes=header.notes,
            kerf_mm=project.constraints.kerf_mm,
        )

    omitted = set(solution.omitted_piece_ids)
    used_instances: dict[int, set[int]] = {}
    for placement in solution.placements:
        reference = placement.panel_reference
        if reference is None:
            continue
        used_instances.setdefault(reference.stock_panel_index, set()).add(
            reference.instance_index
        )

    panels: list[CutListPanel] = []
    if project is not None:
        for index, panel in enumerate(project.stock_panels):
            panels.append(
                CutListPanel(
                    panel_id=panel.id or f"panel-{index + 1}",
                    material=panel.material,
                    thickness_mm=panel.thickness_mm,
                    length_mm=panel.length_mm,
                    width_mm=panel.width_mm,
                    quantity=panel.quantity,
                    instances_used=len(used_instances.get(index, ())),
                )
            )

    pieces: list[CutListPiece] = []
    if project is not None:
        for board in project.boards:
            piece_id = board.id or ""
            pieces.append(
                CutListPiece(
                    piece_id=piece_id,
                    material=board.material,
                    thickness_mm=board.thickness_mm,
                    length_mm=board.length_mm,
                    width_mm=board.width_mm,
                    omitted=piece_id in omitted,
                )
            )
    else:
        for piece_id in omitted:
            pieces.append(
                CutListPiece(
                    piece_id=piece_id,
                    material="",
                    thickness_mm=0,
                    length_mm=0,
                    width_mm=0,
                    omitted=True,
                )
            )
        seen = {item.piece_id for item in pieces}
        for placement in solution.placements:
            if placement.board_id in seen:
                continue
            seen.add(placement.board_id)
            pieces.append(
                CutListPiece(
                    piece_id=placement.board_id,
                    material="",
                    thickness_mm=0,
                    length_mm=placement.length_mm,
                    width_mm=placement.width_mm,
                    omitted=False,
                )
            )

    cuts: list[CutListCut] = []
    for placement in solution.placements:
        reference = placement.panel_reference
        panel_id = ""
        stock_index = -1
        instance_index = 0
        material = ""
        thickness = 0.0
        if reference is not None:
            stock_index = reference.stock_panel_index
            instance_index = reference.instance_index
            if project is not None:
                panel = project.stock_panel_for(reference)
                if panel is not None:
                    panel_id = panel.id or f"panel-{stock_index + 1}"
                    material = panel.material
                    thickness = panel.thickness_mm
            if not panel_id:
                panel_id = f"panel-{stock_index + 1}"
        if project is not None:
            for board in project.boards:
                if board.id == placement.board_id:
                    material = material or board.material
                    thickness = thickness or board.thickness_mm
                    break
        cuts.append(
            CutListCut(
                piece_id=placement.board_id,
                material=material,
                thickness_mm=thickness,
                length_mm=placement.length_mm,
                width_mm=placement.width_mm,
                rotated=placement.rotated,
                panel_id=panel_id,
                stock_panel_index=stock_index,
                instance_index=instance_index,
                x_mm=placement.x_mm,
                y_mm=placement.y_mm,
            )
        )

    return CutList(
        meta=header,
        panels=tuple(panels),
        pieces=tuple(pieces),
        cuts=tuple(cuts),
    )


def cut_list_to_csv(cut_list: CutList) -> str:
    """Return a UTF-8 CSV with meta, panels, pieces, and cuts."""
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=_FIELDNAMES, lineterminator="\n")
    writer.writeheader()

    meta = cut_list.meta
    for key, value in (
        ("project_name", meta.project_name),
        ("client", meta.client),
        ("reference", meta.reference),
        ("notes", meta.notes),
        ("kerf_mm", meta.kerf_mm),
    ):
        writer.writerow({"section": "meta", "id": key, "value": value})

    for panel in cut_list.panels:
        writer.writerow(
            {
                "section": "panel",
                "id": panel.panel_id,
                "material": panel.material,
                "thickness_mm": panel.thickness_mm,
                "length_mm": panel.length_mm,
                "width_mm": panel.width_mm,
                "quantity": panel.quantity,
                "instance_index": panel.instances_used,
            }
        )

    for piece in cut_list.pieces:
        writer.writerow(
            {
                "section": "piece",
                "id": piece.piece_id,
                "material": piece.material,
                "thickness_mm": piece.thickness_mm,
                "length_mm": piece.length_mm,
                "width_mm": piece.width_mm,
                "omitted": "true" if piece.omitted else "false",
            }
        )

    for cut in cut_list.cuts:
        writer.writerow(
            {
                "section": "cut",
                "id": cut.piece_id,
                "material": cut.material,
                "thickness_mm": cut.thickness_mm,
                "length_mm": cut.length_mm,
                "width_mm": cut.width_mm,
                "instance_index": cut.instance_index,
                "rotated": "true" if cut.rotated else "false",
                "panel_id": cut.panel_id,
                "x_mm": cut.x_mm,
                "y_mm": cut.y_mm,
            }
        )

    return buffer.getvalue()


def cut_list_to_pdf(cut_list: CutList) -> bytes:
    """Return a printable A4 PDF with the same sections as the CSV."""
    lines = _report_lines(cut_list)
    return _pdf_from_lines(lines)


def render_cut_list(cut_list: CutList, fmt: str) -> str | bytes:
    """Render ``csv`` text or ``pdf`` bytes."""
    if normalize_cut_list_format(fmt) == "pdf":
        return cut_list_to_pdf(cut_list)
    return cut_list_to_csv(cut_list)


def _report_lines(cut_list: CutList) -> list[str]:
    meta = cut_list.meta
    lines = [
        "Lista de corte — BoardComposer",
        "",
        f"Proyecto: {meta.project_name or '-'}",
        f"Cliente: {meta.client or '-'}",
        f"Referencia: {meta.reference or '-'}",
        f"Notas: {meta.notes or '-'}",
        f"Kerf (mm): {meta.kerf_mm}",
        "",
        "Tableros",
        "id  material  espesor  LxW  stock  usados",
    ]
    if not cut_list.panels:
        lines.append("(sin inventario de tableros)")
    for panel in cut_list.panels:
        lines.append(
            f"{panel.panel_id}  {panel.material}  {panel.thickness_mm:g}  "
            f"{panel.length_mm:g}x{panel.width_mm:g}  {panel.quantity}  "
            f"{panel.instances_used}"
        )

    lines.extend(["", "Piezas", "id  material  espesor  LxW  omitida"])
    if not cut_list.pieces:
        lines.append("(sin piezas)")
    for piece in cut_list.pieces:
        omitted = "si" if piece.omitted else "no"
        lines.append(
            f"{piece.piece_id}  {piece.material}  {piece.thickness_mm:g}  "
            f"{piece.length_mm:g}x{piece.width_mm:g}  {omitted}"
        )

    lines.extend(["", "Cortes por tablero", "pieza  panel#  LxW  rotada  x,y"])
    if not cut_list.cuts:
        lines.append("(sin cortes colocados)")
    for cut in cut_list.cuts:
        rotated = "si" if cut.rotated else "no"
        panel_label = f"{cut.panel_id}#{cut.instance_index + 1}"
        lines.append(
            f"{cut.piece_id}  {panel_label}  "
            f"{cut.length_mm:g}x{cut.width_mm:g}  {rotated}  "
            f"{cut.x_mm:g},{cut.y_mm:g}"
        )
    return lines


def _escape_pdf_text(value: str) -> str:
    latin = value.encode("latin-1", errors="replace").decode("latin-1")
    return latin.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _pdf_from_lines(lines: list[str]) -> bytes:
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
