"""Workshop cut list (IDE-0023): pieces, stock panels, and placed cuts.

PDF reports can append the IDE-0043 traceability footer; CSV stays data-only.
PDF TEXT follows ``meta.units`` (IDE-0048); CSV columns stay millimetres.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass, replace

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.export.cut_sequence import (
    PanelCutSequence,
    SequenceStep,
    build_cut_sequences,
    piece_sequence_numbers,
)
from boardcomposer.export.common import (
    report_length_label,
    report_size_label,
    report_traceability_footer,
    report_unit_label,
)
from boardcomposer.units import DEFAULT_UNITS, normalize_units
from boardcomposer.export.report_pdf import pdf_from_text_lines

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
    "sequence",
)


@dataclass(frozen=True)
class CutListMeta:
    """Optional project header printed on the workshop report."""

    project_name: str = ""
    client: str = ""
    reference: str = ""
    notes: str = ""
    kerf_mm: float = 0.0
    include_traceability: bool = True
    strategy_name: str = ""
    version: str | None = None
    exported_at: str | None = None
    units: str = DEFAULT_UNITS


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
    sequence: int = 0


@dataclass(frozen=True)
class CutList:
    """Structured cut list for CSV / PDF workshop export."""

    meta: CutListMeta
    panels: tuple[CutListPanel, ...]
    pieces: tuple[CutListPiece, ...]
    cuts: tuple[CutListCut, ...]
    sequences: tuple[PanelCutSequence, ...] = ()


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
        header = replace(header, kerf_mm=project.constraints.kerf_mm)

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

    sequences = build_cut_sequences(solution, project)
    numbers = piece_sequence_numbers(solution, project)
    cuts: list[CutListCut] = []
    for index, placement in enumerate(solution.placements):
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
                sequence=numbers.get(index, index + 1),
            )
        )
    cuts.sort(
        key=lambda item: (
            item.stock_panel_index,
            item.instance_index,
            item.sequence,
            item.piece_id,
        )
    )

    return CutList(
        meta=header,
        panels=tuple(panels),
        pieces=tuple(pieces),
        cuts=tuple(cuts),
        sequences=sequences,
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
                "sequence": cut.sequence,
            }
        )

    for panel in cut_list.sequences:
        for step in panel.steps:
            row = {
                "section": "saw",
                "id": step.piece_id or f"cut-{step.index}",
                "value": step.kind,
                "panel_id": panel.panel_id,
                "instance_index": panel.instance_index,
                "sequence": step.index,
                "length_mm": step.span_mm if step.span_mm is not None else "",
            }
            if step.axis == "x":
                row["x_mm"] = step.position_mm
            elif step.axis == "y":
                row["y_mm"] = step.position_mm
            writer.writerow(row)

    return buffer.getvalue()


def cut_list_to_pdf(cut_list: CutList) -> bytes:
    """Return a printable A4 PDF with the same sections as the CSV."""
    return pdf_from_text_lines(_report_lines(cut_list))


def render_cut_list(cut_list: CutList, fmt: str) -> str | bytes:
    """Render ``csv`` text or ``pdf`` bytes."""
    if normalize_cut_list_format(fmt) == "pdf":
        return cut_list_to_pdf(cut_list)
    return cut_list_to_csv(cut_list)


def _report_lines(cut_list: CutList) -> list[str]:
    meta = cut_list.meta
    units = normalize_units(meta.units)
    lines = [
        "Lista de corte — BoardComposer",
        "",
        f"Proyecto: {meta.project_name or '-'}",
        f"Cliente: {meta.client or '-'}",
        f"Referencia: {meta.reference or '-'}",
        f"Notas: {meta.notes or '-'}",
        f"Kerf ({report_unit_label(units)}): {report_length_label(meta.kerf_mm, units)}",
        "",
        "Tableros",
        "id  material  espesor  LxW  stock  usados",
    ]
    if not cut_list.panels:
        lines.append("(sin inventario de tableros)")
    for panel in cut_list.panels:
        lines.append(
            f"{panel.panel_id}  {panel.material}  "
            f"{report_length_label(panel.thickness_mm, units)}  "
            f"{report_size_label(panel.length_mm, panel.width_mm, units)}  "
            f"{panel.quantity}  {panel.instances_used}"
        )

    lines.extend(["", "Piezas", "id  material  espesor  LxW  omitida"])
    if not cut_list.pieces:
        lines.append("(sin piezas)")
    for piece in cut_list.pieces:
        omitted = "si" if piece.omitted else "no"
        lines.append(
            f"{piece.piece_id}  {piece.material}  "
            f"{report_length_label(piece.thickness_mm, units)}  "
            f"{report_size_label(piece.length_mm, piece.width_mm, units)}  "
            f"{omitted}"
        )

    lines.extend(["", "Cortes por tablero", "seq  pieza  panel#  LxW  rotada  x,y"])
    if not cut_list.cuts:
        lines.append("(sin cortes colocados)")
    for cut in cut_list.cuts:
        rotated = "si" if cut.rotated else "no"
        panel_label = f"{cut.panel_id}#{cut.instance_index + 1}"
        lines.append(
            f"{cut.sequence}  {cut.piece_id}  {panel_label}  "
            f"{report_size_label(cut.length_mm, cut.width_mm, units)}  "
            f"{rotated}  "
            f"{report_length_label(cut.x_mm, units)},"
            f"{report_length_label(cut.y_mm, units)}"
        )

    lines.extend(["", "Secuencia de sierra"])
    if not cut_list.sequences:
        lines.append("(sin secuencia)")
    for panel in cut_list.sequences:
        mode = "guillotina" if panel.guillotine else "orden por posicion"
        panel_label = f"{panel.panel_id}#{panel.instance_index + 1}"
        lines.append(f"{panel_label}  {mode}")
        if not panel.steps:
            lines.append("(sin pasos)")
            continue
        for step in panel.steps:
            lines.append(_saw_step_line(step, units))
    lines.extend(
        report_traceability_footer(
            include=meta.include_traceability,
            strategy_name=meta.strategy_name,
            version=meta.version,
            exported_at=meta.exported_at,
        )
    )
    return lines


def _saw_step_line(step: SequenceStep, units: str = DEFAULT_UNITS) -> str:
    if step.kind == "piece":
        return f"{step.index}. Pieza {step.piece_id}"
    axis = "horizontal" if step.axis == "y" else "vertical"
    if step.position_mm is None:
        position = "-"
    elif normalize_units(units) == DEFAULT_UNITS:
        position = f"{step.position_mm:g} mm"
    else:
        position = report_length_label(step.position_mm, units)
    span = "-" if step.span_mm is None else report_length_label(step.span_mm, units)
    return f"{step.index}. Corte {axis} a {position} (largo {span})"
