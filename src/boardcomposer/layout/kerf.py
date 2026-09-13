"""Kerf (saw-kerf) helpers for packing and collision (IDE-0020)."""

from __future__ import annotations

from dataclasses import replace

from boardcomposer.domain.placement import BoardPlacement
from boardcomposer.domain.project import Project
from boardcomposer.domain.solution import AssemblySolution

DEFAULT_KERF_MM = 0.0
MAX_KERF_MM = 50.0


def normalize_kerf(value: object) -> float:
    """Clamp kerf to ``[0, MAX_KERF_MM]``; invalid input becomes 0."""
    try:
        kerf = float(value)
    except (TypeError, ValueError):
        return DEFAULT_KERF_MM
    if kerf < 0:
        return DEFAULT_KERF_MM
    if kerf > MAX_KERF_MM:
        return MAX_KERF_MM
    return kerf


def inflate_size(
    length_mm: float, width_mm: float, kerf_mm: float
) -> tuple[float, float]:
    """Add kerf to the right and bottom of a rectangle."""
    kerf = normalize_kerf(kerf_mm)
    return length_mm + kerf, width_mm + kerf


def aabb_overlap(
    ax: float,
    ay: float,
    aw: float,
    ah: float,
    bx: float,
    by: float,
    bw: float,
    bh: float,
) -> bool:
    """True when two AABBs overlap in area (touching edges is allowed)."""
    return not (ax + aw <= bx or bx + bw <= ax or ay + ah <= by or by + bh <= ay)


def aabb_overlap_with_kerf(
    ax: float,
    ay: float,
    aw: float,
    ah: float,
    bx: float,
    by: float,
    bw: float,
    bh: float,
    kerf_mm: float,
) -> bool:
    """Overlap test that enforces one shared ``kerf_mm`` gap between AABBs."""
    kerf = normalize_kerf(kerf_mm)
    return aabb_overlap(ax, ay, aw + kerf, ah + kerf, bx, by, bw + kerf, bh + kerf)


def inflate_project_for_kerf(project: Project) -> Project:
    """Copy ``project`` with piece and panel sizes grown by kerf."""
    kerf = normalize_kerf(project.constraints.kerf_mm)
    if kerf == 0:
        return project

    constraints = project.constraints
    max_length = constraints.max_length_mm
    max_width = constraints.max_width_mm
    inflated_constraints = replace(
        constraints,
        max_length_mm=None if max_length is None else max_length + kerf,
        max_width_mm=None if max_width is None else max_width + kerf,
    )
    inflated = Project(constraints=inflated_constraints)
    for panel in project.stock_panels:
        length, width = inflate_size(panel.length_mm, panel.width_mm, kerf)
        inflated.add_stock_panel(replace(panel, length_mm=length, width_mm=width))
    for board in project.boards:
        length, width = inflate_size(board.length_mm, board.width_mm, kerf)
        inflated.add_board(replace(board, length_mm=length, width_mm=width))
    return inflated


def deflate_placement(placement: BoardPlacement, kerf_mm: float) -> BoardPlacement:
    """Restore actual piece size after packing with inflated dimensions."""
    kerf = normalize_kerf(kerf_mm)
    if kerf == 0:
        return placement
    length = max(placement.length_mm - kerf, 1e-6)
    width = max(placement.width_mm - kerf, 1e-6)
    return replace(placement, length_mm=length, width_mm=width)


def deflate_solution(solution: AssemblySolution, kerf_mm: float) -> AssemblySolution:
    """Restore actual placement sizes on a packed solution."""
    kerf = normalize_kerf(kerf_mm)
    if kerf == 0:
        return solution
    return replace(
        solution,
        placements=[deflate_placement(item, kerf) for item in solution.placements],
    )
