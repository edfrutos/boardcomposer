from boardcomposer.domain import AssemblySolution, BoardPlacement, Project, SolutionScore


from .base_solver import BaseSolver


class SequentialSolver(BaseSolver):
    def __init__(self, project: Project) -> None:
        self.project = project

    def solve(self) -> list[AssemblySolution]:
        x = 0.0
        placements: list[BoardPlacement] = []

        for index, board in enumerate(self.project.boards):
            board_id = board.id or f"board-{index + 1}"
            placements.append(
                BoardPlacement(
                    board_id=board_id,
                    x_mm=x,
                    y_mm=0,
                    length_mm=board.length_mm,
                    width_mm=board.width_mm,
                )
            )
            x += board.length_mm

        solution = AssemblySolution(
            placements=placements,
            score=SolutionScore(material_usage_score=100.0),
            notes=["Solución secuencial básica: coloca las tablas una detrás de otra."],
        )

        return [solution]
