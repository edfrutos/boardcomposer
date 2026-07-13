from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.deduplication import deduplicate_solutions
from boardcomposer.solver.generators import generators_by_name
from boardcomposer.solver.solution_evaluator import SolutionEvaluator
from boardcomposer.solver.strategies import OptimizationStrategy


class CandidatePipeline:
    def __init__(
        self,
        project: Project,
        strategy: OptimizationStrategy,
    ) -> None:
        self.project = project
        self.strategy = strategy

    def run(self) -> list[AssemblySolution]:
        candidates: list[AssemblySolution] = []

        for generator in generators_by_name(list(self.strategy.generator_names)):
            candidates.extend(generator(self.project))

        unique_candidates = deduplicate_solutions(candidates)

        evaluator = SolutionEvaluator(
            project=self.project,
            weights=self.strategy.weights,
        )

        evaluated: list[AssemblySolution] = []

        for candidate in unique_candidates:
            solution = evaluator.evaluate(candidate)

            if solution is not None:
                evaluated.append(solution)

        return sorted(
            evaluated,
            key=lambda solution: solution.score.total,
            reverse=True,
        )
