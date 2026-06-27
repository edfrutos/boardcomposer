from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    Project,
    SolutionScore,
)

from .base_solver import BaseSolver


class SequentialSolver(BaseSolver):

    def __init__(self, project: Project) -> None:
        self.project = project

    def solve(self) -> list[AssemblySolution]:

        x = 0.0
        placements: list[BoardPlacement] = []

        for index, board in enumerate(self.project.boards):

            board_id = board.id or f"board-{index+1}"

            if (
                self.project.constraints.max_length_mm is not None
                and x + board.length_mm > self.project.constraints.max_length_mm
            ):
                break

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

        usage = (
            len(placements) / len(self.project.boards) * 100
            if self.project.boards
            else 0
        )

        return [
            AssemblySolution(
                placements=placements,
                score=SolutionScore(material_usage_score=usage),
                notes=["SequentialSolver"],
            )
        ]

    def test_solver_respects_max_length():

        from boardcomposer import ProjectConstraints
        from boardcomposer.solver import SequentialSolver

        project = Project(
            constraints=ProjectConstraints(max_length_mm=2500)
        )

        project.add_board(Board(2000, 300, 20, "A"))
        project.add_board(Board(1000, 300, 20, "B"))

        solution = SequentialSolver(project).solve()[0]

        assert len(solution.placements) == 1
        assert solution.total_length_mm == 2000
