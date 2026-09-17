"""Suggest a free gap on a panel for manual placement (IDE-0036).

Uses MaxRects free rectangles. Kerf is applied by occupying inflated
rects and searching for an inflated piece; the returned origin is the
actual (non-inflated) placement. Does not mutate the solver pipeline.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from boardcomposer.layout.kerf import aabb_overlap_with_kerf, inflate_size
from boardcomposer.solver.maxrects.maxrects import MaxRects
from boardcomposer.solver.maxrects.placement import MaxRectsPlacement

_EPS_MM = 1e-6


@dataclass(frozen=True)
class OccupiedRect:
    """Already-placed rectangle on the same physical panel."""

    x_mm: float
    y_mm: float
    length_mm: float
    width_mm: float


@dataclass(frozen=True)
class GapSuggestion:
    """A feasible origin for the piece on the panel."""

    x_mm: float
    y_mm: float
    length_mm: float
    width_mm: float
    rotated: bool = False


def suggest_gap(
    *,
    panel_length_mm: float,
    panel_width_mm: float,
    piece_length_mm: float,
    piece_width_mm: float,
    occupied: Sequence[OccupiedRect] = (),
    kerf_mm: float = 0.0,
    allow_rotation: bool = False,
    prefer_near: tuple[float, float] | None = None,
) -> GapSuggestion | None:
    """Return one free-rect origin that fits, or ``None``.

    ``prefer_near`` picks the closest origin to ``(x, y)`` (drop assist).
    Without it, Min waste then bottom-left (Ctrl+Alt+G).
    """
    if (
        panel_length_mm <= 0
        or panel_width_mm <= 0
        or piece_length_mm <= 0
        or piece_width_mm <= 0
    ):
        return None

    packer = MaxRects(panel_length_mm, panel_width_mm)
    for rect in occupied:
        packed_l, packed_w = inflate_size(rect.length_mm, rect.width_mm, kerf_mm)
        packer.occupy(rect.x_mm, rect.y_mm, packed_l, packed_w)

    packed_piece_l, packed_piece_w = inflate_size(
        piece_length_mm, piece_width_mm, kerf_mm
    )
    raw = packer.find_candidates(
        packed_piece_l,
        packed_piece_w,
        allow_rotation=allow_rotation,
    )
    viable = [
        candidate
        for candidate in raw
        if _candidate_fits(
            candidate,
            piece_length_mm=piece_length_mm,
            piece_width_mm=piece_width_mm,
            panel_length_mm=panel_length_mm,
            panel_width_mm=panel_width_mm,
            occupied=occupied,
            kerf_mm=kerf_mm,
        )
    ]
    if not viable:
        return None

    if prefer_near is None:
        chosen = min(
            viable,
            key=lambda candidate: (
                _waste_for(packer, candidate),
                candidate.y_mm,
                candidate.x_mm,
            ),
        )
    else:
        near_x, near_y = prefer_near
        chosen = min(
            viable,
            key=lambda candidate: (
                (candidate.x_mm - near_x) ** 2 + (candidate.y_mm - near_y) ** 2,
                _waste_for(packer, candidate),
                candidate.y_mm,
                candidate.x_mm,
            ),
        )

    length, width = _actual_size(chosen, piece_length_mm, piece_width_mm)
    return GapSuggestion(
        x_mm=chosen.x_mm,
        y_mm=chosen.y_mm,
        length_mm=length,
        width_mm=width,
        rotated=chosen.rotated,
    )


def _actual_size(
    candidate: MaxRectsPlacement,
    piece_length_mm: float,
    piece_width_mm: float,
) -> tuple[float, float]:
    if candidate.rotated:
        return piece_width_mm, piece_length_mm
    return piece_length_mm, piece_width_mm


def _candidate_fits(
    candidate: MaxRectsPlacement,
    *,
    piece_length_mm: float,
    piece_width_mm: float,
    panel_length_mm: float,
    panel_width_mm: float,
    occupied: Sequence[OccupiedRect],
    kerf_mm: float,
) -> bool:
    length, width = _actual_size(candidate, piece_length_mm, piece_width_mm)
    if candidate.x_mm + length > panel_length_mm + _EPS_MM:
        return False
    if candidate.y_mm + width > panel_width_mm + _EPS_MM:
        return False
    if candidate.x_mm < -_EPS_MM or candidate.y_mm < -_EPS_MM:
        return False
    for other in occupied:
        if aabb_overlap_with_kerf(
            candidate.x_mm,
            candidate.y_mm,
            length,
            width,
            other.x_mm,
            other.y_mm,
            other.length_mm,
            other.width_mm,
            kerf_mm,
        ):
            return False
    return True


def _waste_for(packer: MaxRects, candidate: MaxRectsPlacement) -> float:
    piece_area = candidate.length_mm * candidate.width_mm
    for rectangle in packer.free_rectangles:
        if (
            abs(rectangle.x_mm - candidate.x_mm) <= _EPS_MM
            and abs(rectangle.y_mm - candidate.y_mm) <= _EPS_MM
        ):
            return rectangle.area_mm2 - piece_area
    return float("inf")
