import pytest

from boardcomposer import Offcut, PanelReference


def test_offcut_area():
    offcut = Offcut(
        panel_reference=PanelReference(0, 0),
        x_mm=400,
        y_mm=0,
        length_mm=600,
        width_mm=1000,
    )

    assert offcut.area_mm2 == 600_000


def test_offcut_rejects_negative_position():
    with pytest.raises(ValueError):
        Offcut(
            panel_reference=PanelReference(0, 0),
            x_mm=-1,
            y_mm=0,
            length_mm=100,
            width_mm=100,
        )


def test_offcut_rejects_non_positive_dimensions():
    with pytest.raises(ValueError):
        Offcut(
            panel_reference=PanelReference(0, 0),
            x_mm=0,
            y_mm=0,
            length_mm=0,
            width_mm=100,
        )
