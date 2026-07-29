"""Validation rules for generated layout solutions."""

from math import isclose

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.layout.validation import has_overlaps
from boardcomposer.solver.constraints_validator import respects_constraints
from boardcomposer.solver.validation_result import (
    ValidationReason,
    ValidationResult,
)

# Reasons that describe a partial (but otherwise geometrically sound)
# solution. A solution missing pieces because they don't fit is still a
# usable result — only broken geometry (overlaps, duplicates, ...) rejects a
# solution outright. See DOC-004 backlog and ADR-016 (retales informativos).
_SOFT_REASONS = frozenset({ValidationReason.MISSING_BOARD})


def validate_solution(
    solution: AssemblySolution,
    project: Project,
) -> ValidationResult:
    """Validate a generated solution and report every detected problem."""
    expected_ids = [board.id for board in project.boards]
    placed_ids = [placement.board_id for placement in solution.placements]

    expected_set = set(expected_ids)
    placed_set = set(placed_ids)

    reasons: list[ValidationReason] = []
    missing_board_ids: tuple[str, ...] = ()

    if len(placed_ids) != len(placed_set):
        reasons.append(ValidationReason.DUPLICATE_BOARD)

    if expected_set - placed_set:
        reasons.append(ValidationReason.MISSING_BOARD)
        missing_board_ids = tuple(
            board_id for board_id in expected_ids if board_id not in placed_set
        )

    if placed_set - expected_set:
        reasons.append(ValidationReason.UNKNOWN_BOARD)

    if project.stock_panels and any(
        placement.panel_reference is None for placement in solution.placements
    ):
        reasons.append(ValidationReason.UNASSIGNED_STOCK_PANEL)

    if any(
        placement.panel_reference is not None
        and project.stock_panel_for(placement.panel_reference) is None
        for placement in solution.placements
    ):
        reasons.append(ValidationReason.UNKNOWN_STOCK_PANEL)

    exceeds_stock_panel = False
    for placement in solution.placements:
        if placement.panel_reference is None:
            continue
        panel = project.stock_panel_for(placement.panel_reference)
        if panel is None:
            continue
        if placement.right_mm > panel.length_mm or placement.top_mm > panel.width_mm:
            exceeds_stock_panel = True
            break

    if exceeds_stock_panel:
        reasons.append(ValidationReason.EXCEEDS_STOCK_PANEL)

    boards_by_id = {board.id: board for board in project.boards}
    thickness_mismatch = False
    material_mismatch = False
    for placement in solution.placements:
        if placement.panel_reference is None:
            continue
        panel = project.stock_panel_for(placement.panel_reference)
        board = boards_by_id.get(placement.board_id)
        if panel is None or board is None:
            continue
        if not isclose(board.thickness_mm, panel.thickness_mm):
            thickness_mismatch = True
        if board.material_key != panel.material_key:
            material_mismatch = True

    if thickness_mismatch:
        reasons.append(ValidationReason.PANEL_THICKNESS_MISMATCH)

    if material_mismatch:
        reasons.append(ValidationReason.PANEL_MATERIAL_MISMATCH)

    if not project.stock_panels and not respects_constraints(
        solution, project.constraints
    ):
        reasons.append(ValidationReason.EXCEEDS_CONSTRAINTS)

    if project.stock_panels:
        panel_groups = {placement.panel_reference for placement in solution.placements}
        overlaps = any(
            has_overlaps(
                [
                    placement
                    for placement in solution.placements
                    if placement.panel_reference == reference
                ]
            )
            for reference in panel_groups
        )
    else:
        overlaps = has_overlaps(solution.placements)

    if overlaps:
        reasons.append(ValidationReason.OVERLAP)

    hard_reasons = [reason for reason in reasons if reason not in _SOFT_REASONS]

    return ValidationResult(
        valid=not hard_reasons,
        reasons=tuple(reasons),
        complete=(
            len(placed_ids) == len(expected_ids)
            and len(placed_ids) == len(placed_set)
            and placed_set == expected_set
        ),
        missing_board_ids=missing_board_ids,
    )


def is_valid_solution(
    solution: AssemblySolution,
    project: Project,
) -> bool:
    """Return whether a generated solution satisfies all core rules."""
    return validate_solution(solution, project).valid
