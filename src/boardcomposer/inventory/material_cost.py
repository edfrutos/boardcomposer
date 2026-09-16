"""Estimated stock-sheet cost from catalog prices (IDE-0029).

Carpenters pay for consumed physical panels, not just placed piece area.
Prices are €/m² keyed by material name (case-insensitive).
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from boardcomposer.domain.project import Project
from boardcomposer.domain.solution import AssemblySolution

MM2_PER_M2 = 1_000_000.0


@dataclass(frozen=True)
class MaterialCostEstimate:
    """Cost of consumed stock panels using a price map."""

    total: float = 0.0
    priced_area_m2: float = 0.0
    unpriced_area_m2: float = 0.0
    missing_materials: tuple[str, ...] = ()

    @property
    def has_price(self) -> bool:
        return self.priced_area_m2 > 0


def normalize_price_map(prices: Mapping[str, float]) -> dict[str, float]:
    """Keep positive rates, keyed by casefolded material name."""
    cleaned: dict[str, float] = {}
    for name, value in prices.items():
        key = str(name).strip().casefold()
        if not key:
            continue
        try:
            rate = float(value)
        except (TypeError, ValueError):
            continue
        if rate > 0:
            cleaned[key] = rate
    return cleaned


def estimated_material_cost(
    solution: AssemblySolution,
    project: Project,
    prices: Mapping[str, float],
) -> MaterialCostEstimate:
    """Return the € cost of every physical panel the solution consumes."""
    lookup = normalize_price_map(prices)
    total = 0.0
    priced = 0.0
    unpriced = 0.0
    missing: list[str] = []
    seen_missing: set[str] = set()

    for reference in solution.panel_references:
        panel = project.stock_panel_for(reference)
        if panel is None:
            continue
        area_m2 = panel.area_mm2 / MM2_PER_M2
        rate = lookup.get(panel.material_key)
        if rate is None:
            unpriced += area_m2
            label = panel.material.strip() or panel.material_key
            if label.casefold() not in seen_missing:
                seen_missing.add(label.casefold())
                missing.append(label)
            continue
        priced += area_m2
        total += area_m2 * rate

    return MaterialCostEstimate(
        total=round(total, 2),
        priced_area_m2=round(priced, 6),
        unpriced_area_m2=round(unpriced, 6),
        missing_materials=tuple(missing),
    )
