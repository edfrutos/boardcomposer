"""
MaxRects runner.
"""

from collections.abc import Callable, Iterator

from boardcomposer.domain import (
    AssemblySolution,
    Board,
    BoardPlacement,
    Project,
    SolutionExplanation,
)
from boardcomposer.solver.maxrects.adaptive import AdaptiveSelector
from boardcomposer.solver.maxrects.contact import contact_score
from boardcomposer.solver.maxrects.heuristics import (
    Heuristic,
    best_contact_point_fit,
)
from boardcomposer.solver.maxrects.maxrects import MaxRects
from boardcomposer.solver.maxrects.orderings import MAXRECTS_BOARD_ORDERINGS
from boardcomposer.solver.maxrects.placement import MaxRectsPlacement
from boardcomposer.solver.maxrects.strategies import MAXRECTS_HEURISTICS

BoardOrdering = Callable[[list[Board]], list[Board]]


def _maxrects_size(project: Project) -> tuple[float, float]:
    length = project.constraints.max_length_mm or sum(
        board.length_mm for board in project.boards
    )
    width = project.constraints.max_width_mm or max(
        (board.width_mm for board in project.boards),
        default=0,
    )

    return length, width


def _to_board_placement(
    placement: MaxRectsPlacement,
    board: Board,
    index: int,
) -> BoardPlacement:
    return BoardPlacement(
        board_id=board.id or f"board-{index + 1}",
        x_mm=placement.x_mm,
        y_mm=placement.y_mm,
        length_mm=placement.length_mm,
        width_mm=placement.width_mm,
        rotated=placement.rotated,
    )


def _place_all_boards_adaptive(
    maxrects: MaxRects,
    boards: list[Board],
    allow_rotation: bool,
) -> list[BoardPlacement]:
    placements: list[BoardPlacement] = []
    selector = AdaptiveSelector()

    for index, board in enumerate(boards):
        heuristic = selector.choose(
            board,
            placements,
        )

        if heuristic is best_contact_point_fit:
            candidates = maxrects.find_candidates(
                length_mm=board.length_mm,
                width_mm=board.width_mm,
                allow_rotation=allow_rotation,
            )

            placed = [
                MaxRectsPlacement(
                    x_mm=placement.x_mm,
                    y_mm=placement.y_mm,
                    length_mm=placement.length_mm,
                    width_mm=placement.width_mm,
                    rotated=placement.rotated,
                )
                for placement in placements
            ]

            selected = best_contact_point_fit(
                candidates,
                score=lambda candidate: contact_score(
                    candidate,
                    placed,
                    board_length_mm=maxrects.length_mm,
                    board_width_mm=maxrects.width_mm,
                ),
            )

            if selected is None:
                continue

            placement = maxrects.place_candidate(selected)

        else:
            maxrects.heuristic = heuristic

            placement = maxrects.place(
                length_mm=board.length_mm,
                width_mm=board.width_mm,
                allow_rotation=allow_rotation,
            )

            if placement is None:
                continue

        placements.append(
            _to_board_placement(
                placement,
                board,
                index,
            )
        )

    return placements


def generate_maxrects_candidate(
    project: Project,
    heuristic_name: str,
    heuristic: Heuristic,
    ordering_name: str,
    ordering: BoardOrdering,
) -> AssemblySolution:
    length, width = _maxrects_size(project)
    maxrects = MaxRects(
        length_mm=length,
        width_mm=width,
        heuristic=heuristic,
    )

    placements = _place_all_boards_fixed(
        maxrects=maxrects,
        boards=ordering(project.boards),
        allow_rotation=project.constraints.allow_rotation,
    )

    return AssemblySolution(
        placements=placements,
        explanation=SolutionExplanation(
            notes=["maxrects", heuristic_name, ordering_name]
        ),
    )


def iter_maxrects_solutions(project: Project) -> Iterator[AssemblySolution]:
    for heuristic_name, heuristic in MAXRECTS_HEURISTICS:
        for ordering_name, ordering in MAXRECTS_BOARD_ORDERINGS:
            yield generate_maxrects_candidate(
                project=project,
                heuristic_name=heuristic_name,
                heuristic=heuristic,
                ordering_name=ordering_name,
                ordering=ordering,
            )

    for ordering_name, ordering in MAXRECTS_BOARD_ORDERINGS:
        yield generate_adaptive_maxrects_candidate(
            project=project,
            ordering_name=ordering_name,
            ordering=ordering,
        )


def _place_all_boards_by_contact(
    maxrects: MaxRects,
    boards: list[Board],
    allow_rotation: bool,
) -> list[BoardPlacement]:
    placements: list[BoardPlacement] = []

    for index, board in enumerate(boards):
        candidates = maxrects.find_candidates(
            length_mm=board.length_mm,
            width_mm=board.width_mm,
            allow_rotation=allow_rotation,
        )

        placed = [
            MaxRectsPlacement(
                x_mm=placement.x_mm,
                y_mm=placement.y_mm,
                length_mm=placement.length_mm,
                width_mm=placement.width_mm,
                rotated=placement.rotated,
            )
            for placement in placements
        ]

        selected = best_contact_point_fit(
            candidates,
            score=lambda candidate: contact_score(
                candidate,
                placed,
                board_length_mm=maxrects.length_mm,
                board_width_mm=maxrects.width_mm,
            ),
        )

        if selected is None:
            continue

        placement = maxrects.place_candidate(selected)
        placements.append(_to_board_placement(placement, board, index))

    return placements


def generate_contact_maxrects_candidate(
    project: Project,
    ordering_name: str,
    ordering: BoardOrdering,
) -> AssemblySolution:
    length, width = _maxrects_size(project)
    maxrects = MaxRects(
        length_mm=length,
        width_mm=width,
    )

    placements = _place_all_boards_by_contact(
        maxrects=maxrects,
        boards=ordering(project.boards),
        allow_rotation=project.constraints.allow_rotation,
    )

    return AssemblySolution(
        placements=placements,
        explanation=SolutionExplanation(
            notes=["maxrects", "best_contact_point_fit", ordering_name]
        ),
    )


def _place_all_boards_fixed(
    maxrects: MaxRects,
    boards: list[Board],
    allow_rotation: bool,
) -> list[BoardPlacement]:
    placements: list[BoardPlacement] = []

    for index, board in enumerate(boards):
        placement = maxrects.place(
            length_mm=board.length_mm,
            width_mm=board.width_mm,
            allow_rotation=allow_rotation,
        )

        if placement is None:
            continue

        placements.append(_to_board_placement(placement, board, index))

    return placements


def generate_adaptive_maxrects_candidate(
    project: Project,
    ordering_name: str,
    ordering: BoardOrdering,
) -> AssemblySolution:
    length, width = _maxrects_size(project)
    maxrects = MaxRects(
        length_mm=length,
        width_mm=width,
    )

    placements = _place_all_boards_adaptive(
        maxrects=maxrects,
        boards=ordering(project.boards),
        allow_rotation=project.constraints.allow_rotation,
    )

    return AssemblySolution(
        placements=placements,
        explanation=SolutionExplanation(notes=["maxrects", "adaptive", ordering_name]),
    )
