"""Skyline packing across physical stock-panel instances (IDE-0022 / ADR-014)."""

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
from boardcomposer.domain.grain import rotation_allowed
from boardcomposer.solver.board_ordering import (
    largest_area_first,
    longest_edge_first,
    original_order,
)
from boardcomposer.solver.panel_ordering import PANEL_ORDERINGS
from boardcomposer.solver.placement_failures import record_placement_failure
from boardcomposer.solver.skyline.skyline import Skyline

BoardOrdering = Callable[[list[Board]], list[Board]]
PanelOrdering = Callable[
    [tuple[tuple[PanelReference, StockPanel], ...]],
    list[tuple[PanelReference, StockPanel]],
]

SKYLINE_BOARD_ORDERINGS = (
    ("original", original_order),
    ("largest_area", largest_area_first),
    ("longest_edge", longest_edge_first),
)

# Free leftover smaller than this on either side isn't worth reporting
# as a reusable offcut (kerf, sawdust-sized slivers, ...). See ADR-016.
_MIN_OFFCUT_SIDE_MM = 50


def _panel_offcuts(
    reference: PanelReference,
    skyline: Skyline,
    panel_height_mm: float,
) -> list[Offcut]:
    """Turn leftover skyline segments into usable offcuts."""
    offcuts: list[Offcut] = []
    for node in skyline.nodes:
        leftover_height = panel_height_mm - node.y_mm
        if (
            node.width_mm >= _MIN_OFFCUT_SIDE_MM
            and leftover_height >= _MIN_OFFCUT_SIDE_MM
        ):
            offcuts.append(
                Offcut(
                    panel_reference=reference,
                    x_mm=node.x_mm,
                    y_mm=node.y_mm,
                    length_mm=node.width_mm,
                    width_mm=leftover_height,
                )
            )
    return offcuts


@dataclass
class _PackingState:
    remaining: list[tuple[int, Board]]
    placements: list[BoardPlacement] = field(default_factory=list)
    offcuts: list[Offcut] = field(default_factory=list)

    @property
    def done(self) -> bool:
        return not self.remaining


def _pack_panel(
    reference: PanelReference,
    panel: StockPanel,
    allow_rotation: bool,
    remaining: list[tuple[int, Board]],
) -> tuple[list[BoardPlacement], list[Offcut], list[tuple[int, Board]]]:
    """Fit as many `remaining` boards as possible onto one physical panel."""
    packer = Skyline(
        width_mm=panel.length_mm,
        max_height_mm=panel.width_mm,
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
                algorithm="skyline",
            )
            not_placed.append((board_index, board))
            continue

        position = packer.place(
            width_mm=board.length_mm,
            height_mm=board.width_mm,
            allow_rotation=rotation_allowed(board, allow_rotation),
        )

        if position is None:
            record_placement_failure(
                piece_id=board.id or f"board-{board_index + 1}",
                reason="no_fit",
                stock_panel_index=reference.stock_panel_index,
                instance_index=reference.instance_index,
                algorithm="skyline",
            )
            not_placed.append((board_index, board))
            continue

        placements.append(
            BoardPlacement(
                board_id=board.id or f"board-{board_index + 1}",
                x_mm=position.x_mm,
                y_mm=position.y_mm,
                length_mm=(board.width_mm if position.rotated else board.length_mm),
                width_mm=(board.length_mm if position.rotated else board.width_mm),
                rotated=position.rotated,
                panel_reference=reference,
            )
        )

    offcuts = _panel_offcuts(reference, packer, panel.width_mm) if placements else []

    return placements, offcuts, not_placed


def _generate_candidate(
    project: Project,
    named_ordering: tuple[str, BoardOrdering],
    named_panel_ordering: tuple[str, PanelOrdering],
) -> AssemblySolution:
    ordering_name, ordering = named_ordering
    panel_ordering_name, panel_ordering = named_panel_ordering

    state = _PackingState(remaining=list(enumerate(ordering(project.boards))))

    for reference, panel in panel_ordering(project.stock_panel_instances()):
        if state.done:
            break

        placements, offcuts, state.remaining = _pack_panel(
            reference,
            panel,
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
                "skyline",
                "multi_panel",
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


def generate_multi_panel_skyline_solution(project: Project) -> AssemblySolution:
    """Pack boards across the project's available physical stock panels."""
    candidates = [
        _generate_candidate(
            project=project,
            named_ordering=(ordering_name, ordering),
            named_panel_ordering=(panel_ordering_name, panel_ordering),
        )
        for ordering_name, ordering in SKYLINE_BOARD_ORDERINGS
        for panel_ordering_name, panel_ordering in PANEL_ORDERINGS
    ]
    return max(candidates, key=lambda solution: _candidate_key(project, solution))
