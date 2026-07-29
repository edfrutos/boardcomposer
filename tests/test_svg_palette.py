"""Tests for SVG export palette contract with Studio canvas colors."""

from boardcomposer.export.svg_palette import DEFAULT_SVG_PALETTE
from studio.theme_tokens import LIGHT_CANVAS


def test_default_svg_palette_mirrors_light_canvas():
    """Export / thumbnails stay aligned with the light workspace canvas."""
    assert DEFAULT_SVG_PALETTE.background == LIGHT_CANVAS.background
    assert DEFAULT_SVG_PALETTE.panel_fill == LIGHT_CANVAS.board_fill
    assert DEFAULT_SVG_PALETTE.panel_stroke == LIGHT_CANVAS.board_stroke
    assert DEFAULT_SVG_PALETTE.piece_fill == LIGHT_CANVAS.piece_fill
    assert DEFAULT_SVG_PALETTE.piece_stroke == LIGHT_CANVAS.piece_stroke
    assert DEFAULT_SVG_PALETTE.piece_label == LIGHT_CANVAS.piece_label
    assert DEFAULT_SVG_PALETTE.offcut_stroke == LIGHT_CANVAS.valid_stroke
    assert DEFAULT_SVG_PALETTE.legend == LIGHT_CANVAS.selected_stroke
