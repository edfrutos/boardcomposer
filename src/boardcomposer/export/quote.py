"""Material quote PDF (IDE-0032) with optional report footer (IDE-0043).

Does not change the solver. Cost matches IDE-0029 (physical panels, not
placed piece area). Helvetica PDF stays latin-1, so currency is ``EUR``.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.export.common import report_traceability_footer
from boardcomposer.export.report_pdf import pdf_from_text_lines
from boardcomposer.inventory.material_cost import (
    MM2_PER_M2,
    MaterialCostEstimate,
    estimated_material_cost,
    normalize_price_map,
)


@dataclass(frozen=True)
class QuoteMeta:
    """Optional project header printed on the quote."""

    project_name: str = ""
    client: str = ""
    reference: str = ""
    notes: str = ""
    include_traceability: bool = True
    strategy_name: str = ""
    version: str | None = None
    exported_at: str | None = None


@dataclass(frozen=True)
class QuoteLine:
    """One consumed physical panel on the quote."""

    panel_id: str
    instance_index: int
    material: str
    length_mm: float
    width_mm: float
    thickness_mm: float
    area_m2: float
    price_per_m2: float | None
    cost: float

    @property
    def priced(self) -> bool:
        return self.price_per_m2 is not None


@dataclass(frozen=True)
class QuoteReport:
    """Structured material quote for PDF export."""

    meta: QuoteMeta
    lines: tuple[QuoteLine, ...]
    estimate: MaterialCostEstimate
    placed_count: int
    omitted_ids: tuple[str, ...]


def build_quote(
    solution: AssemblySolution,
    project: Project | None,
    prices: Mapping[str, float],
    meta: QuoteMeta | None = None,
) -> QuoteReport:
    """Build a quote from consumed panels of ``solution``."""
    header = meta or QuoteMeta()
    if project is None:
        return QuoteReport(
            meta=header,
            lines=(),
            estimate=MaterialCostEstimate(),
            placed_count=len(solution.placements),
            omitted_ids=solution.omitted_piece_ids,
        )

    lookup = normalize_price_map(prices)
    lines: list[QuoteLine] = []
    for reference in solution.panel_references:
        panel = project.stock_panel_for(reference)
        if panel is None:
            continue
        area_m2 = round(panel.area_mm2 / MM2_PER_M2, 6)
        rate = lookup.get(panel.material_key)
        priced = rate is not None
        cost = round(area_m2 * rate, 2) if priced else 0.0
        lines.append(
            QuoteLine(
                panel_id=panel.id or f"panel-{reference.stock_panel_index + 1}",
                instance_index=reference.instance_index,
                material=panel.material,
                length_mm=panel.length_mm,
                width_mm=panel.width_mm,
                thickness_mm=panel.thickness_mm,
                area_m2=area_m2,
                price_per_m2=rate,
                cost=cost,
            )
        )

    return QuoteReport(
        meta=header,
        lines=tuple(lines),
        estimate=estimated_material_cost(solution, project, prices),
        placed_count=len(solution.placements),
        omitted_ids=solution.omitted_piece_ids,
    )


def quote_to_pdf(report: QuoteReport) -> bytes:
    """Return a printable A4 PDF of the material quote."""
    return pdf_from_text_lines(_report_lines(report))


def _money(value: float) -> str:
    return f"{value:.2f} EUR"


def _rate(value: float | None) -> str:
    return f"{value:.2f}" if value is not None else "-"


def _report_lines(report: QuoteReport) -> list[str]:
    meta = report.meta
    estimate = report.estimate
    omitted = ", ".join(report.omitted_ids) if report.omitted_ids else "-"
    total = _money(estimate.total) if estimate.has_price else "-"
    if estimate.has_price and estimate.unpriced_area_m2 > 0:
        total = f"{total} *"

    lines = [
        "Presupuesto de material — BoardComposer",
        "",
        f"Proyecto: {meta.project_name or '-'}",
        f"Cliente: {meta.client or '-'}",
        f"Referencia: {meta.reference or '-'}",
        f"Notas: {meta.notes or '-'}",
        "",
        "Tableros consumidos",
        "panel  material  LxW  espesor  m2  EUR/m2  coste",
    ]
    if not report.lines:
        lines.append("(sin tableros consumidos)")
    for item in report.lines:
        cost = _money(item.cost) if item.priced else "-"
        lines.append(
            f"{item.panel_id}#{item.instance_index + 1}  {item.material}  "
            f"{item.length_mm:g}x{item.width_mm:g}  {item.thickness_mm:g}  "
            f"{item.area_m2:.3f}  {_rate(item.price_per_m2)}  {cost}"
        )

    missing = ", ".join(estimate.missing_materials) or "-"
    lines.extend(
        [
            "",
            f"Total material: {total}",
            f"Area con precio: {estimate.priced_area_m2:.3f} m2",
            f"Area sin precio: {estimate.unpriced_area_m2:.3f} m2",
            f"Materiales sin precio: {missing}",
            "",
            f"Piezas colocadas: {report.placed_count}",
            f"Piezas omitidas: {omitted}",
            "",
            "El coste es el de tableros fisicos consumidos (catalogo EUR/m2).",
            "No incluye mano de obra ni herrajes. No cambia el packing.",
        ]
    )
    lines.extend(
        report_traceability_footer(
            include=meta.include_traceability,
            strategy_name=meta.strategy_name,
            version=meta.version,
            exported_at=meta.exported_at,
        )
    )
    return lines
