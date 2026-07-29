"""Tests for studio.units — mm storage vs display conversion/formatting."""

from studio.units import (
    DEFAULT_UNITS,
    VALID_UNITS,
    display_to_mm,
    format_length,
    format_size,
    mm_to_display,
    normalize_units,
    unit_label,
)


def test_valid_units_and_default():
    assert VALID_UNITS == ("mm", "cm", "in")
    assert DEFAULT_UNITS == "mm"


def test_normalize_units_known_and_fallback():
    assert normalize_units("mm") == "mm"
    assert normalize_units("cm") == "cm"
    assert normalize_units("in") == "in"
    assert normalize_units("px") == "mm"
    assert normalize_units("") == "mm"


def test_unit_label_follows_normalize():
    assert unit_label("mm") == "mm"
    assert unit_label("bogus") == "mm"


def test_mm_to_display_for_each_unit():
    assert mm_to_display(254, "mm") == 254.0
    assert mm_to_display(254, "cm") == 25.4
    assert mm_to_display(254, "in") == 10.0


def test_display_to_mm_round_trip_inches():
    assert abs(display_to_mm(mm_to_display(19, "in"), "in") - 19.0) < 1e-9


def test_format_length_mm_default_decimals():
    assert format_length(19, "mm") == "19 mm"
    assert format_length(19.5, "mm") == "19.5 mm"


def test_format_length_cm_and_in_trim_trailing_zeros():
    assert format_length(100, "cm") == "10 cm"
    assert format_length(25.4, "in") == "1 in"
    assert format_length(38.1, "in") == "1.5 in"


def test_format_length_explicit_decimals():
    assert format_length(10, "mm", decimals=2) == "10 mm"
    assert format_length(25.4, "in", decimals=3) == "1 in"


def test_format_size_without_thickness():
    assert format_size(3000, 1200, "mm") == "3000 x 1200 mm"


def test_format_size_with_thickness_in_inches():
    text = format_size(254, 127, "in", thickness_mm=25.4)
    assert text.endswith(" in")
    assert "10" in text
    assert "5" in text
    assert "1" in text
