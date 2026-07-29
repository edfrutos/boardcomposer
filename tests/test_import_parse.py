"""Tests for studio.import_parse — shared CSV numeric parsers."""

from studio.import_parse import parse_positive_float, parse_positive_int


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
