from dataclasses import replace

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.cancel import (
    CancellationToken,
    CancelledError,
    check_cancelled,
)
from boardcomposer.solver.deduplication import deduplicate_solutions
from boardcomposer.solver.generators import generators_by_name
from boardcomposer.solver.solution_evaluator import SolutionEvaluator
from boardcomposer.solver.strategies import OptimizationStrategy
from boardcomposer.solver.pipeline_stats import PipelineStats
from boardcomposer.solver.placement_failures import (
    PlacementFailureLog,
    capture_placement_failures,
)
from boardcomposer.solver.solution_ranking import solution_ranking_key
from boardcomposer.solver.solve_trace import SolveTrace


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
        self.trace = SolveTrace()

    def run(self) -> list[AssemblySolution]:
        self.stats = PipelineStats()
        self.trace = SolveTrace()
        candidates: list[AssemblySolution] = []

        panel_instances = self.project.stock_panel_instances()
        generator_names = (
            ["maxrects"]
            if len(panel_instances) > 1
            else list(self.strategy.generator_names)
        )

        try:
            for name in generator_names:
                check_cancelled(self.cancel)
                self.trace.record("generator_started", algorithm=name)
                generator = generators_by_name([name])[0]
                if name == "maxrects":
                    failure_log = PlacementFailureLog()
                    with capture_placement_failures(failure_log):
                        generated = generator(self.project)
                    self._record_placement_failures(failure_log)
                else:
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
                self.trace.record(
                    "generator_finished",
                    algorithm=name,
                    count=len(generated),
                )
                candidates.extend(generated)

            self.stats.generated = len(candidates)

            unique_candidates = deduplicate_solutions(candidates)
            self.stats.unique = len(unique_candidates)

            self.trace.record(
                "evaluation_started",
                unique=len(unique_candidates),
            )

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

            ranked = sorted(
                evaluated,
                key=solution_ranking_key,
                reverse=True,
            )
            self.trace.record(
                "evaluation_finished",
                accepted=self.stats.accepted,
                rejected=self.stats.rejected,
            )
            if ranked:
                best = ranked[0]
                algorithm = (
                    best.explanation.notes[0] if best.explanation.notes else "unknown"
                )
                self.trace.record(
                    "build_order",
                    algorithm=algorithm,
                    pieces=tuple(p.board_id for p in best.placements),
                )
            return ranked
        except CancelledError:
            self.stats.cancelled = True
            self.stats.generated = max(self.stats.generated, len(candidates))
            self.trace.record("cancelled")
            return []

    def _record_placement_failures(self, failure_log: PlacementFailureLog) -> None:
        """Fold MaxRects failure samples into the solve trace."""
        if failure_log.total == 0:
            return
        self.trace.record(
            "placement_failures_summary",
            total=failure_log.total,
            incompatible=failure_log.counts.get("incompatible", 0),
            no_fit=failure_log.counts.get("no_fit", 0),
            unique=len(failure_log.failures),
        )
        for failure in failure_log.failures:
            payload: dict[str, object] = {
                "piece": failure.piece_id,
                "reason": failure.reason,
                "algorithm": failure.algorithm,
            }
            if failure.stock_panel_index is not None:
                payload["stock"] = failure.stock_panel_index
            if failure.instance_index is not None:
                payload["instance"] = failure.instance_index
            self.trace.record("placement_failed", **payload)
