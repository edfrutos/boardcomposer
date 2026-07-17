from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.cancel import CancellationToken
from boardcomposer.solver.candidate_pipeline import CandidatePipeline
from boardcomposer.solver.pipeline_stats import PipelineStats
from boardcomposer.solver.solve_trace import SolveTrace
from boardcomposer.solver.strategies import (
    OptimizationStrategy,
    balanced_strategy,
)

from .base_solver import BaseSolver


class GeometrySolver(BaseSolver):
    def __init__(
        self,
        project: Project,
        strategy: OptimizationStrategy | None = None,
        *,
        cancel: CancellationToken | None = None,
    ) -> None:
        self.project = project
        self.strategy = strategy or balanced_strategy()
        self.cancel = cancel
        self.stats = PipelineStats()
        self.trace = SolveTrace()

    def solve(self) -> list[AssemblySolution]:
        pipeline = CandidatePipeline(
            project=self.project,
            strategy=self.strategy,
            cancel=self.cancel,
        )

        solutions = pipeline.run()
        self.stats = pipeline.stats
        self.trace = pipeline.trace

        return solutions
