"""Validate and evaluate generated layout solutions."""

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.evaluation import evaluate
from boardcomposer.solver.evaluation_result import EvaluationResult
from boardcomposer.solver.scoring_weights import ScoringWeights
from boardcomposer.solver.solution_validator import validate_solution


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
    ) -> EvaluationResult:
        """Return the evaluation result for a candidate solution."""
        validation = validate_solution(
            solution,
            self.project,
        )

        if not validation.valid:
            return EvaluationResult(
                solution=None,
                validation=validation,
            )

        evaluated_solution = evaluate(
            solution,
            total_boards=len(self.project.boards),
            weights=self.weights,
        )

        return EvaluationResult(
            solution=evaluated_solution,
            validation=validation,
        )
