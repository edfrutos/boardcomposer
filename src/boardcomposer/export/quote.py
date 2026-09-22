"""Material quote PDF (IDE-0032) with optional labor (IDE-0045).

Does not change the solver. Material cost matches IDE-0029 (physical
panels, not placed piece area). Labor is shop prefs: EUR/h x minutes
per placed piece. PDF TEXT sizes follow ``meta.units`` (IDE-0048);
area stays m2. Helvetica PDF stays latin-1, so currency is ``EUR``.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.export.common import (
    report_length_label,
    report_size_label,
    report_traceability_footer,
)
from boardcomposer.units import DEFAULT_UNITS, normalize_units
from boardcomposer.export.report_pdf import pdf_from_text_lines
from boardcomposer.inventory.material_cost import (
    MM2_PER_M2,
    MaterialCostEstimate,
    estimated_material_cost,
    normalize_price_map,
)

DEFAULT_LABOR_EUR_PER_HOUR = 0.0
MAX_LABOR_EUR_PER_HOUR = 999.0
DEFAULT_LABOR_MINUTES_PER_PIECE = 0.0
MAX_LABOR_MINUTES_PER_PIECE = 180.0


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
    labor_rate_eur_per_hour: float = DEFAULT_LABOR_EUR_PER_HOUR
    labor_minutes_per_piece: float = DEFAULT_LABOR_MINUTES_PER_PIECE
    units: str = DEFAULT_UNITS


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
    labor_hours: float = 0.0
    labor_cost: float = 0.0

    @property
    def has_labor(self) -> bool:
        return self.labor_cost > 0

    @property
    def grand_total(self) -> float:
        material = self.estimate.total if self.estimate.has_price else 0.0
        return round(material + self.labor_cost, 2)


def normalize_labor_rate(value: object) -> float:
    """Clamp a shop hourly rate to ``0…999`` EUR/h."""
    try:
        rate = float(value)
    except (TypeError, ValueError):
        return DEFAULT_LABOR_EUR_PER_HOUR
    return max(0.0, min(MAX_LABOR_EUR_PER_HOUR, round(rate, 2)))


def normalize_labor_minutes(value: object) -> float:
    """Clamp minutes per placed piece to ``0…180``."""
    try:
        minutes = float(value)
    except (TypeError, ValueError):
        return DEFAULT_LABOR_MINUTES_PER_PIECE
    return max(0.0, min(MAX_LABOR_MINUTES_PER_PIECE, round(minutes, 1)))


def quote_labor_hours(placed_count: int, minutes_per_piece: float) -> float:
    """Return hours for ``placed_count`` pieces at ``minutes_per_piece``."""
    minutes = normalize_labor_minutes(minutes_per_piece)
    count = max(0, int(placed_count))
    if minutes <= 0 or count <= 0:
        return 0.0
    return round(count * minutes / 60.0, 4)


def quote_labor_cost(hours: float, rate: float) -> float:
    """Return EUR for ``hours`` at ``rate`` EUR/h."""
    hourly = normalize_labor_rate(rate)
    if hours <= 0 or hourly <= 0:
        return 0.0
    return round(float(hours) * hourly, 2)


def build_quote(
    solution: AssemblySolution,
    project: Project | None,
    prices: Mapping[str, float],
    meta: QuoteMeta | None = None,
) -> QuoteReport:
    """Build a quote from consumed panels of ``solution``."""
    header = meta or QuoteMeta()
    placed = len(solution.placements)
    hours = quote_labor_hours(placed, header.labor_minutes_per_piece)
    labor = quote_labor_cost(hours, header.labor_rate_eur_per_hour)
    if project is None:
        return QuoteReport(
            meta=header,
            lines=(),
            estimate=MaterialCostEstimate(),
            placed_count=placed,
            omitted_ids=solution.omitted_piece_ids,
            labor_hours=hours,
            labor_cost=labor,
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
        placed_count=placed,
        omitted_ids=solution.omitted_piece_ids,
        labor_hours=hours,
        labor_cost=labor,
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
    units = normalize_units(meta.units)
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
            f"{report_size_label(item.length_mm, item.width_mm, units)}  "
            f"{report_length_label(item.thickness_mm, units)}  "
            f"{item.area_m2:.3f}  {_rate(item.price_per_m2)}  {cost}"
        )

    missing = ", ".join(estimate.missing_materials) or "-"
    rate = normalize_labor_rate(meta.labor_rate_eur_per_hour)
    minutes = normalize_labor_minutes(meta.labor_minutes_per_piece)
    totals = [
        "",
        f"Total material: {total}",
    ]
    if report.has_labor:
        totals.append(
            f"Mano de obra: {report.placed_count} x {minutes:g} min x "
            f"{rate:.2f} EUR/h = {_money(report.labor_cost)}"
        )
        totals.append(f"Total: {_money(report.grand_total)}")
    totals.extend(
        [
            f"Area con precio: {estimate.priced_area_m2:.3f} m2",
            f"Area sin precio: {estimate.unpriced_area_m2:.3f} m2",
            f"Materiales sin precio: {missing}",
            "",
            f"Piezas colocadas: {report.placed_count}",
            f"Piezas omitidas: {omitted}",
            "",
            "El coste de material es el de tableros fisicos consumidos "
            "(catalogo EUR/m2).",
        ]
    )
    if report.has_labor:
        totals.append(
            "La mano de obra estima piezas colocadas x minutos x tarifa. "
            "No incluye herrajes."
        )
    else:
        totals.append("No incluye mano de obra ni herrajes. No cambia el packing.")
    if report.has_labor:
        totals.append("No cambia el packing.")
    lines.extend(totals)
    lines.extend(
        report_traceability_footer(
            include=meta.include_traceability,
            strategy_name=meta.strategy_name,
            version=meta.version,
            exported_at=meta.exported_at,
        )
    )
    return lines
