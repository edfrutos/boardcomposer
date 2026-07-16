from boardcomposer import PanelReference, StockPanel
from boardcomposer.solver.panel_ordering import (
    PANEL_ORDERINGS,
    largest_area_first,
    original_order,
    smallest_area_first,
)


def _instances(*panels: StockPanel):
    return tuple(
        (PanelReference(index, 0), panel) for index, panel in enumerate(panels)
    )


def test_original_order_keeps_declared_order():
    panels = _instances(
        StockPanel(1000, 300, 19, "B"),
        StockPanel(2500, 600, 19, "A"),
    )

    assert [panel.id for _, panel in original_order(panels)] == ["B", "A"]


def test_largest_area_first_orders_by_panel_area_descending():
    panels = _instances(
        StockPanel(1000, 300, 19, "B"),
        StockPanel(2500, 600, 19, "A"),
        StockPanel(800, 250, 19, "C"),
    )

    assert [panel.id for _, panel in largest_area_first(panels)] == ["A", "B", "C"]


def test_smallest_area_first_orders_by_panel_area_ascending():
    panels = _instances(
        StockPanel(1000, 300, 19, "B"),
        StockPanel(2500, 600, 19, "A"),
        StockPanel(800, 250, 19, "C"),
    )

    assert [panel.id for _, panel in smallest_area_first(panels)] == ["C", "B", "A"]


def test_panel_orderings_preserves_panel_references():
    panels = _instances(
        StockPanel(1000, 300, 19, "B"),
        StockPanel(2500, 600, 19, "A"),
    )

    reordered = largest_area_first(panels)

    assert {reference for reference, _ in reordered} == {
        reference for reference, _ in panels
    }


def test_panel_orderings_registry_has_the_expected_names():
    assert [name for name, _ in PANEL_ORDERINGS] == [
        "original",
        "largest_area",
        "smallest_area",
    ]
