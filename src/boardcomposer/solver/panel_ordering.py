"""Ordering strategies for physical stock-panel instances.

Analogous to `board_ordering.py`, but for the order in which physical
panels are offered to the packer, rather than the order pieces are
offered within a panel.
"""

from boardcomposer.domain import PanelReference, StockPanel

PanelInstance = tuple[PanelReference, StockPanel]


def original_order(panels: tuple[PanelInstance, ...]) -> list[PanelInstance]:
    """Keep the order declared by the project (current default behavior)."""
    return list(panels)


def largest_area_first(panels: tuple[PanelInstance, ...]) -> list[PanelInstance]:
    return sorted(
        panels,
        key=lambda item: (
            item[1].length_mm * item[1].width_mm,
            item[1].length_mm,
            item[1].width_mm,
        ),
        reverse=True,
    )


def smallest_area_first(panels: tuple[PanelInstance, ...]) -> list[PanelInstance]:
    return sorted(
        panels,
        key=lambda item: (
            item[1].length_mm * item[1].width_mm,
            item[1].length_mm,
            item[1].width_mm,
        ),
    )


PANEL_ORDERINGS = (
    ("original", original_order),
    ("largest_area", largest_area_first),
    ("smallest_area", smallest_area_first),
)
