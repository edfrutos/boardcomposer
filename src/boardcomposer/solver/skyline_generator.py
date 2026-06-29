from boardcomposer.domain import AssemblySolution, BoardPlacement, Project, SolutionExplanation
from boardcomposer.solver.skyline.skyline import Skyline


def generate_skyline_solution(project: Project) -> AssemblySolution:
    max_width = project.constraints.max_width_mm or max(
        (board.length_mm for board in project.boards),
        default=0,
    )

    skyline = Skyline(width_mm=max_width)
    placements: list[BoardPlacement] = []

    for index, board in enumerate(project.boards):
        position = skyline.place(
            width_mm=board.length_mm,
            height_mm=board.width_mm,
        )

        if position is None:
            continue

        placements.append(
            BoardPlacement(
                board_id=board.id or f"board-{index + 1}",
                x_mm=position.x_mm,
                y_mm=position.y_mm,
                length_mm=board.length_mm,
                width_mm=board.width_mm,
            )
        )

    return AssemblySolution(
        placements=placements,
        explanation=SolutionExplanation(notes=["skyline"]),
    )
