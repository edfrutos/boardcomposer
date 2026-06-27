from boardcomposer.domain import AssemblySolution, Project

from .base_solver import BaseSolver
from .evaluation import evaluate
from .layout_generator import generate_horizontal_solution, generate_vertical_solution


class GeometrySolver(BaseSolver):
    def __init__(self, project: Project) -> None:
        self.project = project

    def solve(self) -> list[AssemblySolution]:
        candidates = [
            generate_horizontal_solution(self.project),
            generate_vertical_solution(self.project),
        ]

        valid = [
            solution for solution in candidates
            if self._respects_constraints(solution)
        ]

        evaluated = [evaluate(solution) for solution in valid]

        return sorted(
            evaluated,
            key=lambda solution: solution.score.total,
            reverse=True,
        )

    def _respects_constraints(self, solution: AssemblySolution) -> bool:
        constraints = self.project.constraints

        if constraints.max_length_mm is not None and solution.total_length_mm > constraints.max_length_mm:
            return False

        if constraints.max_width_mm is not None and solution.total_width_mm > constraints.max_width_mm:
            return False

        return True
