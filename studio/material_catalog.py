"""User-level material / thickness catalog (IDE-0028).

Stored outside `.bcproj` so every project can reuse the same typed stock
names. Optional: the catalog learns new pairs when the user accepts a
board or piece dialog.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


def default_material_catalog_path() -> Path:
    return Path.home() / ".boardcomposer" / "material_catalog.json"


def normalize_thickness(value: float) -> float:
    """Round to 0.1 mm so 19.0000001 matches 19."""
    return round(float(value), 1)


@dataclass(frozen=True)
class CatalogMaterial:
    """Named material with typical thicknesses in millimetres."""

    name: str
    thicknesses_mm: tuple[float, ...] = ()

    def __post_init__(self) -> None:
        cleaned = self.name.strip()
        if not cleaned:
            raise ValueError("el nombre del material no puede estar vacío")
        thicknesses = tuple(
            sorted(
                {normalize_thickness(item) for item in self.thicknesses_mm if item > 0}
            )
        )
        object.__setattr__(self, "name", cleaned)
        object.__setattr__(self, "thicknesses_mm", thicknesses)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "thicknesses_mm": list(self.thicknesses_mm),
        }

    @classmethod
    def from_dict(cls, payload: dict) -> CatalogMaterial | None:
        name = str(payload.get("name", "")).strip()
        if not name:
            return None
        raw = payload.get("thicknesses_mm", ())
        if not isinstance(raw, (list, tuple)):
            raw = ()
        thicknesses = []
        for item in raw:
            try:
                thicknesses.append(float(item))
            except (TypeError, ValueError):
                continue
        return cls(name=name, thicknesses_mm=tuple(thicknesses))


DEFAULT_CATALOG_MATERIALS: tuple[CatalogMaterial, ...] = (
    CatalogMaterial("Melamina blanca", (16.0, 19.0, 22.0)),
    CatalogMaterial("MDF", (16.0, 19.0, 22.0, 30.0)),
    CatalogMaterial("Contrachapado", (12.0, 15.0, 18.0)),
    CatalogMaterial("Demo", (19.0,)),
)


def default_catalog() -> "MaterialCatalog":
    """In-memory seed used when no user file exists yet."""
    catalog = MaterialCatalog()
    catalog.replace_all(list(DEFAULT_CATALOG_MATERIALS))
    return catalog


def in_memory_catalog() -> "MaterialCatalogManager":
    """Defaults only; tests and StudioServices must not touch ~/.boardcomposer."""
    return MaterialCatalogManager(autoload=False)


@dataclass
class MaterialCatalog:
    """Editable list of catalog materials (not persisted by itself)."""

    materials: list[CatalogMaterial] = field(default_factory=list)

    def names(self) -> list[str]:
        return [item.name for item in self.materials]

    def find(self, name: str) -> CatalogMaterial | None:
        key = name.strip().casefold()
        if not key:
            return None
        for item in self.materials:
            if item.name.casefold() == key:
                return item
        return None

    def thicknesses_for(self, name: str) -> tuple[float, ...]:
        found = self.find(name)
        return found.thicknesses_mm if found else ()

    def remember(self, name: str, thickness_mm: float) -> bool:
        """Add a material/thickness pair. Return True if the catalog changed."""
        cleaned = name.strip()
        if not cleaned:
            return False
        thickness = normalize_thickness(thickness_mm)
        if thickness <= 0:
            return False
        existing = self.find(cleaned)
        if existing is None:
            self.materials.append(
                CatalogMaterial(name=cleaned, thicknesses_mm=(thickness,))
            )
            self.materials.sort(key=lambda item: item.name.casefold())
            return True
        if thickness in existing.thicknesses_mm:
            return False
        updated = CatalogMaterial(
            name=existing.name,
            thicknesses_mm=existing.thicknesses_mm + (thickness,),
        )
        index = self.materials.index(existing)
        self.materials[index] = updated
        return True

    def replace_all(self, materials: list[CatalogMaterial]) -> None:
        seen: set[str] = set()
        cleaned: list[CatalogMaterial] = []
        for item in materials:
            key = item.name.casefold()
            if key in seen:
                continue
            seen.add(key)
            cleaned.append(item)
        cleaned.sort(key=lambda item: item.name.casefold())
        self.materials = cleaned

    def to_payload(self) -> dict:
        return {
            "version": 1,
            "materials": [item.to_dict() for item in self.materials],
        }

    @classmethod
    def from_payload(cls, payload: object) -> MaterialCatalog:
        if isinstance(payload, list):
            items = payload
        elif isinstance(payload, dict):
            items = payload.get("materials", [])
        else:
            items = []
        materials: list[CatalogMaterial] = []
        if isinstance(items, list):
            for raw in items:
                if not isinstance(raw, dict):
                    continue
                parsed = CatalogMaterial.from_dict(raw)
                if parsed is not None:
                    materials.append(parsed)
        catalog = cls()
        catalog.replace_all(materials)
        return catalog


@dataclass
class MaterialCatalogManager:
    """Load and save the user catalog from a JSON file."""

    catalog: MaterialCatalog = field(default_factory=default_catalog)
    path: Path | None = None
    autoload: bool = True

    def __post_init__(self) -> None:
        if self.path is None and self.autoload:
            self.path = default_material_catalog_path()
        if self.autoload:
            self.load()

    def names(self) -> list[str]:
        return self.catalog.names()

    def thicknesses_for(self, name: str) -> tuple[float, ...]:
        return self.catalog.thicknesses_for(name)

    def remember(self, name: str, thickness_mm: float) -> bool:
        changed = self.catalog.remember(name, thickness_mm)
        if changed:
            self.save()
        return changed

    def replace_all(self, materials: list[CatalogMaterial]) -> None:
        self.catalog.replace_all(materials)
        self.save()

    def restore_defaults(self) -> None:
        self.replace_all(list(DEFAULT_CATALOG_MATERIALS))

    def load(self) -> None:
        if self.path is None or not self.path.is_file():
            self.catalog = default_catalog()
            return
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            self.catalog = default_catalog()
            return
        loaded = MaterialCatalog.from_payload(payload)
        if loaded.materials:
            self.catalog = loaded
        else:
            self.catalog = default_catalog()

    def save(self) -> None:
        if self.path is None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self.catalog.to_payload(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
