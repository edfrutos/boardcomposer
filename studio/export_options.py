"""Export options and rendering helpers for Studio (SCR-007)."""

from __future__ import annotations

from dataclasses import dataclass

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.export import (
    prepare_solution_for_export,
    solution_to_csv,
    solution_to_dxf,
    solution_to_json,
    solution_to_pdf,
    solution_to_svg,
)

VALID_EXPORT_FORMATS = ("svg", "png", "jpeg", "dxf", "pdf", "json", "csv")
DEFAULT_EXPORT_FORMAT = "svg"

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

    def normalized(self) -> ExportOptions:
        fmt = (
            self.format
            if self.format in VALID_EXPORT_FORMATS
            else DEFAULT_EXPORT_FORMAT
        )
        return ExportOptions(
            format=fmt,
            include_metrics=self.include_metrics,
            include_explanation=self.include_explanation,
            include_offcuts=self.include_offcuts,
        )

    @property
    def label(self) -> str:
        return _FORMAT_LABELS[self.normalized().format]

    @property
    def file_filter(self) -> str:
        return _FORMAT_FILTERS[self.normalized().format]

    @property
    def extension(self) -> str:
        return self.normalized().format


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
) -> str | bytes:
    """Render the export payload (text or PDF bytes)."""
    options = options.normalized()
    prepared = prepare_solution(solution, options)

    if options.format == "svg":
        return solution_to_svg(prepared, project)
    if options.format in {"png", "jpeg"}:
        # Raster export is generated in Studio from this SVG payload.
        return solution_to_svg(prepared, project)
    if options.format == "dxf":
        return solution_to_dxf(prepared, project)
    if options.format == "pdf":
        return solution_to_pdf(prepared, project)
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
    )


def preview_svg(
    solution: AssemblySolution,
    project: Project | None,
    options: ExportOptions,
) -> str:
    """Return the layout SVG used for the graphical export preview."""
    options = options.normalized()
    prepared = prepare_solution(solution, options)
    return solution_to_svg(prepared, project)


def preview_text(
    solution: AssemblySolution,
    project: Project | None,
    options: ExportOptions,
    *,
    strategy_name: str | None = None,
    solution_index: int | None = None,
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

    if options.format in {"json", "csv"}:
        payload = render_export(
            solution,
            project,
            options,
            strategy_name=strategy_name,
            solution_index=solution_index,
        )
        assert isinstance(payload, str)
        body = payload if len(payload) <= max_chars else payload[:max_chars] + "\n…"
        return "\n".join(summary) + body

    if options.format == "svg":
        svg = solution_to_svg(prepared, project)
        summary.append(f"Tamaño SVG: {len(svg)} caracteres")
        summary.append("Arriba: vista previa gráfica del dibujo vectorial.")
        return "\n".join(summary)

    summary.append(
        f"Se generará un archivo {options.label} con paneles, piezas"
        + (" y retales." if options.include_offcuts else " (sin retales).")
    )
    if options.format in {"dxf", "pdf"}:
        summary.append(
            "Arriba: vista previa del layout (misma geometría que el export)."
        )
    return "\n".join(summary)
