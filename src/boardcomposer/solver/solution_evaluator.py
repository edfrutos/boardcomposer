"""Validate and evaluate generated layout solutions."""

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.evaluation import evaluate
from boardcomposer.solver.scoring_weights import ScoringWeights
from boardcomposer.solver.solution_validator import is_valid_solution


class SolutionEvaluator:
    """Validate and score candidate solutions for a project."""

    def __init__(
        self,
        project: Project,
        weights: ScoringWeights | None = None,
    ) -> None:
        self.project = project
        self.weights = weights

    def evaluate(
        self,
        solution: AssemblySolution,
    ) -> AssemblySolution | None:
        """Return the evaluated solution or None when it is invalid."""
        if not is_valid_solution(solution, self.project):
            return None

        return evaluate(
            solution,
            total_boards=len(self.project.boards),
            weights=self.weights,
        )
