"""Named export option templates / client profiles for Studio (SCR-007)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from studio.export_options import ExportOptions


def default_export_templates_path() -> Path:
    return Path.home() / ".boardcomposer" / "export_templates.json"


def normalize_client(client: str | None) -> str:
    return (client or "").strip()


@dataclass(frozen=True)
class ExportTemplate:
    """A named snapshot of export options, optionally scoped to a client."""

    name: str
    options: ExportOptions
    client: str = ""

    @property
    def key(self) -> tuple[str, str]:
        return (self.client.casefold(), self.name.casefold())

    def display_label(self, *, general_label: str = "") -> str:
        if self.client:
            return f"{self.client} — {self.name}"
        if general_label:
            return f"{general_label} — {self.name}"
        return self.name

    def to_dict(self) -> dict:
        payload = {
            "name": self.name,
            "format": self.options.format,
            "include_metrics": self.options.include_metrics,
            "include_explanation": self.options.include_explanation,
            "include_offcuts": self.options.include_offcuts,
        }
        if self.client:
            payload["client"] = self.client
        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> ExportTemplate | None:
        name = str(payload.get("name", "")).strip()
        if not name:
            return None
        options = ExportOptions(
            format=str(payload.get("format", "svg")),
            include_metrics=bool(payload.get("include_metrics", True)),
            include_explanation=bool(payload.get("include_explanation", True)),
            include_offcuts=bool(payload.get("include_offcuts", True)),
        ).normalized()
        client = normalize_client(str(payload.get("client", "")))
        return cls(name=name, options=options, client=client)


@dataclass
class ExportTemplatesManager:
    """Load and save named export templates from a JSON file."""

    templates: list[ExportTemplate] = field(default_factory=list)
    path: Path | None = None
    autoload: bool = True

    def __post_init__(self) -> None:
        if self.path is None and self.autoload:
            self.path = default_export_templates_path()
        if self.autoload and not self.templates:
            self.load()

    def clients(self) -> list[str]:
        """Return sorted unique client names (excluding the empty/general bucket)."""
        names = {template.client for template in self.templates if template.client}
        return sorted(names, key=str.casefold)

    def names(self, client: str | None = None) -> list[str]:
        """Return template names, optionally filtered by client.

        `client=None` returns every template name (legacy helper).
        `client=""` returns only general (no-client) templates.
        """
        if client is None:
            return [template.name for template in self.templates]
        wanted = normalize_client(client)
        return [
            template.name for template in self.templates if template.client == wanted
        ]

    def templates_for(self, client: str | None = None) -> list[ExportTemplate]:
        if client is None:
            return list(self.templates)
        wanted = normalize_client(client)
        return [template for template in self.templates if template.client == wanted]

    def get(self, name: str, client: str = "") -> ExportTemplate | None:
        wanted = (normalize_client(client).casefold(), name.strip().casefold())
        for template in self.templates:
            if template.key == wanted:
                return template
        return None

    def save_template(
        self,
        name: str,
        options: ExportOptions,
        *,
        client: str = "",
    ) -> ExportTemplate:
        """Insert or replace a template by client+name and persist."""
        cleaned = name.strip()
        if not cleaned:
            raise ValueError("El nombre de la plantilla no puede estar vacío")

        client_name = normalize_client(client)
        template = ExportTemplate(
            name=cleaned,
            options=options.normalized(),
            client=client_name,
        )
        self.templates = [
            existing for existing in self.templates if existing.key != template.key
        ]
        self.templates.append(template)
        self.templates.sort(
            key=lambda item: (item.client.casefold(), item.name.casefold())
        )
        self.save()
        return template

    def delete(self, name: str, client: str = "") -> bool:
        wanted = (normalize_client(client).casefold(), name.strip().casefold())
        before = len(self.templates)
        self.templates = [
            template for template in self.templates if template.key != wanted
        ]
        if len(self.templates) == before:
            return False
        self.save()
        return True

    def load(self) -> None:
        if self.path is None or not self.path.is_file():
            self.templates = []
            return
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            self.templates = []
            return
        if not isinstance(payload, list):
            self.templates = []
            return

        templates: list[ExportTemplate] = []
        seen: set[tuple[str, str]] = set()
        for item in payload:
            if not isinstance(item, dict):
                continue
            template = ExportTemplate.from_dict(item)
            if template is None or template.key in seen:
                continue
            seen.add(template.key)
            templates.append(template)
        templates.sort(key=lambda item: (item.client.casefold(), item.name.casefold()))
        self.templates = templates

    def save(self) -> None:
        if self.path is None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [template.to_dict() for template in self.templates]
        self.path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
