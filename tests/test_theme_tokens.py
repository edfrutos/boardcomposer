"""Tests for studio.theme_tokens — UI and canvas palettes."""

from studio.theme_tokens import (
    DARK,
    DARK_CANVAS,
    LIGHT,
    LIGHT_CANVAS,
    TOKENS_BY_NAME,
    canvas_colors_for,
    tokens_for,
)


def test_tokens_for_light_and_dark():
    assert tokens_for("light") is LIGHT
    assert tokens_for("dark") is DARK


def test_tokens_for_system_and_unknown_return_none():
    assert tokens_for("system") is None
    assert tokens_for("unknown") is None
    assert tokens_for("") is None


def test_tokens_by_name_covers_both_modes():
    assert set(TOKENS_BY_NAME) == {"light", "dark"}
    assert TOKENS_BY_NAME["light"] is LIGHT
    assert TOKENS_BY_NAME["dark"] is DARK


def test_light_and_dark_share_font_families():
    assert LIGHT.font_ui == DARK.font_ui == "Source Sans 3"
    assert LIGHT.font_brand == DARK.font_brand == "Archivo SemiBold"


def test_accent_text_is_dark_ink_on_both_modes():
    # WCAG ink on amber — same dark ink for light and dark chrome
    assert LIGHT.accent_text == DARK.accent_text == "#1a1410"


def test_canvas_colors_for_known_and_fallback():
    assert canvas_colors_for("light") is LIGHT_CANVAS
    assert canvas_colors_for("dark") is DARK_CANVAS
    assert canvas_colors_for("system") is LIGHT_CANVAS
    assert canvas_colors_for("nope") is LIGHT_CANVAS


def test_canvas_palettes_differ_between_modes():
    assert LIGHT_CANVAS.background != DARK_CANVAS.background
    assert LIGHT_CANVAS.piece_fill != DARK_CANVAS.piece_fill
    assert LIGHT_CANVAS.selected_stroke != DARK_CANVAS.selected_stroke
