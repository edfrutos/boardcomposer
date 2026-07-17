"""Shared SVG color palette (Industrial madera, light / printable)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SvgPalette:
    """Colors for SVG export and Studio thumbnails."""

    background: str
    panel_fill: str
    panel_stroke: str
    piece_fill: str
    piece_stroke: str
    piece_label: str
    offcut_stroke: str
    legend: str


# Mirrors studio LIGHT_CANVAS so export / thumbnails match the workspace.
DEFAULT_SVG_PALETTE = SvgPalette(
    background="#e8ddd0",
    panel_fill="#faf6f0",
    panel_stroke="#2c241c",
    piece_fill="#edd5a8",
    piece_stroke="#a86512",
    piece_label="#2c241c",
    offcut_stroke="#3d6b2e",
    legend="#b42318",
)
