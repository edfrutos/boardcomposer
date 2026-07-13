from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.candidate_pipeline import CandidatePipeline
from boardcomposer.solver.pipeline_stats import PipelineStats
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
    ) -> None:
        self.project = project
        self.strategy = strategy or balanced_strategy()
        self.stats = PipelineStats()

    def solve(self) -> list[AssemblySolution]:
        pipeline = CandidatePipeline(
            project=self.project,
            strategy=self.strategy,
        )

        solutions = pipeline.run()
        self.stats = pipeline.stats

        return solutions
