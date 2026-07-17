"""Tests for Industrial madera workspace canvas colors."""

from PySide6.QtGui import QColor

from studio.models import StudioBoard
from studio.theme import apply_theme
from studio.theme_tokens import DARK_CANVAS, LIGHT_CANVAS, canvas_colors_for
from studio.workspace.board_item import create_board_item
from studio.workspace.board_piece_item import BoardPieceItem
from studio.workspace.canvas_style import active_canvas, set_active_canvas_theme
from studio.workspace.selection import apply_selection


def test_canvas_colors_for_system_defaults_to_light():
    assert canvas_colors_for("system") == LIGHT_CANVAS
    assert canvas_colors_for("light") == LIGHT_CANVAS
    assert canvas_colors_for("dark") == DARK_CANVAS


def test_apply_theme_updates_active_canvas(qapp):
    apply_theme(qapp, "dark")
    assert active_canvas() == DARK_CANVAS
    apply_theme(qapp, "light")
    assert active_canvas() == LIGHT_CANVAS
    apply_theme(qapp, "system")
    assert active_canvas() == LIGHT_CANVAS


def test_board_and_piece_use_canvas_tokens(qapp):
    del qapp
    set_active_canvas_theme("light")
    board = create_board_item(StudioBoard("B1", 100, 50, "Demo", 18, 1))
    assert board.brush().color().name() == QColor(LIGHT_CANVAS.board_fill).name()
    assert board.pen().color().name() == QColor(LIGHT_CANVAS.board_stroke).name()

    piece = BoardPieceItem("P1", 0, 0, 40, 20)
    assert piece.brush().color().name() == QColor(LIGHT_CANVAS.piece_fill).name()
    assert piece.pen().color().name() == QColor(LIGHT_CANVAS.piece_stroke).name()

    apply_selection(piece, True)
    assert piece.brush().color().name() == QColor(LIGHT_CANVAS.selected_fill).name()
    assert piece.pen().color().name() == QColor(LIGHT_CANVAS.selected_stroke).name()

    piece.set_valid()
    assert piece.brush().color().name() == QColor(LIGHT_CANVAS.valid_fill).name()
    piece.set_invalid()
    assert piece.brush().color().name() == QColor(LIGHT_CANVAS.invalid_fill).name()


def test_dark_canvas_piece_colors(qapp):
    del qapp
    set_active_canvas_theme("dark")
    piece = BoardPieceItem("P1", 0, 0, 40, 20)
    assert piece.brush().color().name() == QColor(DARK_CANVAS.piece_fill).name()
    assert piece.pen().color().name() == QColor(DARK_CANVAS.piece_stroke).name()
