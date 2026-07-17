"""Tests for display units and language preferences (SCR-006)."""

from studio.i18n import tr
from studio.preferences import PreferencesManager, StudioPreferences
from studio.units import display_to_mm, format_size, mm_to_display


def test_mm_cm_inch_round_trip():
    assert mm_to_display(1000, "cm") == 100
    assert display_to_mm(100, "cm") == 1000
    assert abs(display_to_mm(1, "in") - 25.4) < 1e-9


def test_format_size_uses_selected_unit():
    assert format_size(3000, 1200, "mm", thickness_mm=19) == "3000 x 1200 x 19 mm"
    assert "cm" in format_size(1000, 500, "cm")


def test_tr_switches_language():
    assert tr("welcome.new", "es") == "Nuevo proyecto"
    assert tr("welcome.new", "en") == "New project"


def test_tr_formats_interpolated_values():
    assert tr("inspector.placed", "en", n=3) == "Pieces placed: 3"
    assert tr("menu.file", "en") == "File"
    assert tr("action.solve_layout", "en") == "Calculate layout"
    assert tr("inspector.none", "en") == "No selection"


def test_preferences_persist_language_and_units(tmp_path):
    path = tmp_path / "preferences.json"
    manager = PreferencesManager(path)
    manager.update(StudioPreferences(language="en", units="in"))

    reloaded = PreferencesManager(path).current

    assert reloaded.language == "en"
    assert reloaded.units == "in"
