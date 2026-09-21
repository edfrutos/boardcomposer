"""User-level material / thickness / sheet-size catalog (IDE-0028/0031/0042).

Stored outside `.bcproj` so every project can reuse the same typed stock
names. Optional: the catalog learns new pairs when the user accepts a
board or piece dialog. Share via JSON export/import (no cloud).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


CATALOG_PACK_KIND = "boardcomposer.material_catalog"


def default_material_catalog_path() -> Path:
    return Path.home() / ".boardcomposer" / "material_catalog.json"


def normalize_thickness(value: float) -> float:
    """Round to 0.1 mm so 19.0000001 matches 19."""
    return round(float(value), 1)


def normalize_size(length_mm: float, width_mm: float) -> tuple[float, float] | None:
    """Return a positive L×W pair rounded to 0.1 mm, or None."""
    try:
        length = normalize_thickness(length_mm)
        width = normalize_thickness(width_mm)
    except (TypeError, ValueError):
        return None
    if length <= 0 or width <= 0:
        return None
    return (length, width)


def format_catalog_size(length_mm: float, width_mm: float) -> str:
    """Human L×W label without units (2800×2070)."""

    def _fmt(value: float) -> str:
        return str(int(value) if value == int(value) else value)

    return f"{_fmt(length_mm)}×{_fmt(width_mm)}"


def _normalize_sizes(
    sizes: tuple[tuple[float, float], ...],
) -> tuple[tuple[float, float], ...]:
    cleaned: list[tuple[float, float]] = []
    seen: set[tuple[float, float]] = set()
    for raw in sizes:
        if not isinstance(raw, (list, tuple)) or len(raw) < 2:
            continue
        pair = normalize_size(raw[0], raw[1])
        if pair is None or pair in seen:
            continue
        seen.add(pair)
        cleaned.append(pair)
    return tuple(cleaned)


@dataclass(frozen=True)
class CatalogMaterial:
    """Named material with thicknesses, optional €/m² and typical L×W."""

    name: str
    thicknesses_mm: tuple[float, ...] = ()
    price_per_m2: float = 0.0
    sizes_mm: tuple[tuple[float, float], ...] = ()

    def __post_init__(self) -> None:
        cleaned = self.name.strip()
        if not cleaned:
            raise ValueError("el nombre del material no puede estar vacío")
        thicknesses = tuple(
            sorted(
                {normalize_thickness(item) for item in self.thicknesses_mm if item > 0}
            )
        )
        try:
            price = max(0.0, round(float(self.price_per_m2), 2))
        except (TypeError, ValueError):
            price = 0.0
        object.__setattr__(self, "name", cleaned)
        object.__setattr__(self, "thicknesses_mm", thicknesses)
        object.__setattr__(self, "price_per_m2", price)
        object.__setattr__(self, "sizes_mm", _normalize_sizes(self.sizes_mm))

    def to_dict(self) -> dict:
        payload = {
            "name": self.name,
            "thicknesses_mm": list(self.thicknesses_mm),
        }
        if self.price_per_m2 > 0:
            payload["price_per_m2"] = self.price_per_m2
        if self.sizes_mm:
            payload["sizes_mm"] = [list(pair) for pair in self.sizes_mm]
        return payload

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
        price = 0.0
        raw_price = payload.get("price_per_m2", 0)
        try:
            price = float(raw_price)
        except (TypeError, ValueError):
            price = 0.0
        sizes: list[tuple[float, float]] = []
        raw_sizes = payload.get("sizes_mm", ())
        if isinstance(raw_sizes, (list, tuple)):
            for item in raw_sizes:
                if not isinstance(item, (list, tuple)) or len(item) < 2:
                    continue
                try:
                    sizes.append((float(item[0]), float(item[1])))
                except (TypeError, ValueError):
                    continue
        return cls(
            name=name,
            thicknesses_mm=tuple(thicknesses),
            price_per_m2=price,
            sizes_mm=tuple(sizes),
        )


_EURO_SHEET: tuple[tuple[float, float], ...] = (
    (2800.0, 2070.0),
    (2440.0, 1220.0),
)

DEFAULT_CATALOG_MATERIALS: tuple[CatalogMaterial, ...] = (
    CatalogMaterial("Melamina blanca", (16.0, 19.0, 22.0), sizes_mm=_EURO_SHEET),
    CatalogMaterial("MDF", (16.0, 19.0, 22.0, 30.0), sizes_mm=_EURO_SHEET),
    CatalogMaterial(
        "Contrachapado",
        (12.0, 15.0, 18.0),
        sizes_mm=((2500.0, 1250.0), (2440.0, 1220.0)),
    ),
    CatalogMaterial("Demo", (19.0,), sizes_mm=((2800.0, 2070.0),)),
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

    def sizes_for(self, name: str) -> tuple[tuple[float, float], ...]:
        found = self.find(name)
        return found.sizes_mm if found else ()

    def price_for(self, name: str) -> float:
        found = self.find(name)
        return found.price_per_m2 if found else 0.0

    def price_map(self) -> dict[str, float]:
        return {
            item.name.casefold(): item.price_per_m2
            for item in self.materials
            if item.price_per_m2 > 0
        }

    def remember(
        self,
        name: str,
        thickness_mm: float,
        *,
        length_mm: float | None = None,
        width_mm: float | None = None,
    ) -> bool:
        """Add a material/thickness and optional L×W. True if catalog changed."""
        cleaned = name.strip()
        if not cleaned:
            return False
        thickness = normalize_thickness(thickness_mm)
        if thickness <= 0:
            return False
        size = None
        if length_mm is not None and width_mm is not None:
            size = normalize_size(length_mm, width_mm)
        existing = self.find(cleaned)
        if existing is None:
            sizes = (size,) if size is not None else ()
            self.materials.append(
                CatalogMaterial(
                    name=cleaned,
                    thicknesses_mm=(thickness,),
                    sizes_mm=sizes,
                )
            )
            self.materials.sort(key=lambda item: item.name.casefold())
            return True
        thicknesses = existing.thicknesses_mm
        sizes = existing.sizes_mm
        changed = False
        if thickness not in thicknesses:
            thicknesses = thicknesses + (thickness,)
            changed = True
        if size is not None and size not in sizes:
            sizes = sizes + (size,)
            changed = True
        if not changed:
            return False
        updated = CatalogMaterial(
            name=existing.name,
            thicknesses_mm=thicknesses,
            price_per_m2=existing.price_per_m2,
            sizes_mm=sizes,
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

    def sizes_for(self, name: str) -> tuple[tuple[float, float], ...]:
        return self.catalog.sizes_for(name)

    def price_map(self) -> dict[str, float]:
        return self.catalog.price_map()

    def remember(
        self,
        name: str,
        thickness_mm: float,
        *,
        length_mm: float | None = None,
        width_mm: float | None = None,
    ) -> bool:
        changed = self.catalog.remember(
            name,
            thickness_mm,
            length_mm=length_mm,
            width_mm=width_mm,
        )
        if changed:
            self.save()
        return changed

    def replace_all(self, materials: list[CatalogMaterial]) -> None:
        self.catalog.replace_all(materials)
        self.save()

    def restore_defaults(self) -> None:
        self.replace_all(list(DEFAULT_CATALOG_MATERIALS))

    def export_pack(self, path: Path | str) -> int:
        """Write the catalog to a shareable JSON pack. Returns count exported."""
        destination = Path(path)
        payload = {
            **self.catalog.to_payload(),
            "kind": CATALOG_PACK_KIND,
        }
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return len(self.catalog.materials)

    @staticmethod
    def parse_pack(payload: object) -> MaterialCatalog:
        """Parse a pack, a user catalog file, or a legacy bare list."""
        kind = payload.get("kind") if isinstance(payload, dict) else None
        if kind is not None and kind != CATALOG_PACK_KIND:
            raise ValueError("El archivo no es un catálogo de materiales BoardComposer")
        catalog = MaterialCatalog.from_payload(payload)
        if not catalog.materials and kind != CATALOG_PACK_KIND:
            raise ValueError("El paquete no contiene materiales")
        return catalog

    def import_pack(
        self,
        path: Path | str,
        *,
        mode: str = "merge",
    ) -> tuple[int, int]:
        """Import materials from a JSON pack.

        `mode="merge"` upserts by name (incoming wins).
        `mode="replace"` replaces the whole catalog.

        Returns `(imported_count, total_after)`.
        """
        source = Path(path)
        try:
            payload = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"No se pudo leer el paquete: {exc}") from exc

        incoming = self.parse_pack(payload)
        if mode == "replace":
            self.replace_all(list(incoming.materials))
        else:
            by_key = {item.name.casefold(): item for item in self.catalog.materials}
            for item in incoming.materials:
                by_key[item.name.casefold()] = item
            self.replace_all(list(by_key.values()))
        return len(incoming.materials), len(self.catalog.materials)

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
