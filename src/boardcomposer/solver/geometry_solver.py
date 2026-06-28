from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.strategies import (
    OptimizationStrategy,
    balanced_strategy,
)

from .base_solver import BaseSolver
from .constraints_validator import respects_constraints
from .deduplication import deduplicate_solutions
from .evaluation import evaluate
from .generators import generators_by_name


class GeometrySolver(BaseSolver):
    def __init__(
        self,
        project: Project,
        strategy: OptimizationStrategy | None = None,
    ) -> None:
        self.project = project
        self.strategy = strategy or balanced_strategy()

    def solve(self) -> list[AssemblySolution]:
        candidates = []

        for generator in generators_by_name(list(self.strategy.generator_names)):
            candidates.extend(generator(self.project))

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
