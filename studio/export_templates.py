"""Named export option templates for Studio (SCR-007)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from studio.export_options import ExportOptions


def default_export_templates_path() -> Path:
    return Path.home() / ".boardcomposer" / "export_templates.json"


@dataclass(frozen=True)
class ExportTemplate:
    """A named snapshot of export options."""

    name: str
    options: ExportOptions

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "format": self.options.format,
            "include_metrics": self.options.include_metrics,
            "include_explanation": self.options.include_explanation,
            "include_offcuts": self.options.include_offcuts,
        }

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
        return cls(name=name, options=options)


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

    def names(self) -> list[str]:
        return [template.name for template in self.templates]

    def get(self, name: str) -> ExportTemplate | None:
        for template in self.templates:
            if template.name == name:
                return template
        return None

    def save_template(self, name: str, options: ExportOptions) -> ExportTemplate:
        """Insert or replace a template by name and persist."""
        cleaned = name.strip()
        if not cleaned:
            raise ValueError("El nombre de la plantilla no puede estar vacío")

        template = ExportTemplate(name=cleaned, options=options.normalized())
        self.templates = [
            existing for existing in self.templates if existing.name != cleaned
        ]
        self.templates.append(template)
        self.templates.sort(key=lambda item: item.name.casefold())
        self.save()
        return template

    def delete(self, name: str) -> bool:
        before = len(self.templates)
        self.templates = [
            template for template in self.templates if template.name != name
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
        seen: set[str] = set()
        for item in payload:
            if not isinstance(item, dict):
                continue
            template = ExportTemplate.from_dict(item)
            if template is None or template.name in seen:
                continue
            seen.add(template.name)
            templates.append(template)
        templates.sort(key=lambda item: item.name.casefold())
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
