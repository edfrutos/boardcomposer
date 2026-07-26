"""Headless reader for Studio export templates (SCR-007 / EP-002 SPR-002).

Compatible with ``~/.boardcomposer/export_templates.json`` and share packs
(``kind: boardcomposer.export_templates``). No Qt / Studio imports.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

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
        return cls(
            name=name,
            format=fmt,
            include_metrics=bool(payload.get("include_metrics", True)),
            include_explanation=bool(payload.get("include_explanation", True)),
            include_offcuts=bool(payload.get("include_offcuts", True)),
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
