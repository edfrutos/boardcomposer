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
    UNASSIGNED_STOCK_PANEL = "unassigned_stock_panel"
    UNKNOWN_STOCK_PANEL = "unknown_stock_panel"
    EXCEEDS_STOCK_PANEL = "exceeds_stock_panel"
    PANEL_THICKNESS_MISMATCH = "panel_thickness_mismatch"
    PANEL_MATERIAL_MISMATCH = "panel_material_mismatch"


@dataclass(frozen=True)
class ValidationResult:
    """Result of validating a generated solution."""

    valid: bool
    reasons: tuple[ValidationReason, ...] = ()
    complete: bool = True
    missing_board_ids: tuple[str, ...] = ()
