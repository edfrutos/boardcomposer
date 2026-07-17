"""MaxRects orchestration across physical stock-panel instances."""

from collections.abc import Callable
from dataclasses import dataclass, field
from math import isclose

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
from boardcomposer.solver.maxrects.free_rectangle import FreeRectangle
from boardcomposer.solver.maxrects.heuristics import Heuristic
from boardcomposer.solver.maxrects.maxrects import MaxRects
from boardcomposer.solver.maxrects.orderings import MAXRECTS_BOARD_ORDERINGS
from boardcomposer.solver.maxrects.strategies import MAXRECTS_HEURISTICS
from boardcomposer.solver.panel_ordering import PANEL_ORDERINGS
from boardcomposer.solver.placement_failures import record_placement_failure

BoardOrdering = Callable[[list[Board]], list[Board]]
PanelOrdering = Callable[
    [tuple[tuple[PanelReference, StockPanel], ...]],
    list[tuple[PanelReference, StockPanel]],
]

# Free rectangles smaller than this on either side aren't worth reporting
# as reusable offcuts (kerf, sawdust-sized slivers, ...). See ADR-016.
_MIN_OFFCUT_SIDE_MM = 50


def _panel_offcuts(
    reference: PanelReference,
    free_rectangles: list[FreeRectangle],
) -> list[Offcut]:
    """Convert a consumed panel's leftover free space into usable offcuts."""
    return [
        Offcut(
            panel_reference=reference,
            x_mm=rectangle.x_mm,
            y_mm=rectangle.y_mm,
            length_mm=rectangle.length_mm,
            width_mm=rectangle.width_mm,
        )
        for rectangle in free_rectangles
        if rectangle.length_mm >= _MIN_OFFCUT_SIDE_MM
        and rectangle.width_mm >= _MIN_OFFCUT_SIDE_MM
    ]


@dataclass
class _PackingState:
    """Accumulates placements/offcuts across every panel of one candidate."""

    remaining: list[tuple[int, Board]]
    placements: list[BoardPlacement] = field(default_factory=list)
    offcuts: list[Offcut] = field(default_factory=list)

    @property
    def done(self) -> bool:
        return not self.remaining


def _pack_panel(
    reference: PanelReference,
    panel: StockPanel,
    heuristic: Heuristic,
    allow_rotation: bool,
    remaining: list[tuple[int, Board]],
) -> tuple[list[BoardPlacement], list[Offcut], list[tuple[int, Board]]]:
    """Fit as many `remaining` boards as possible onto one physical panel."""
    packer = MaxRects(
        length_mm=panel.length_mm,
        width_mm=panel.width_mm,
        heuristic=heuristic,
    )
    placements: list[BoardPlacement] = []
    not_placed: list[tuple[int, Board]] = []

    for board_index, board in remaining:
        compatible = isclose(board.thickness_mm, panel.thickness_mm) and (
            board.material_key == panel.material_key
        )

        if not compatible:
            record_placement_failure(
                piece_id=board.id or f"board-{board_index + 1}",
                reason="incompatible",
                stock_panel_index=reference.stock_panel_index,
                instance_index=reference.instance_index,
            )
            not_placed.append((board_index, board))
            continue

        placement = packer.place(
            length_mm=board.length_mm,
            width_mm=board.width_mm,
            allow_rotation=allow_rotation,
        )

        if placement is None:
            record_placement_failure(
                piece_id=board.id or f"board-{board_index + 1}",
                reason="no_fit",
                stock_panel_index=reference.stock_panel_index,
                instance_index=reference.instance_index,
            )
            not_placed.append((board_index, board))
            continue

        placements.append(
            BoardPlacement(
                board_id=board.id or f"board-{board_index + 1}",
                x_mm=placement.x_mm,
                y_mm=placement.y_mm,
                length_mm=placement.length_mm,
                width_mm=placement.width_mm,
                rotated=placement.rotated,
                panel_reference=reference,
            )
        )

    offcuts = _panel_offcuts(reference, packer.free_rectangles) if placements else []

    return placements, offcuts, not_placed


def _generate_candidate(
    project: Project,
    named_heuristic: tuple[str, Heuristic],
    named_ordering: tuple[str, BoardOrdering],
    named_panel_ordering: tuple[str, PanelOrdering],
) -> AssemblySolution:
    heuristic_name, heuristic = named_heuristic
    ordering_name, ordering = named_ordering
    panel_ordering_name, panel_ordering = named_panel_ordering

    state = _PackingState(remaining=list(enumerate(ordering(project.boards))))

    for reference, panel in panel_ordering(project.stock_panel_instances()):
        if state.done:
            break

        placements, offcuts, state.remaining = _pack_panel(
            reference,
            panel,
            heuristic,
            project.constraints.allow_rotation,
            state.remaining,
        )
        state.placements.extend(placements)
        state.offcuts.extend(offcuts)

    return AssemblySolution(
        placements=state.placements,
        offcuts=tuple(state.offcuts),
        explanation=SolutionExplanation(
            notes=[
                "maxrects",
                "multi_panel",
                heuristic_name,
                ordering_name,
                panel_ordering_name,
            ]
        ),
    )


def _candidate_key(
    project: Project,
    solution: AssemblySolution,
) -> tuple[int, int, float, int]:
    return (
        len(solution.placements),
        -len(solution.panel_references),
        -solution.total_panel_waste_area_mm2(project),
        -sum(1 for placement in solution.placements if placement.rotated),
    )


def generate_multi_panel_maxrects_solution(project: Project) -> AssemblySolution:
    """Pack boards across the project's available physical stock panels."""
    candidates = [
        _generate_candidate(
            project=project,
            named_heuristic=(heuristic_name, heuristic),
            named_ordering=(ordering_name, ordering),
            named_panel_ordering=(panel_ordering_name, panel_ordering),
        )
        for heuristic_name, heuristic in MAXRECTS_HEURISTICS
        for ordering_name, ordering in MAXRECTS_BOARD_ORDERINGS
        for panel_ordering_name, panel_ordering in PANEL_ORDERINGS
    ]
    return max(candidates, key=lambda solution: _candidate_key(project, solution))
