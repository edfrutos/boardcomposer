from boardcomposer.domain import AssemblySolution, BoardPlacement, Project, SolutionExplanation
from boardcomposer.solver.skyline.skyline import Skyline


def _default_skyline_width(project: Project) -> float:
    if project.constraints.max_width_mm is not None:
        return project.constraints.max_width_mm

    if project.constraints.allow_rotation:
        return max(
            (min(board.length_mm, board.width_mm) for board in project.boards),
            default=0,
        )

    return max(
        (board.length_mm for board in project.boards),
        default=0,
    )


def generate_skyline_solution(project: Project) -> AssemblySolution:
    max_width = _default_skyline_width(project)

    skyline = Skyline(width_mm=max_width)
    placements: list[BoardPlacement] = []

    for index, board in enumerate(project.boards):
        position = skyline.place(
            width_mm=board.length_mm,
            height_mm=board.width_mm,
            allow_rotation=project.constraints.allow_rotation,
        )

        if position is None:
            continue

        placements.append(
            BoardPlacement(
                board_id=board.id or f"board-{index + 1}",
                x_mm=position.x_mm,
                y_mm=position.y_mm,
                length_mm=board.width_mm if position.rotated else board.length_mm,
                width_mm=board.length_mm if position.rotated else board.width_mm,
                rotated=position.rotated,
            )
        )

    return AssemblySolution(
        placements=placements,
        explanation=SolutionExplanation(notes=["skyline"]),
    )
