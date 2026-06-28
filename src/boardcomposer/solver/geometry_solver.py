from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.strategies import (
    OptimizationStrategy,
    balanced_strategy,
)

from .base_solver import BaseSolver
from .constraints_validator import respects_constraints
from .deduplication import deduplicate_solutions
from .evaluation import evaluate
from .free_space_generator import generate_free_space_solution
from .layout_generator import (
    generate_horizontal_permutations,
    generate_vertical_permutations,
)


class GeometrySolver(BaseSolver):
    def __init__(
        self,
        project: Project,
        strategy: OptimizationStrategy | None = None,
    ) -> None:
        self.project = project
        self.strategy = strategy or balanced_strategy()

    def solve(self) -> list[AssemblySolution]:
        candidates = [
            *generate_horizontal_permutations(self.project),
            *generate_vertical_permutations(self.project),
            generate_free_space_solution(self.project),
        ]

        valid = [
            solution
            for solution in candidates
            if respects_constraints(solution, self.project.constraints)
        ]

        unique = deduplicate_solutions(valid)
        evaluated = [
            evaluate(
                solution,
                total_boards=len(self.project.boards),
                weights=self.strategy.weights,
            )
            for solution in unique
        ]

        return sorted(
            evaluated,
            key=lambda solution: solution.score.total,
            reverse=True,
        )
