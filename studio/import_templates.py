"""Named column-mapping templates for CSV/Excel import (FLW-002)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from studio.import_headers import missing_required_fields, sanitize_header_map

VALID_IMPORT_KINDS = ("boards", "pieces")


def default_import_templates_path() -> Path:
    return Path.home() / ".boardcomposer" / "import_templates.json"


def normalize_kind(kind: str) -> str:
    cleaned = kind.strip().casefold()
    if cleaned not in VALID_IMPORT_KINDS:
        raise ValueError(f"Tipo de importación no válido: {kind}")
    return cleaned


@dataclass(frozen=True)
class ImportMappingTemplate:
    """A named header map for boards or pieces import."""

    name: str
    kind: str
    header_map: dict[str, str]

    @property
    def key(self) -> tuple[str, str]:
        return (self.kind, self.name.casefold())

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "kind": self.kind,
            "header_map": dict(self.header_map),
        }

    @classmethod
    def from_dict(cls, payload: dict) -> ImportMappingTemplate | None:
        name = str(payload.get("name", "")).strip()
        kind_raw = str(payload.get("kind", "")).strip()
        raw_map = payload.get("header_map", {})
        if not name or not kind_raw or not isinstance(raw_map, dict):
            return None
        try:
            kind = normalize_kind(kind_raw)
        except ValueError:
            return None
        header_map = {
            str(canonical).strip(): str(header).strip()
            for canonical, header in raw_map.items()
            if str(canonical).strip() and str(header).strip()
        }
        if not header_map:
            return None
        return cls(name=name, kind=kind, header_map=header_map)


@dataclass
class ImportTemplatesManager:
    """Load and save named import column-mapping templates."""

    templates: list[ImportMappingTemplate] = field(default_factory=list)
    path: Path | None = None
    autoload: bool = True

    def __post_init__(self) -> None:
        if self.path is None and self.autoload:
            self.path = default_import_templates_path()
        if self.autoload and not self.templates:
            self.load()

    def for_kind(self, kind: str) -> list[ImportMappingTemplate]:
        wanted = normalize_kind(kind)
        return [template for template in self.templates if template.kind == wanted]

    def names(self, kind: str) -> list[str]:
        return [template.name for template in self.for_kind(kind)]

    def get(self, kind: str, name: str) -> ImportMappingTemplate | None:
        wanted = (normalize_kind(kind), name.strip().casefold())
        for template in self.templates:
            if template.key == wanted:
                return template
        return None

    def save_template(
        self,
        kind: str,
        name: str,
        header_map: dict[str, str],
    ) -> ImportMappingTemplate:
        cleaned = name.strip()
        if not cleaned:
            raise ValueError("El nombre de la plantilla no puede estar vacío")
        mapping = {
            str(canonical).strip(): str(header).strip()
            for canonical, header in header_map.items()
            if str(canonical).strip() and str(header).strip()
        }
        if not mapping:
            raise ValueError("El mapeo de columnas no puede estar vacío")

        template = ImportMappingTemplate(
            name=cleaned,
            kind=normalize_kind(kind),
            header_map=mapping,
        )
        self.templates = [
            existing for existing in self.templates if existing.key != template.key
        ]
        self.templates.append(template)
        self.templates.sort(key=lambda item: (item.kind, item.name.casefold()))
        self.save()
        return template

    def delete(self, kind: str, name: str) -> bool:
        wanted = (normalize_kind(kind), name.strip().casefold())
        before = len(self.templates)
        self.templates = [
            template for template in self.templates if template.key != wanted
        ]
        if len(self.templates) == before:
            return False
        self.save()
        return True

    def find_applicable(
        self,
        kind: str,
        fieldnames: list[str] | tuple[str, ...],
        required_fields: tuple[str, ...] | list[str],
    ) -> ImportMappingTemplate | None:
        """Return the best saved template that covers required fields."""
        best: ImportMappingTemplate | None = None
        best_score = -1
        for template in self.for_kind(kind):
            sanitized = sanitize_header_map(template.header_map, fieldnames)
            if missing_required_fields(sanitized, required_fields):
                continue
            score = len(sanitized)
            if score > best_score:
                best = template
                best_score = score
        return best

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

        templates: list[ImportMappingTemplate] = []
        seen: set[tuple[str, str]] = set()
        for item in payload:
            if not isinstance(item, dict):
                continue
            template = ImportMappingTemplate.from_dict(item)
            if template is None or template.key in seen:
                continue
            seen.add(template.key)
            templates.append(template)
        templates.sort(key=lambda item: (item.kind, item.name.casefold()))
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
