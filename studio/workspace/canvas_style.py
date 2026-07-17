"""Active canvas color helpers for the Studio workspace."""

from __future__ import annotations

from PySide6.QtGui import QColor, QPen

from studio.theme_tokens import LIGHT_CANVAS, CanvasColors, canvas_colors_for

_active: CanvasColors = LIGHT_CANVAS


def set_active_canvas_theme(theme: str) -> None:
    """Update the canvas palette used when building workspace items."""
    global _active
    _active = canvas_colors_for(theme)


def active_canvas() -> CanvasColors:
    """Return the currently active canvas color tokens."""
    return _active


def color(name: str) -> QColor:
    """Resolve a `CanvasColors` field name to `QColor`."""
    return QColor(getattr(_active, name))


def pen(name: str, width: int) -> QPen:
    """Build a pen from a canvas stroke token."""
    return QPen(color(name), width)
