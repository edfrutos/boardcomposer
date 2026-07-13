"""Structured solution validation results."""

from dataclasses import dataclass
from enum import StrEnum


class ValidationReason(StrEnum):
    """Reason why a generated solution is invalid."""

    MISSING_BOARD = "missing_board"
    DUPLICATE_BOARD = "duplicate_board"
    UNKNOWN_BOARD = "unknown_board"
    OVERLAP = "overlap"
    EXCEEDS_CONSTRAINTS = "exceeds_constraints"


@dataclass(frozen=True)
class ValidationResult:
    """Result of validating a generated solution."""

    valid: bool
    reasons: tuple[ValidationReason, ...] = ()
