import pytest

from boardcomposer import StockPanel


def test_stock_panel_area():
    panel = StockPanel(3000, 1200, 19, "P1")

    assert panel.area_mm2 == 3_600_000


@pytest.mark.parametrize(
    "kwargs",
    [
        {"length_mm": 0, "width_mm": 1200, "thickness_mm": 19},
        {"length_mm": 3000, "width_mm": 0, "thickness_mm": 19},
        {"length_mm": 3000, "width_mm": 1200, "thickness_mm": 0},
        {
            "length_mm": 3000,
            "width_mm": 1200,
            "thickness_mm": 19,
            "quantity": 0,
        },
    ],
)
def test_stock_panel_rejects_invalid_values(kwargs):
    with pytest.raises(ValueError):
        StockPanel(**kwargs)
