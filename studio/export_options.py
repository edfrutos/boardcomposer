"""Export options and rendering helpers for Studio (SCR-007)."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.export import (
    DEFAULT_PDF_MARGIN_MM,
    DEFAULT_PDF_ORIENTATION,
    DEFAULT_PDF_PAPER,
    DEFAULT_PDF_SCALE,
    PdfPageOptions,
    prepare_solution_for_export,
    solution_to_csv,
    solution_to_dxf,
    solution_to_json,
    solution_to_pdf,
    solution_to_svg,
)

VALID_EXPORT_FORMATS = ("svg", "png", "jpeg", "dxf", "pdf", "json", "csv")
DEFAULT_EXPORT_FORMAT = "svg"

MM_PER_INCH = 25.4
DEFAULT_RASTER_DPI = 96
MIN_RASTER_DPI = 36
MAX_RASTER_DPI = 300
DEFAULT_JPEG_QUALITY = 90
MIN_JPEG_QUALITY = 1
MAX_JPEG_QUALITY = 100
MAX_RASTER_EDGE_PX = 16384

_FORMAT_LABELS = {
    "svg": "SVG",
    "png": "PNG",
    "jpeg": "JPEG",
    "dxf": "DXF",
    "pdf": "PDF",
    "json": "JSON",
    "csv": "CSV",
}

_FORMAT_FILTERS = {
    "svg": "SVG (*.svg)",
    "png": "PNG (*.png)",
    "jpeg": "JPEG (*.jpg *.jpeg)",
    "dxf": "DXF (*.dxf)",
    "pdf": "PDF (*.pdf)",
    "json": "JSON (*.json)",
    "csv": "CSV (*.csv)",
}


@dataclass(frozen=True)
class ExportOptions:
    """User choices for exporting one solution."""

    format: str = DEFAULT_EXPORT_FORMAT
    include_metrics: bool = True
    include_explanation: bool = True
    include_offcuts: bool = True
    include_piece_labels: bool = True
    include_offcut_labels: bool = True
    include_panel_dimensions: bool = True
    pdf_paper: str = DEFAULT_PDF_PAPER
    pdf_orientation: str = DEFAULT_PDF_ORIENTATION
    pdf_scale: str = DEFAULT_PDF_SCALE
    pdf_margin_mm: float = DEFAULT_PDF_MARGIN_MM
    raster_dpi: int = DEFAULT_RASTER_DPI
    jpeg_quality: int = DEFAULT_JPEG_QUALITY
    export_batch: bool = False

    def normalized(self) -> ExportOptions:
        fmt = (
            self.format
            if self.format in VALID_EXPORT_FORMATS
            else DEFAULT_EXPORT_FORMAT
        )
        page = self.pdf_page()
        return ExportOptions(
            format=fmt,
            include_metrics=self.include_metrics,
            include_explanation=self.include_explanation,
            include_offcuts=self.include_offcuts,
            include_piece_labels=self.include_piece_labels,
            include_offcut_labels=self.include_offcut_labels,
            include_panel_dimensions=self.include_panel_dimensions,
            pdf_paper=page.paper,
            pdf_orientation=page.orientation,
            pdf_scale=page.scale,
            pdf_margin_mm=page.margin_mm,
            raster_dpi=normalize_raster_dpi(self.raster_dpi),
            jpeg_quality=normalize_jpeg_quality(self.jpeg_quality),
            export_batch=self.export_batch,
        )

    def pdf_page(self) -> PdfPageOptions:
        """Return plan-PDF page settings (ignored by other formats)."""
        return PdfPageOptions(
            paper=self.pdf_paper,
            orientation=self.pdf_orientation,
            scale=self.pdf_scale,
            margin_mm=self.pdf_margin_mm,
        ).normalized()

    @property
    def label(self) -> str:
        return _FORMAT_LABELS[self.normalized().format]

    @property
    def file_filter(self) -> str:
        return _FORMAT_FILTERS[self.normalized().format]

    @property
    def extension(self) -> str:
        return self.normalized().format


def normalize_raster_dpi(value: object) -> int:
    """Clamp PNG/JPEG resolution (dots per inch)."""
    try:
        dpi = int(round(float(value)))
    except (TypeError, ValueError):
        return DEFAULT_RASTER_DPI
    return max(MIN_RASTER_DPI, min(MAX_RASTER_DPI, dpi))


def normalize_jpeg_quality(value: object) -> int:
    """Clamp JPEG encoder quality (1–100)."""
    try:
        quality = int(round(float(value)))
    except (TypeError, ValueError):
        return DEFAULT_JPEG_QUALITY
    return max(MIN_JPEG_QUALITY, min(MAX_JPEG_QUALITY, quality))


def _plan_label_kwargs(options: ExportOptions) -> dict[str, bool]:
    return {
        "include_piece_labels": options.include_piece_labels,
        "include_offcut_labels": options.include_offcut_labels,
        "include_panel_dimensions": options.include_panel_dimensions,
    }


def format_label(fmt: str) -> str:
    return _FORMAT_LABELS.get(fmt, fmt.upper())


def prepare_solution(
    solution: AssemblySolution, options: ExportOptions
) -> AssemblySolution:
    """Return a solution filtered according to export options."""
    return prepare_solution_for_export(
        solution, include_offcuts=options.include_offcuts
    )


def render_export(
    solution: AssemblySolution,
    project: Project | None,
    options: ExportOptions,
    *,
    strategy_name: str | None = None,
    solution_index: int | None = None,
    material_prices: Mapping[str, float] | None = None,
) -> str | bytes:
    """Render the export payload (text or PDF bytes)."""
    options = options.normalized()
    prepared = prepare_solution(solution, options)

    if options.format == "svg":
        return solution_to_svg(prepared, project, **_plan_label_kwargs(options))
    if options.format in {"png", "jpeg"}:
        # Raster export is generated in Studio from this SVG payload.
        return solution_to_svg(prepared, project, **_plan_label_kwargs(options))
    if options.format == "dxf":
        return solution_to_dxf(prepared, project, **_plan_label_kwargs(options))
    if options.format == "pdf":
        return solution_to_pdf(
            prepared,
            project,
            **_plan_label_kwargs(options),
            page=options.pdf_page(),
        )
    if options.format == "csv":
        return solution_to_csv(prepared)
    return solution_to_json(
        prepared,
        project,
        strategy_name=strategy_name,
        solution_index=solution_index,
        include_metrics=options.include_metrics,
        include_explanation=options.include_explanation,
        include_offcuts=options.include_offcuts,
        material_prices=material_prices,
    )


def preview_svg(
    solution: AssemblySolution,
    project: Project | None,
    options: ExportOptions,
) -> str:
    """Return the layout SVG used for the graphical export preview."""
    options = options.normalized()
    prepared = prepare_solution(solution, options)
    return solution_to_svg(prepared, project, **_plan_label_kwargs(options))


def preview_text(
    solution: AssemblySolution,
    project: Project | None,
    options: ExportOptions,
    *,
    strategy_name: str | None = None,
    solution_index: int | None = None,
    material_prices: Mapping[str, float] | None = None,
    ranked_count: int = 1,
    max_chars: int = 4000,
) -> str:
    """Return a human-readable preview for the export dialog."""
    options = options.normalized()
    prepared = prepare_solution(solution, options)

    summary = [
        f"Formato: {options.label}",
        f"Piezas colocadas: {len(prepared.placements)}",
        f"Omitidas: {len(prepared.omitted_piece_ids)}",
        f"Retales: {len(prepared.offcuts)}",
        f"Completa: {'sí' if prepared.is_complete else 'no'}",
        f"Puntuación: {prepared.score.total:.2f}",
        "",
    ]
    if options.export_batch and ranked_count > 1:
        summary.append(
            f"Lote: {ranked_count} archivos "
            f"boardcomposer-solution-01.{options.extension} …"
        )
        summary.append("")

    if options.format in {"json", "csv"}:
        payload = render_export(
            solution,
            project,
            options,
            strategy_name=strategy_name,
            solution_index=solution_index,
            material_prices=material_prices,
        )
        assert isinstance(payload, str)
        body = payload if len(payload) <= max_chars else payload[:max_chars] + "\n…"
        return "\n".join(summary) + body

    if options.format == "svg":
        svg = solution_to_svg(prepared, project, **_plan_label_kwargs(options))
        summary.append(f"Tamaño SVG: {len(svg)} caracteres")
        summary.append("Arriba: vista previa gráfica del dibujo vectorial.")
        summary.append(
            "Etiquetas de piezas (id y LxW mm) incluidas."
            if options.include_piece_labels
            else "Sin etiquetas de piezas."
        )
        if options.include_offcuts:
            summary.append(
                "Etiquetas de retales (LxW mm) incluidas."
                if options.include_offcut_labels
                else "Sin etiquetas de retales."
            )
        summary.append(
            "Cotas L×A del tablero incluidas."
            if options.include_panel_dimensions
            else "Sin cotas de tablero."
        )
        return "\n".join(summary)

    summary.append(
        f"Se generará un archivo {options.label} con paneles, piezas"
        + (" y retales." if options.include_offcuts else " (sin retales).")
    )
    if options.format in {"svg", "png", "jpeg", "dxf", "pdf"}:
        summary.append(
            "Etiquetas de piezas (id y LxW mm) incluidas."
            if options.include_piece_labels
            else "Sin etiquetas de piezas."
        )
        if options.include_offcuts:
            summary.append(
                "Etiquetas de retales (LxW mm) incluidas."
                if options.include_offcut_labels
                else "Sin etiquetas de retales."
            )
        summary.append(
            "Cotas L×A del tablero incluidas."
            if options.include_panel_dimensions
            else "Sin cotas de tablero."
        )
    if options.format in {"dxf", "pdf"}:
        summary.append(
            "Arriba: vista previa del layout (misma geometría que el export)."
        )
    if options.format in {"png", "jpeg"}:
        summary.append(f"Resolución: {options.raster_dpi} DPI.")
        if options.format == "jpeg":
            summary.append(f"Calidad JPEG: {options.jpeg_quality}.")
    if options.format == "pdf":
        summary.append(
            f"Papel: {options.pdf_paper}; orientación: {options.pdf_orientation}; "
            f"escala: {options.pdf_scale}; margen: {options.pdf_margin_mm:g} mm."
        )
        if options.pdf_paper == "drawing":
            summary.append(
                "Página a tamaño del dibujo (1:1). Lista de corte y presupuesto "
                "siguen en A4 aparte."
            )
    return "\n".join(summary)
