from boardcomposer.domain import AssemblySolution, BoardPlacement, Project, SolutionExplanation


def generate_horizontal_solution(project: Project) -> AssemblySolution:
    x = 0.0
    placements: list[BoardPlacement] = []

    for index, board in enumerate(project.boards):
        placements.append(
            BoardPlacement(
                board_id=board.id or f"board-{index + 1}",
                x_mm=x,
                y_mm=0,
                length_mm=board.length_mm,
                width_mm=board.width_mm,
            )
        )
        x += board.length_mm

    return AssemblySolution(
        placements=placements,
        explanation=SolutionExplanation(notes=["horizontal"]),
    )


def generate_vertical_solution(project: Project) -> AssemblySolution:
    y = 0.0
    placements: list[BoardPlacement] = []

    for index, board in enumerate(project.boards):
        placements.append(
            BoardPlacement(
                board_id=board.id or f"board-{index + 1}",
                x_mm=0,
                y_mm=y,
                length_mm=board.length_mm,
                width_mm=board.width_mm,
            )
        )
        y += board.width_mm

    return AssemblySolution(
        placements=placements,
        explanation=SolutionExplanation(notes=["vertical"]),
    )
