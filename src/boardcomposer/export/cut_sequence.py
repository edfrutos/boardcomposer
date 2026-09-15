"""Per-panel saw sequence (IDE-0027).

Recover a guillotine through-cut order from packed pieces. When the packing
is not guillotine-valid, fall back to a stable (y, x, id) piece order.
"""

from __future__ import annotations

from dataclasses import dataclass

from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    PanelReference,
    Project,
)

_EPS = 1e-4


@dataclass(frozen=True)
class SequenceStep:
    """One numbered action on a physical panel."""

    index: int
    kind: str
    axis: str | None = None
    position_mm: float | None = None
    span_mm: float | None = None
    piece_id: str | None = None


@dataclass(frozen=True)
class PanelCutSequence:
    """Ordered saw/piece steps for one physical panel instance."""

    panel_id: str
    stock_panel_index: int
    instance_index: int
    length_mm: float
    width_mm: float
    steps: tuple[SequenceStep, ...]
    piece_order: tuple[str, ...]
    guillotine: bool


@dataclass(frozen=True)
class _Region:
    x: float
    y: float
    length: float
    width: float


def build_cut_sequences(
    solution: AssemblySolution,
    project: Project | None = None,
) -> tuple[PanelCutSequence, ...]:
    """Return a saw sequence for every used physical panel."""
    groups: dict[tuple[int, int], list[BoardPlacement]] = {}
    for placement in solution.placements:
        reference = placement.panel_reference
        key = (
            (reference.stock_panel_index, reference.instance_index)
            if reference is not None
            else (-1, 0)
        )
        groups.setdefault(key, []).append(placement)

    sequences: list[PanelCutSequence] = []
    for (stock_index, instance_index), placements in sorted(groups.items()):
        sequences.append(
            _sequence_for_panel(
                placements,
                project=project,
                stock_index=stock_index,
                instance_index=instance_index,
            )
        )
    return tuple(sequences)


def piece_sequence_numbers(
    solution: AssemblySolution,
    project: Project | None = None,
) -> dict[int, int]:
    """Map placement index → 1-based piece order on its panel."""
    lookup: dict[tuple[int, int, str], int] = {}
    for panel in build_cut_sequences(solution, project):
        for order, piece_id in enumerate(panel.piece_order, start=1):
            lookup[(panel.stock_panel_index, panel.instance_index, piece_id)] = order

    numbers: dict[int, int] = {}
    for index, placement in enumerate(solution.placements):
        reference = placement.panel_reference
        key = (
            (reference.stock_panel_index if reference is not None else -1),
            reference.instance_index if reference is not None else 0,
            placement.board_id,
        )
        numbers[index] = lookup.get(key, index + 1)
    return numbers


def _sequence_for_panel(
    placements: list[BoardPlacement],
    *,
    project: Project | None,
    stock_index: int,
    instance_index: int,
) -> PanelCutSequence:
    length, width, panel_id = _panel_geometry(
        placements,
        project=project,
        stock_index=stock_index,
        instance_index=instance_index,
    )
    raw, guillotine = _isolate(_Region(0.0, 0.0, length, width), placements)
    steps = tuple(
        SequenceStep(
            index=index,
            kind=item.kind,
            axis=item.axis,
            position_mm=item.position_mm,
            span_mm=item.span_mm,
            piece_id=item.piece_id,
        )
        for index, item in enumerate(raw, start=1)
    )
    piece_order = tuple(step.piece_id for step in steps if step.piece_id is not None)
    return PanelCutSequence(
        panel_id=panel_id,
        stock_panel_index=stock_index,
        instance_index=instance_index,
        length_mm=length,
        width_mm=width,
        steps=steps,
        piece_order=piece_order,
        guillotine=guillotine,
    )


def _panel_geometry(
    placements: list[BoardPlacement],
    *,
    project: Project | None,
    stock_index: int,
    instance_index: int,
) -> tuple[float, float, str]:
    reference = (
        PanelReference(stock_index, instance_index) if stock_index >= 0 else None
    )
    if project is not None and reference is not None:
        panel = project.stock_panel_for(reference)
        if panel is not None:
            panel_id = panel.id or f"panel-{stock_index + 1}"
            return panel.length_mm, panel.width_mm, panel_id

    length = max(item.right_mm for item in placements)
    width = max(item.top_mm for item in placements)
    panel_id = f"panel-{stock_index + 1}" if stock_index >= 0 else "panel"
    return length, width, panel_id


def _isolate(
    region: _Region,
    placements: list[BoardPlacement],
) -> tuple[list[SequenceStep], bool]:
    pieces = [item for item in placements if _contained(region, item)]
    if not pieces:
        return [], True
    if len(pieces) == 1:
        return [_piece_step(pieces[0].board_id)], True

    y_cuts = _through_y(region, pieces)
    x_cuts = _through_x(region, pieces)
    if y_cuts:
        return _split_y(region, pieces, y_cuts[0])
    if x_cuts:
        return _split_x(region, pieces, x_cuts[0])

    ordered = sorted(pieces, key=lambda item: (item.y_mm, item.x_mm, item.board_id))
    return [_piece_step(item.board_id) for item in ordered], False


def _split_y(
    region: _Region,
    pieces: list[BoardPlacement],
    position: float,
) -> tuple[list[SequenceStep], bool]:
    cut = SequenceStep(
        index=0,
        kind="h",
        axis="y",
        position_mm=position,
        span_mm=region.length,
    )
    low = _Region(region.x, region.y, region.length, position - region.y)
    high = _Region(
        region.x,
        position,
        region.length,
        region.y + region.width - position,
    )
    first, g_first = _isolate(low, pieces)
    second, g_second = _isolate(high, pieces)
    return [cut, *first, *second], g_first and g_second


def _split_x(
    region: _Region,
    pieces: list[BoardPlacement],
    position: float,
) -> tuple[list[SequenceStep], bool]:
    cut = SequenceStep(
        index=0,
        kind="v",
        axis="x",
        position_mm=position,
        span_mm=region.width,
    )
    left = _Region(region.x, region.y, position - region.x, region.width)
    right = _Region(
        position,
        region.y,
        region.x + region.length - position,
        region.width,
    )
    first, g_first = _isolate(left, pieces)
    second, g_second = _isolate(right, pieces)
    return [cut, *first, *second], g_first and g_second


def _through_y(region: _Region, pieces: list[BoardPlacement]) -> list[float]:
    lo = region.y
    hi = region.y + region.width
    candidates = sorted(
        {item.top_mm for item in pieces if lo + _EPS < item.top_mm < hi - _EPS}
    )
    return [
        pos
        for pos in candidates
        if all(item.top_mm <= pos + _EPS or item.y_mm >= pos - _EPS for item in pieces)
    ]


def _through_x(region: _Region, pieces: list[BoardPlacement]) -> list[float]:
    lo = region.x
    hi = region.x + region.length
    candidates = sorted(
        {item.right_mm for item in pieces if lo + _EPS < item.right_mm < hi - _EPS}
    )
    return [
        pos
        for pos in candidates
        if all(
            item.right_mm <= pos + _EPS or item.x_mm >= pos - _EPS for item in pieces
        )
    ]


def _contained(region: _Region, piece: BoardPlacement) -> bool:
    return (
        piece.x_mm >= region.x - _EPS
        and piece.y_mm >= region.y - _EPS
        and piece.right_mm <= region.x + region.length + _EPS
        and piece.top_mm <= region.y + region.width + _EPS
    )


def _piece_step(piece_id: str) -> SequenceStep:
    return SequenceStep(index=0, kind="piece", piece_id=piece_id)
