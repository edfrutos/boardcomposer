from dataclasses import dataclass

from boardcomposer.domain import AssemblySolution
from boardcomposer.solver.validation_result import ValidationResult


@dataclass(frozen=True)
class EvaluationResult:
    """Outcome of evaluating a candidate solution against constraints."""

    solution: AssemblySolution | None
    """The evaluated solution, if it is accepted."""

    validation: ValidationResult
    """The validation result of the solution."""

    @property
    def accepted(self) -> bool:
        """Whether the solution is accepted."""
        return self.solution is not None
