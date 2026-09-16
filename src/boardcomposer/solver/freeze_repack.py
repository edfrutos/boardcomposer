"""Freeze accepted placements and re-pack omitted pieces (IDE-0030)."""

from __future__ import annotations

from dataclasses import replace

from boardcomposer.domain import (
    AssemblySolution,
    Board,
    BoardPlacement,
    Offcut,
    PanelReference,
    Project,
    SolutionExplanation,
    StockPanel,
)
from boardcomposer.domain.grain import rotation_allowed
from boardcomposer.layout.kerf import (
    deflate_placement,
    inflate_project_for_kerf,
    inflate_size,
    normalize_kerf,
)
from boardcomposer.solver.maxrects.heuristics import best_area_fit
from boardcomposer.solver.maxrects.maxrects import MaxRects
from boardcomposer.solver.solution_evaluator import SolutionEvaluator

_MIN_OFFCUT_SIDE_MM = 50


def freeze_and_repack_omitted(
    project: Project,
    frozen: AssemblySolution,
) -> AssemblySolution:
    """Keep frozen placements and pack only omitted pieces into leftover space.

    Used panels are filled first (offcuts), then unused stock instances.
    Frozen coordinates never move. If nothing was omitted, ``frozen`` is
    returned unchanged.
    """
    omitted_ids = tuple(frozen.omitted_piece_ids)
    if not omitted_ids:
        return frozen

    kerf_mm = normalize_kerf(project.constraints.kerf_mm)
    packing = inflate_project_for_kerf(project) if kerf_mm else project
    instances = list(packing.stock_panel_instances())
    if not instances:
        return frozen

    omitted_set = set(omitted_ids)
    remaining = [
        (index, board)
        for index, board in enumerate(packing.boards)
        if _board_id(board, index) in omitted_set
    ]
    if not remaining:
        return frozen

    frozen_by_panel = _group_frozen(frozen.placements, instances[0][0])
    used_refs = set(frozen_by_panel)
    ordered = [item for item in instances if item[0] in used_refs]
    ordered.extend(item for item in instances if item[0] not in used_refs)

    new_placements: list[BoardPlacement] = []
    offcuts: list[Offcut] = []
    allow_rotation = packing.constraints.allow_rotation

    for reference, panel in ordered:
        if not remaining and reference not in used_refs:
            break
        extra, leftover, remaining = _pack_panel_with_frozen(
            reference,
            panel,
            remaining,
            frozen_by_panel.get(reference, ()),
            allow_rotation=allow_rotation,
            kerf_mm=kerf_mm,
        )
        new_placements.extend(extra)
        offcuts.extend(leftover)

    merged = list(frozen.placements) + new_placements
    placed_ids = {item.board_id for item in merged}
    still_omitted = tuple(
        piece_id for piece_id in omitted_ids if piece_id not in placed_ids
    )
    notes = list(frozen.explanation.notes) + [
        "freeze_repack",
        f"frozen:{len(frozen.placements)}",
        f"added:{len(new_placements)}",
    ]
    raw = AssemblySolution(
        placements=merged,
        explanation=SolutionExplanation(notes=notes),
        omitted_piece_ids=still_omitted,
        offcuts=tuple(offcuts),
    )
    evaluated = SolutionEvaluator(project).evaluate(raw)
    if evaluated.solution is None:
        return replace(
            frozen,
            explanation=SolutionExplanation(notes=notes),
            omitted_piece_ids=omitted_ids,
        )
    return evaluated.solution


def _board_id(board: Board, index: int) -> str:
    return board.id or f"board-{index + 1}"


def _group_frozen(
    placements: list[BoardPlacement],
    fallback: PanelReference,
) -> dict[PanelReference, list[BoardPlacement]]:
    grouped: dict[PanelReference, list[BoardPlacement]] = {}
    for placement in placements:
        reference = placement.panel_reference or fallback
        grouped.setdefault(reference, []).append(placement)
    return grouped


def _pack_panel_with_frozen(
    reference: PanelReference,
    panel: StockPanel,
    remaining: list[tuple[int, Board]],
    frozen: list[BoardPlacement] | tuple[BoardPlacement, ...],
    *,
    allow_rotation: bool,
    kerf_mm: float,
) -> tuple[list[BoardPlacement], list[Offcut], list[tuple[int, Board]]]:
    packer = MaxRects(
        length_mm=panel.length_mm,
        width_mm=panel.width_mm,
        heuristic=best_area_fit,
    )
    for placement in frozen:
        length, width = inflate_size(placement.length_mm, placement.width_mm, kerf_mm)
        packer.occupy(placement.x_mm, placement.y_mm, length, width)

    extra: list[BoardPlacement] = []
    not_placed: list[tuple[int, Board]] = []
    for board_index, board in remaining:
        compatible = (
            abs(board.thickness_mm - panel.thickness_mm) < 1e-6
            and board.material_key == panel.material_key
        )
        if not compatible:
            not_placed.append((board_index, board))
            continue
        found = packer.place(
            length_mm=board.length_mm,
            width_mm=board.width_mm,
            allow_rotation=rotation_allowed(board, allow_rotation),
        )
        if found is None:
            not_placed.append((board_index, board))
            continue
        packed = BoardPlacement(
            board_id=_board_id(board, board_index),
            x_mm=found.x_mm,
            y_mm=found.y_mm,
            length_mm=found.length_mm,
            width_mm=found.width_mm,
            rotated=found.rotated,
            panel_reference=reference,
        )
        extra.append(deflate_placement(packed, kerf_mm) if kerf_mm else packed)

    leftover = [
        Offcut(
            panel_reference=reference,
            x_mm=rectangle.x_mm,
            y_mm=rectangle.y_mm,
            length_mm=(
                max(rectangle.length_mm - kerf_mm, 0.0)
                if kerf_mm
                else rectangle.length_mm
            ),
            width_mm=(
                max(rectangle.width_mm - kerf_mm, 0.0)
                if kerf_mm
                else rectangle.width_mm
            ),
        )
        for rectangle in packer.free_rectangles
        if rectangle.length_mm >= _MIN_OFFCUT_SIDE_MM
        and rectangle.width_mm >= _MIN_OFFCUT_SIDE_MM
    ]
    leftover = [
        item
        for item in leftover
        if item.length_mm >= _MIN_OFFCUT_SIDE_MM
        and item.width_mm >= _MIN_OFFCUT_SIDE_MM
    ]
    return extra, leftover, not_placed
