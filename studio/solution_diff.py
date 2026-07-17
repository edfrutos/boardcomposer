"""Compare two assembly solutions and surface only what changes (SCR-003).

Pure helper for the comparator “panel de diferencias”: given a reference
solution and a candidate, report metric deltas and placement changes so the
UI can show a concise diff without re-deriving comparison rules.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from boardcomposer.domain import AssemblySolution, BoardPlacement, PanelReference
from studio.i18n import DEFAULT_LANGUAGE, tr


@dataclass(frozen=True)
class MetricDelta:
    """A comparable scalar that differs between reference and candidate."""

    label: str
    reference: str
    candidate: str
    better: str | None = None  # "reference", "candidate", or None if tie/neutral


@dataclass(frozen=True)
class PlacementChange:
    """How a single piece differs between the two solutions."""

    piece_id: str
    kind: str  # only_reference | only_candidate | moved
    detail: str


@dataclass(frozen=True)
class SolutionDiff:
    """Structured differences between a reference and a candidate solution."""

    reference_index: int
    candidate_index: int
    identical: bool
    metrics: tuple[MetricDelta, ...] = ()
    placements: tuple[PlacementChange, ...] = ()
    language: str = DEFAULT_LANGUAGE

    def summary_lines(self) -> list[str]:
        """Human-readable lines for the Studio differences panel."""
        lang = self.language
        if self.identical:
            return [
                tr(
                    "diff.identical",
                    lang,
                    candidate=self.candidate_index + 1,
                    reference=self.reference_index + 1,
                )
            ]

        lines = [
            tr(
                "diff.header",
                lang,
                candidate=self.candidate_index + 1,
                reference=self.reference_index + 1,
            ),
            "",
        ]

        if self.metrics:
            lines.append(tr("diff.metrics", lang))
            for metric in self.metrics:
                marker = ""
                if metric.better == "candidate":
                    marker = tr("diff.better_here", lang)
                elif metric.better == "reference":
                    marker = tr("diff.better_reference", lang)
                lines.append(
                    f"  {metric.label}: {metric.reference} → {metric.candidate}{marker}"
                )
            lines.append("")

        if self.placements:
            lines.append(tr("diff.placements", lang))
            for change in self.placements:
                lines.append(f"  {change.piece_id}: {change.detail}")
        elif not self.metrics:
            lines.append(tr("diff.none", lang))

        return lines


def _panel_label(reference: PanelReference | None, language: str) -> str:
    if reference is None:
        return tr("diff.no_panel", language)
    return tr(
        "diff.panel",
        language,
        stock=reference.stock_panel_index + 1,
        instance=reference.instance_index,
    )


def _placement_key(placement: BoardPlacement) -> tuple:
    return (
        placement.x_mm,
        placement.y_mm,
        placement.length_mm,
        placement.width_mm,
        placement.rotated,
        placement.panel_reference,
    )


def _format_placement(placement: BoardPlacement, language: str) -> str:
    rotated = tr("diff.rotated", language) if placement.rotated else ""
    return (
        f"({placement.x_mm:g}, {placement.y_mm:g}) "
        f"{placement.length_mm:g}×{placement.width_mm:g} mm"
        f"{rotated}"
        f", {_panel_label(placement.panel_reference, language)}"
    )


def _placements_by_id(
    solution: AssemblySolution,
) -> dict[str, BoardPlacement]:
    return {placement.board_id: placement for placement in solution.placements}


def _metric_deltas(
    reference: AssemblySolution,
    candidate: AssemblySolution,
    *,
    board_waste_reference: float | None,
    board_waste_candidate: float | None,
    language: str,
) -> list[MetricDelta]:
    deltas: list[MetricDelta] = []

    def add(
        label_key: str,
        ref_value: float,
        cand_value: float,
        *,
        higher_is_better: bool,
        as_percent: bool = False,
        as_int: bool = False,
    ) -> None:
        if ref_value == cand_value:
            return
        if as_percent:
            ref_text = f"{ref_value:.1%}"
            cand_text = f"{cand_value:.1%}"
        elif as_int:
            ref_text = f"{ref_value:.0f}"
            cand_text = f"{cand_value:.0f}"
        else:
            ref_text = f"{ref_value:.2f}"
            cand_text = f"{cand_value:.2f}"

        if cand_value == ref_value:
            better = None
        elif higher_is_better:
            better = "candidate" if cand_value > ref_value else "reference"
        else:
            better = "candidate" if cand_value < ref_value else "reference"

        deltas.append(
            MetricDelta(
                label=tr(label_key, language),
                reference=ref_text,
                candidate=cand_text,
                better=better,
            )
        )

    add(
        "diff.metric.pieces",
        float(len(reference.placements)),
        float(len(candidate.placements)),
        higher_is_better=True,
        as_int=True,
    )
    add(
        "diff.metric.omitted",
        float(len(reference.omitted_piece_ids)),
        float(len(candidate.omitted_piece_ids)),
        higher_is_better=False,
        as_int=True,
    )
    add(
        "diff.metric.waste",
        reference.waste_ratio,
        candidate.waste_ratio,
        higher_is_better=False,
        as_percent=True,
    )
    if board_waste_reference is not None and board_waste_candidate is not None:
        add(
            "diff.metric.board_free",
            board_waste_reference,
            board_waste_candidate,
            higher_is_better=False,
            as_percent=True,
        )
    add(
        "diff.metric.length",
        reference.total_length_mm,
        candidate.total_length_mm,
        higher_is_better=False,
        as_int=True,
    )
    add(
        "diff.metric.width",
        reference.total_width_mm,
        candidate.total_width_mm,
        higher_is_better=False,
        as_int=True,
    )
    add(
        "diff.metric.panels",
        float(len(reference.panel_references)),
        float(len(candidate.panel_references)),
        higher_is_better=False,
        as_int=True,
    )
    add(
        "diff.metric.offcuts",
        float(len(reference.offcuts)),
        float(len(candidate.offcuts)),
        higher_is_better=True,
        as_int=True,
    )
    add(
        "diff.metric.score",
        reference.score.total,
        candidate.score.total,
        higher_is_better=True,
    )

    if reference.is_complete != candidate.is_complete:
        deltas.append(
            MetricDelta(
                label=tr("diff.metric.completeness", language),
                reference=tr(
                    "diff.complete" if reference.is_complete else "diff.partial",
                    language,
                ),
                candidate=tr(
                    "diff.complete" if candidate.is_complete else "diff.partial",
                    language,
                ),
                better="candidate" if candidate.is_complete else "reference",
            )
        )

    return deltas


def _placement_changes(
    reference: AssemblySolution,
    candidate: AssemblySolution,
    language: str,
) -> list[PlacementChange]:
    ref_map = _placements_by_id(reference)
    cand_map = _placements_by_id(candidate)
    changes: list[PlacementChange] = []

    for piece_id in sorted(set(ref_map) - set(cand_map)):
        changes.append(
            PlacementChange(
                piece_id=piece_id,
                kind="only_reference",
                detail=tr(
                    "diff.only_reference",
                    language,
                    placement=_format_placement(ref_map[piece_id], language),
                ),
            )
        )

    for piece_id in sorted(set(cand_map) - set(ref_map)):
        changes.append(
            PlacementChange(
                piece_id=piece_id,
                kind="only_candidate",
                detail=tr(
                    "diff.only_candidate",
                    language,
                    placement=_format_placement(cand_map[piece_id], language),
                ),
            )
        )

    for piece_id in sorted(set(ref_map) & set(cand_map)):
        ref_placement = ref_map[piece_id]
        cand_placement = cand_map[piece_id]
        if _placement_key(ref_placement) == _placement_key(cand_placement):
            continue
        changes.append(
            PlacementChange(
                piece_id=piece_id,
                kind="moved",
                detail=(
                    f"{_format_placement(ref_placement, language)} → "
                    f"{_format_placement(cand_placement, language)}"
                ),
            )
        )

    return changes


def compare_solutions(
    reference: AssemblySolution,
    candidate: AssemblySolution,
    *,
    reference_index: int,
    candidate_index: int,
    board_waste_reference: float | None = None,
    board_waste_candidate: float | None = None,
    language: str = DEFAULT_LANGUAGE,
) -> SolutionDiff:
    """Return the structured diff of `candidate` against `reference`."""
    if reference_index == candidate_index:
        return SolutionDiff(
            reference_index=reference_index,
            candidate_index=candidate_index,
            identical=True,
            language=language,
        )

    metrics = tuple(
        _metric_deltas(
            reference,
            candidate,
            board_waste_reference=board_waste_reference,
            board_waste_candidate=board_waste_candidate,
            language=language,
        )
    )
    placements = tuple(_placement_changes(reference, candidate, language))
    identical = not metrics and not placements

    return SolutionDiff(
        reference_index=reference_index,
        candidate_index=candidate_index,
        identical=identical,
        metrics=metrics,
        placements=placements,
        language=language,
    )


def truncate_solution_to_step(
    solution: AssemblySolution,
    step: int,
) -> AssemblySolution:
    """Return a copy revealing only the first ``step`` placements."""
    count = max(0, min(step, len(solution.placements)))
    return replace(solution, placements=list(solution.placements[:count]))


def compare_solutions_at_step(
    reference: AssemblySolution,
    candidate: AssemblySolution,
    step: int,
    *,
    reference_index: int,
    candidate_index: int,
    language: str = DEFAULT_LANGUAGE,
) -> list[str]:
    """Diff the first ``step`` placements of each solution (SCR-003 sync).

    Used while the Timeline walks through the candidate: the Comparador
    shows how reference and candidate diverge up to the same reveal count.
    """
    ref_total = len(reference.placements)
    cand_total = len(candidate.placements)
    max_total = max(ref_total, cand_total)
    clamped = max(0, min(step, max_total))

    header = tr(
        "diff.sync_header",
        language,
        step=clamped,
        total=max_total,
        candidate=candidate_index + 1,
        reference=reference_index + 1,
    )

    if clamped == 0:
        return [header, "", tr("diff.sync_empty", language)]

    ref_part = truncate_solution_to_step(reference, clamped)
    cand_part = truncate_solution_to_step(candidate, clamped)

    if reference_index == candidate_index:
        return [
            header,
            "",
            tr(
                "diff.sync_same_solution",
                language,
                revealed=len(cand_part.placements),
                total=cand_total,
            ),
        ]

    diff = compare_solutions(
        ref_part,
        cand_part,
        reference_index=reference_index,
        candidate_index=candidate_index,
        language=language,
    )
    lines = [header, ""]
    if diff.identical:
        lines.append(tr("diff.sync_matched", language, step=clamped))
        return lines

    if diff.metrics:
        lines.append(tr("diff.metrics", language))
        for metric in diff.metrics:
            marker = ""
            if metric.better == "candidate":
                marker = tr("diff.better_here", language)
            elif metric.better == "reference":
                marker = tr("diff.better_reference", language)
            lines.append(
                f"  {metric.label}: {metric.reference} → {metric.candidate}{marker}"
            )
        lines.append("")

    if diff.placements:
        lines.append(tr("diff.placements", language))
        for change in diff.placements:
            lines.append(f"  {change.piece_id}: {change.detail}")
    elif not diff.metrics:
        lines.append(tr("diff.none", language))

    return lines


def format_diff_unavailable(
    reason_key: str,
    language: str = DEFAULT_LANGUAGE,
) -> list[str]:
    """Friendly lines when a diff cannot be computed yet."""
    return [tr("diff.title", language), "", tr(reason_key, language)]
