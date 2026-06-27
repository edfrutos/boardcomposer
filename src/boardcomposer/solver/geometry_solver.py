from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    Project,
    SolutionExplanation,
    SolutionScore,
)

from .base_solver import BaseSolver


class GeometrySolver(BaseSolver):
    def __init__(self, project: Project) -> None:
        self.project = project

    def solve(self) -> list[AssemblySolution]:
        solutions = [
            self._horizontal_solution(),
            self._vertical_solution(),
        ]
        return sorted(solutions, key=lambda solution: solution.score.total, reverse=True)

    def _horizontal_solution(self) -> AssemblySolution:
        x = 0.0
        placements: list[BoardPlacement] = []

        for index, board in enumerate(self.project.boards):
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

        solution = AssemblySolution(placements=placements)
        waste_score = max(0.0, (1.0 - solution.waste_ratio) * 50)

        return AssemblySolution(
            placements=placements,
            score=SolutionScore(material_usage_score=50, waste_score=waste_score),
            explanation=SolutionExplanation(notes=["horizontal"]),
        )

    def _vertical_solution(self) -> AssemblySolution:
        y = 0.0
        placements: list[BoardPlacement] = []

        for index, board in enumerate(self.project.boards):
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

        solution = AssemblySolution(placements=placements)
        waste_score = max(0.0, (1.0 - solution.waste_ratio) * 50)

        return AssemblySolution(
            placements=placements,
            score=SolutionScore(material_usage_score=50, waste_score=waste_score),
            explanation=SolutionExplanation(notes=["vertical"]),
        )
