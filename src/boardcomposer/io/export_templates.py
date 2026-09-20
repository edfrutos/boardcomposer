"""Headless reader for Studio export templates (SCR-007 / EP-002 SPR-002).

Compatible with ``~/.boardcomposer/export_templates.json`` and share packs
(``kind: boardcomposer.export_templates``). No Qt / Studio imports.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from boardcomposer.export.pdf_page import (
    DEFAULT_PDF_MARGIN_MM,
    DEFAULT_PDF_ORIENTATION,
    DEFAULT_PDF_PAPER,
    DEFAULT_PDF_SCALE,
    PdfPageOptions,
)

VALID_TEMPLATE_FORMATS = ("svg", "dxf", "pdf", "json", "csv")


def default_export_templates_path() -> Path:
    return Path.home() / ".boardcomposer" / "export_templates.json"


def normalize_client(client: str | None) -> str:
    return (client or "").strip()


@dataclass(frozen=True)
class NamedExportTemplate:
    """Named export options snapshot (client-scoped)."""

    name: str
    format: str
    include_metrics: bool = True
    include_explanation: bool = True
    include_offcuts: bool = True
    include_piece_labels: bool = True
    include_offcut_labels: bool = True
    include_panel_dimensions: bool = True
    include_plan_traceability: bool = True
    pdf_paper: str = DEFAULT_PDF_PAPER
    pdf_orientation: str = DEFAULT_PDF_ORIENTATION
    pdf_scale: str = DEFAULT_PDF_SCALE
    pdf_margin_mm: float = DEFAULT_PDF_MARGIN_MM
    export_batch: bool = False
    client: str = ""

    @property
    def key(self) -> tuple[str, str]:
        return (self.client.casefold(), self.name.casefold())

    @classmethod
    def from_dict(cls, payload: dict) -> NamedExportTemplate | None:
        name = str(payload.get("name", "")).strip()
        if not name:
            return None
        fmt = str(payload.get("format", "svg")).strip().lower()
        if fmt not in VALID_TEMPLATE_FORMATS:
            fmt = "svg"
        page = PdfPageOptions(
            paper=str(payload.get("pdf_paper", DEFAULT_PDF_PAPER)),
            orientation=str(payload.get("pdf_orientation", DEFAULT_PDF_ORIENTATION)),
            scale=str(payload.get("pdf_scale", DEFAULT_PDF_SCALE)),
            margin_mm=payload.get("pdf_margin_mm", DEFAULT_PDF_MARGIN_MM),
        ).normalized()
        return cls(
            name=name,
            format=fmt,
            include_metrics=bool(payload.get("include_metrics", True)),
            include_explanation=bool(payload.get("include_explanation", True)),
            include_offcuts=bool(payload.get("include_offcuts", True)),
            include_piece_labels=bool(payload.get("include_piece_labels", True)),
            include_offcut_labels=bool(payload.get("include_offcut_labels", True)),
            include_panel_dimensions=bool(
                payload.get("include_panel_dimensions", True)
            ),
            include_plan_traceability=bool(
                payload.get("include_plan_traceability", True)
            ),
            pdf_paper=page.paper,
            pdf_orientation=page.orientation,
            pdf_scale=page.scale,
            pdf_margin_mm=page.margin_mm,
            export_batch=bool(payload.get("export_batch", False)),
            client=normalize_client(str(payload.get("client", ""))),
        )


def parse_export_templates_payload(payload: object) -> list[NamedExportTemplate]:
    """Parse a Studio catalog (list) or share pack (dict)."""
    if isinstance(payload, dict):
        raw = payload.get("templates", [])
        if not isinstance(raw, list):
            return []
        items = raw
    elif isinstance(payload, list):
        items = payload
    else:
        return []

    templates: list[NamedExportTemplate] = []
    seen: set[tuple[str, str]] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        template = NamedExportTemplate.from_dict(item)
        if template is None or template.key in seen:
            continue
        seen.add(template.key)
        templates.append(template)
    templates.sort(key=lambda item: (item.client.casefold(), item.name.casefold()))
    return templates


def load_export_templates(path: str | Path | None = None) -> list[NamedExportTemplate]:
    """Load templates from ``path`` (default: user Studio catalog)."""
    catalog = Path(path) if path is not None else default_export_templates_path()
    if not catalog.is_file():
        return []
    try:
        payload = json.loads(catalog.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return parse_export_templates_payload(payload)


def find_export_template(
    name: str,
    *,
    client: str = "",
    path: str | Path | None = None,
) -> NamedExportTemplate | None:
    """Return the template matching ``client`` + ``name`` (case-insensitive)."""
    wanted = (normalize_client(client).casefold(), name.strip().casefold())
    if not wanted[1]:
        return None
    for template in load_export_templates(path):
        if template.key == wanted:
            return template
    return None
