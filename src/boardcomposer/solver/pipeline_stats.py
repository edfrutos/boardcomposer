"""Statistics collected during candidate pipeline execution."""

from collections import Counter
from dataclasses import dataclass, field

from boardcomposer.solver.validation_result import ValidationReason


@dataclass
class PipelineStats:
    """Execution statistics for the candidate pipeline."""

    generated: int = 0
    unique: int = 0
    accepted: int = 0
    accepted_partial: int = 0
    rejected: int = 0
    rejection_reasons: Counter[ValidationReason] = field(default_factory=Counter)
    cancelled: bool = False
