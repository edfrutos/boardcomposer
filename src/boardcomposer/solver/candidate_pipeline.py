from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.deduplication import deduplicate_solutions
from boardcomposer.solver.generators import generators_by_name
from boardcomposer.solver.solution_evaluator import SolutionEvaluator
from boardcomposer.solver.strategies import OptimizationStrategy
from boardcomposer.solver.pipeline_stats import PipelineStats


class CandidatePipeline:
    def __init__(
        self,
        project: Project,
        strategy: OptimizationStrategy,
    ) -> None:
        self.project = project
        self.strategy = strategy

    def run(self) -> list[AssemblySolution]:
        self.stats = PipelineStats()
        candidates: list[AssemblySolution] = []

        for generator in generators_by_name(list(self.strategy.generator_names)):
            candidates.extend(generator(self.project))

        self.stats.generated = len(candidates)

        unique_candidates = deduplicate_solutions(candidates)
        self.stats.unique = len(unique_candidates)

        evaluator = SolutionEvaluator(
            project=self.project,
            weights=self.strategy.weights,
        )

        evaluated: list[AssemblySolution] = []

        for candidate in unique_candidates:
            result = evaluator.evaluate(candidate)

            if result.solution is None:
                self.stats.rejected += 1

                for reason in result.validation.reasons:
                    self.stats.rejection_reasons[reason] += 1

                continue

            self.stats.accepted += 1
            evaluated.append(result.solution)

        return sorted(
            evaluated,
            key=lambda solution: solution.score.total,
            reverse=True,
        )
