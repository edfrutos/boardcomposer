from dataclasses import replace

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.cancel import CancellationToken, CancelledError, check_cancelled
from boardcomposer.solver.deduplication import deduplicate_solutions
from boardcomposer.solver.generators import generators_by_name
from boardcomposer.solver.solution_evaluator import SolutionEvaluator
from boardcomposer.solver.strategies import OptimizationStrategy
from boardcomposer.solver.pipeline_stats import PipelineStats
from boardcomposer.solver.solution_ranking import solution_ranking_key


class CandidatePipeline:
    def __init__(
        self,
        project: Project,
        strategy: OptimizationStrategy,
        *,
        cancel: CancellationToken | None = None,
    ) -> None:
        self.project = project
        self.strategy = strategy
        self.cancel = cancel

    def run(self) -> list[AssemblySolution]:
        self.stats = PipelineStats()
        candidates: list[AssemblySolution] = []

        panel_instances = self.project.stock_panel_instances()
        generator_names = (
            ["maxrects"]
            if len(panel_instances) > 1
            else list(self.strategy.generator_names)
        )

        try:
            for generator in generators_by_name(generator_names):
                check_cancelled(self.cancel)
                generated = generator(self.project)
                if len(panel_instances) == 1:
                    reference = panel_instances[0][0]
                    generated = [
                        replace(
                            solution,
                            placements=[
                                replace(
                                    placement,
                                    panel_reference=(
                                        placement.panel_reference or reference
                                    ),
                                )
                                for placement in solution.placements
                            ],
                        )
                        for solution in generated
                    ]
                candidates.extend(generated)

            self.stats.generated = len(candidates)

            unique_candidates = deduplicate_solutions(candidates)
            self.stats.unique = len(unique_candidates)

            evaluator = SolutionEvaluator(
                project=self.project,
                weights=self.strategy.weights,
            )

            evaluated: list[AssemblySolution] = []

            for candidate in unique_candidates:
                check_cancelled(self.cancel)
                result = evaluator.evaluate(candidate)

                if result.solution is None:
                    self.stats.rejected += 1

                    for reason in result.validation.reasons:
                        self.stats.rejection_reasons[reason] += 1

                    continue

                self.stats.accepted += 1
                if not result.solution.is_complete:
                    self.stats.accepted_partial += 1
                evaluated.append(result.solution)

            return sorted(
                evaluated,
                key=solution_ranking_key,
                reverse=True,
            )
        except CancelledError:
            self.stats.cancelled = True
            self.stats.generated = max(self.stats.generated, len(candidates))
            return []
