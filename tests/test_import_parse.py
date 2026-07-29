"""Tests for studio.import_parse — shared CSV numeric parsers."""

from studio.import_parse import (
    DEFAULT_IMPORT_MATERIAL,
    DEFAULT_IMPORT_QUANTITY,
    DEFAULT_IMPORT_THICKNESS_MM,
    optional_positive_float,
    optional_positive_int,
    optional_string,
    parse_positive_float,
    parse_positive_int,
)


def test_parse_positive_float_accepts_dot_and_comma():
    errors: list[str] = []
    assert parse_positive_float("19.5", "Espesor", errors) == 19.5
    assert parse_positive_float("1,5", "Espesor", errors) == 1.5
    assert errors == []


def test_parse_positive_float_rejects_zero_negative_and_garbage():
    errors: list[str] = []
    assert parse_positive_float("0", "Largo", errors) is None
    assert parse_positive_float("-3", "Largo", errors) is None
    assert parse_positive_float("abc", "Largo", errors) is None
    assert parse_positive_float("", "Largo", errors) is None
    assert len(errors) == 4
    assert "mayor que cero" in errors[0]
    assert "mayor que cero" in errors[1]
    assert "no es un número válido" in errors[2]
    assert "no es un número válido" in errors[3]


def test_parse_positive_int_accepts_int_and_float_strings():
    errors: list[str] = []
    assert parse_positive_int("3", "Cantidad", errors) == 3
    assert parse_positive_int("2.0", "Cantidad", errors) == 2
    assert errors == []


def test_parse_positive_int_rejects_zero_negative_and_garbage():
    errors: list[str] = []
    assert parse_positive_int("0", "Cantidad", errors) is None
    assert parse_positive_int("-1", "Cantidad", errors) is None
    assert parse_positive_int("x", "Cantidad", errors) is None
    assert len(errors) == 3
    assert "mayor que cero" in errors[0]
    assert "mayor que cero" in errors[1]
    assert "entero válido" in errors[2]


def test_optional_positive_float_uses_default_when_missing_or_blank():
    errors: list[str] = []
    assert (
        optional_positive_float({}, {}, "thickness_mm", "Espesor", 19.0, errors) == 19.0
    )
    assert (
        optional_positive_float(
            {"e": ""},
            {"thickness_mm": "e"},
            "thickness_mm",
            "Espesor",
            19.0,
            errors,
        )
        == 19.0
    )
    assert errors == []


def test_optional_positive_float_parses_value_and_keeps_default_on_invalid():
    errors: list[str] = []
    assert (
        optional_positive_float(
            {"e": "18,5"},
            {"thickness_mm": "e"},
            "thickness_mm",
            "Espesor",
            19.0,
            errors,
        )
        == 18.5
    )
    assert (
        optional_positive_float(
            {"e": "0"},
            {"thickness_mm": "e"},
            "thickness_mm",
            "Espesor",
            19.0,
            errors,
        )
        == 19.0
    )
    assert len(errors) == 1
    assert "mayor que cero" in errors[0]


def test_optional_positive_int_and_optional_string_defaults():
    errors: list[str] = []
    assert (
        optional_positive_int(
            {"q": "4"},
            {"quantity": "q"},
            "quantity",
            "Cantidad",
            DEFAULT_IMPORT_QUANTITY,
            errors,
        )
        == 4
    )
    assert (
        optional_string({}, {}, "material", DEFAULT_IMPORT_MATERIAL)
        == DEFAULT_IMPORT_MATERIAL
    )
    assert (
        optional_string(
            {"m": "Roble"},
            {"material": "m"},
            "material",
            DEFAULT_IMPORT_MATERIAL,
        )
        == "Roble"
    )
    assert DEFAULT_IMPORT_THICKNESS_MM == 19.0
    assert errors == []
