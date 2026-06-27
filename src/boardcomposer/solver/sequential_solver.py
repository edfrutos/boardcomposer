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

            length = board.length_mm
            width = board.width_mm
            rotated = False

            if (
                self.project.constraints.allow_rotation
                and self.project.constraints.max_length_mm is not None
                and x + length > self.project.constraints.max_length_mm
                and x + board.width_mm <= self.project.constraints.max_length_mm
            ):
                length = board.width_mm
                width = board.length_mm
                rotated = True

            if (
                self.project.constraints.max_length_mm is not None
                and x + length > self.project.constraints.max_length_mm
            ):
                break

            if (
                self.project.constraints.max_width_mm is not None
                and width > self.project.constraints.max_width_mm
            ):
                break

            placements.append(
                BoardPlacement(
                    board_id=board_id,
                    x_mm=x,
                    y_mm=0,
                    length_mm=length,
                    width_mm=width,
                    rotated=rotated,
                )
            )

            x += length

        usage = len(placements) / len(self.project.boards) * 100 if self.project.boards else 0

        return [
            AssemblySolution(
                placements=placements,
                score=SolutionScore(material_usage_score=usage),
                notes=["SequentialSolver"],
            )
        ]
