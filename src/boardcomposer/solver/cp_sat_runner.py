"""Exact single-panel packing via CP-SAT (Google OR-Tools).

Exploratory generator (see ADR-017): unlike the heuristic generators
(MaxRects, Skyline, ...), this one models the problem as a constraint
program and lets an exact solver search for it, bounded by a time limit
since 2D bin packing is NP-hard and an exact search can otherwise run
indefinitely on hard instances.

Scope of this iteration: **one physical panel only** (no multipanel bin
selection yet — see ADR-017 for why). `ortools` is an optional dependency
(`pip install boardcomposer[cp_sat]`); importing this module never fails
even if it isn't installed, so the rest of the solver package stays
usable without it. Only calling `generate_cp_sat_solution` requires it.
"""

from dataclasses import dataclass

from boardcomposer.domain import (
    AssemblySolution,
    Board,
    BoardPlacement,
    Project,
    SolutionExplanation,
)

try:
    from ortools.sat.python import cp_model
except ImportError:  # pragma: no cover - exercised by test_cp_sat_runner.py
    cp_model = None


class CpSatUnavailableError(RuntimeError):
    """Raised when `generate_cp_sat_solution` runs without `ortools`."""


DEFAULT_TIME_LIMIT_SECONDS = 5.0


@dataclass(frozen=True)
class _CandidateItem:
    """A board that fits the bin in at least one orientation."""

    index: int
    board: Board
    fits_upright: bool
    fits_rotated: bool

    @property
    def board_id(self) -> str:
        return self.board.id or f"board-{self.index + 1}"


@dataclass
class _ItemVars:
    """CP-SAT variables tied to one `_CandidateItem`."""

    item: _CandidateItem
    placed: "cp_model.IntVar"
    x_start: "cp_model.IntVar"
    y_start: "cp_model.IntVar"
    rotated: "cp_model.IntVar | None"


def _require_cp_sat() -> None:
    if cp_model is None:
        raise CpSatUnavailableError(
            "CP-SAT requiere el paquete opcional 'ortools' "
            "(pip install 'boardcomposer[cp_sat]')."
        )


def _bin_dimensions(project: Project) -> tuple[int, int] | None:
    """Return the single panel's integer dimensions, or None if the
    project doesn't declare bounded constraints (CP-SAT needs a finite
    domain to build the model)."""
    length = project.constraints.max_length_mm
    width = project.constraints.max_width_mm

    if not length or not width:
        return None

    return round(length), round(width)


def _candidate_items(
    project: Project,
    bin_length_mm: int,
    bin_width_mm: int,
) -> list[_CandidateItem]:
    allow_rotation = project.constraints.allow_rotation
    items = []

    for index, board in enumerate(project.boards):
        length_mm = round(board.length_mm)
        width_mm = round(board.width_mm)
        fits_upright = length_mm <= bin_length_mm and width_mm <= bin_width_mm
        fits_rotated = (
            allow_rotation and width_mm <= bin_length_mm and length_mm <= bin_width_mm
        )

        if fits_upright or fits_rotated:
            items.append(_CandidateItem(index, board, fits_upright, fits_rotated))

    return items


def _add_item_to_model(
    model: "cp_model.CpModel",
    item: _CandidateItem,
    bin_length_mm: int,
    bin_width_mm: int,
) -> tuple[_ItemVars, "cp_model.IntervalVar", "cp_model.IntervalVar"]:
    """Add one board's variables and (optional) interval constraints."""
    length_mm = round(item.board.length_mm)
    width_mm = round(item.board.width_mm)
    can_choose_orientation = item.fits_upright and item.fits_rotated

    if can_choose_orientation:
        rotated = model.NewBoolVar(f"rotated_{item.index}")
        eff_length = model.NewIntVarFromDomain(
            cp_model.Domain.FromValues(sorted({length_mm, width_mm})),
            f"len_{item.index}",
        )
        eff_width = model.NewIntVarFromDomain(
            cp_model.Domain.FromValues(sorted({length_mm, width_mm})),
            f"wid_{item.index}",
        )
        model.Add(eff_length == width_mm).OnlyEnforceIf(rotated)
        model.Add(eff_length == length_mm).OnlyEnforceIf(rotated.Not())
        model.Add(eff_width == length_mm).OnlyEnforceIf(rotated)
        model.Add(eff_width == width_mm).OnlyEnforceIf(rotated.Not())
    else:
        rotated = None
        # Only one orientation is geometrically possible in this bin.
        eff_length = width_mm if item.fits_rotated else length_mm
        eff_width = length_mm if item.fits_rotated else width_mm

    placed = model.NewBoolVar(f"placed_{item.index}")
    x_start = model.NewIntVar(0, bin_length_mm, f"x_{item.index}")
    y_start = model.NewIntVar(0, bin_width_mm, f"y_{item.index}")
    x_end = model.NewIntVar(0, bin_length_mm, f"x_end_{item.index}")
    y_end = model.NewIntVar(0, bin_width_mm, f"y_end_{item.index}")

    x_interval = model.NewOptionalIntervalVar(
        x_start, eff_length, x_end, placed, f"x_ival_{item.index}"
    )
    y_interval = model.NewOptionalIntervalVar(
        y_start, eff_width, y_end, placed, f"y_ival_{item.index}"
    )

    return _ItemVars(item, placed, x_start, y_start, rotated), x_interval, y_interval


