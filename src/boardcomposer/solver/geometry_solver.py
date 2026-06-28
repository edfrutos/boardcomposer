from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.scoring_weights import ScoringWeights

from .base_solver import BaseSolver
from .deduplication import deduplicate_solutions
from .evaluation import evaluate
from .free_space_generator import generate_free_space_solution
from .constraints_validator import respects_constraints
from .layout_generator import (
    generate_horizontal_permutations,
    generate_vertical_permutations,
)


class GeometrySolver(BaseSolver):
    def __init__(self, project: Project, weights: ScoringWeights | None = None) -> None:
        self.project = project
        self.weights = weights

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
        evaluated = [evaluate(solution, total_boards=len(self.project.boards), weights=self.weights) for solution in unique]

        return sorted(
            evaluated,
            key=lambda solution: solution.score.total,
            reverse=True,
        )
