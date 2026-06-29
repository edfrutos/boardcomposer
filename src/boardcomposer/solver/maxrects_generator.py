from collections.abc import Callable

from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    Project,
    SolutionExplanation,
)
from boardcomposer.solver.maxrects.maxrects import MaxRects
from boardcomposer.solver.maxrects.placement import MaxRectsPlacement
from boardcomposer.solver.maxrects.strategies import MAXRECTS_HEURISTICS

MaxRectsHeuristic = Callable[
    [list[MaxRectsPlacement]],
    MaxRectsPlacement | None,
]


def _maxrects_size(project: Project) -> tuple[float, float]:
    length = project.constraints.max_length_mm or sum(
        board.length_mm for board in project.boards
    )
    width = project.constraints.max_width_mm or max(
        (board.width_mm for board in project.boards),
        default=0,
    )

    return length, width


def _generate_solution(
    project: Project,
    heuristic_name: str,
    heuristic: MaxRectsHeuristic,
) -> AssemblySolution:
    length, width = _maxrects_size(project)
    maxrects = MaxRects(
        length_mm=length,
        width_mm=width,
        heuristic=heuristic,
    )
    placements: list[BoardPlacement] = []

    for index, board in enumerate(project.boards):
        placement = maxrects.place(
            length_mm=board.length_mm,
            width_mm=board.width_mm,
            allow_rotation=project.constraints.allow_rotation,
        )

        if placement is None:
            continue

        placements.append(
            BoardPlacement(
                board_id=board.id or f"board-{index + 1}",
                x_mm=placement.x_mm,
                y_mm=placement.y_mm,
                length_mm=placement.length_mm,
                width_mm=placement.width_mm,
                rotated=placement.rotated,
            )
        )

    return AssemblySolution(
        placements=placements,
        explanation=SolutionExplanation(notes=["maxrects", heuristic_name]),
    )


def generate_maxrects_solution(project: Project) -> AssemblySolution:
    candidates = [
        _generate_solution(project, name, heuristic)
        for name, heuristic in MAXRECTS_HEURISTICS
    ]

    return max(
        candidates,
        key=lambda solution: (
            len(solution.placements),
            -solution.total_width_mm,
            -solution.total_length_mm,
        ),
    )