def _build_model(
    items: list[_CandidateItem],
    bin_length_mm: int,
    bin_width_mm: int,
) -> tuple["cp_model.CpModel", list[_ItemVars]]:
    model = cp_model.CpModel()
    item_vars: list[_ItemVars] = []
    x_intervals = []
    y_intervals = []

    for item in items:
        vars_for_item, x_interval, y_interval = _add_item_to_model(
            model, item, bin_length_mm, bin_width_mm
        )
        item_vars.append(vars_for_item)
        x_intervals.append(x_interval)
        y_intervals.append(y_interval)

    model.AddNoOverlap2D(x_intervals, y_intervals)
    model.Maximize(sum(vars_for_item.placed for vars_for_item in item_vars))

    return model, item_vars


def _placement_for(
    vars_for_item: _ItemVars, solver: "cp_model.CpSolver"
) -> BoardPlacement:
    item = vars_for_item.item
    length_mm = round(item.board.length_mm)
    width_mm = round(item.board.width_mm)

    if vars_for_item.rotated is not None:
        is_rotated = bool(solver.Value(vars_for_item.rotated))
    else:
        is_rotated = item.fits_rotated and not item.fits_upright

    return BoardPlacement(
        board_id=item.board_id,
        x_mm=solver.Value(vars_for_item.x_start),
        y_mm=solver.Value(vars_for_item.y_start),
        length_mm=width_mm if is_rotated else length_mm,
        width_mm=length_mm if is_rotated else width_mm,
        rotated=is_rotated,
    )


def _empty_solution(note: str, omitted: tuple[str, ...] = ()) -> AssemblySolution:
    return AssemblySolution(
        placements=[],
        explanation=SolutionExplanation(notes=["cp_sat", note]),
        omitted_piece_ids=omitted,
    )


def generate_cp_sat_solution(
    project: Project,
    time_limit_seconds: float = DEFAULT_TIME_LIMIT_SECONDS,
) -> AssemblySolution:
    """Pack `project.boards` onto a single panel with CP-SAT.

    Maximizes the number of pieces placed (partial solutions are
    reported the same way as the heuristic generators, via
    `omitted_piece_ids`). Panel dimensions come from
    `project.constraints` — the same single-panel contract every classic
    generator (horizontal/vertical/free_space/skyline) already follows.
    """
    _require_cp_sat()

    all_ids = tuple(
        board.id or f"board-{index + 1}" for index, board in enumerate(project.boards)
    )

    dimensions = _bin_dimensions(project)
    if dimensions is None or not project.boards:
        return _empty_solution("sin_panel", all_ids)

    bin_length_mm, bin_width_mm = dimensions
    items = _candidate_items(project, bin_length_mm, bin_width_mm)

    placeable_ids = {item.board_id for item in items}
    never_fit = tuple(board_id for board_id in all_ids if board_id not in placeable_ids)

    if not items:
        return _empty_solution("ninguna_pieza_cabe", all_ids)

    model, item_vars = _build_model(items, bin_length_mm, bin_width_mm)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_seconds

    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return _empty_solution("sin_solucion_factible", all_ids)

    placements = [
        _placement_for(vars_for_item, solver)
        for vars_for_item in item_vars
        if solver.Value(vars_for_item.placed)
    ]
    placed_ids = {placement.board_id for placement in placements}
    omitted = never_fit + tuple(
        board_id
        for board_id in all_ids
        if board_id not in placed_ids and board_id not in never_fit
    )
    status_note = "optimo" if status == cp_model.OPTIMAL else "factible"

    return AssemblySolution(
        placements=placements,
        explanation=SolutionExplanation(notes=["cp_sat", status_note]),
        omitted_piece_ids=omitted,
    )
