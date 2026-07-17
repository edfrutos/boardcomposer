"""Compare two assembly solutions and surface only what changes (SCR-003).

Pure helper for the comparator “panel de diferencias”: given a reference
solution and a candidate, report metric deltas and placement changes so the
UI can show a concise diff without re-deriving comparison rules.
"""

from __future__ import annotations

from dataclasses import dataclass

from boardcomposer.domain import AssemblySolution, BoardPlacement, PanelReference


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

    def summary_lines(self) -> list[str]:
        """Human-readable lines for the Studio differences panel."""
        if self.identical:
            return [
                f"Solución #{self.candidate_index + 1} es idéntica a la "
                f"referencia #{self.reference_index + 1}."
            ]

        lines = [
            f"Diferencias de #{self.candidate_index + 1} "
            f"respecto a la referencia #{self.reference_index + 1}",
            "",
        ]

        if self.metrics:
            lines.append("Métricas")
            for metric in self.metrics:
                marker = ""
                if metric.better == "candidate":
                    marker = "  ↑ mejor aquí"
                elif metric.better == "reference":
                    marker = "  ↑ mejor en referencia"
                lines.append(
                    f"  {metric.label}: {metric.reference} → {metric.candidate}{marker}"
                )
            lines.append("")

        if self.placements:
            lines.append("Colocaciones")
            for change in self.placements:
                lines.append(f"  {change.piece_id}: {change.detail}")
        elif not self.metrics:
            lines.append("Sin diferencias relevantes en métricas ni colocaciones.")

        return lines


def _panel_label(reference: PanelReference | None) -> str:
    if reference is None:
        return "sin panel"
    return f"panel {reference.stock_panel_index + 1}.{reference.instance_index}"


def _placement_key(placement: BoardPlacement) -> tuple:
    return (
        placement.x_mm,
        placement.y_mm,
        placement.length_mm,
        placement.width_mm,
        placement.rotated,
        placement.panel_reference,
    )


def _format_placement(placement: BoardPlacement) -> str:
    return (
        f"({placement.x_mm:g}, {placement.y_mm:g}) "
        f"{placement.length_mm:g}×{placement.width_mm:g} mm"
        f"{' rotada' if placement.rotated else ''}"
        f", {_panel_label(placement.panel_reference)}"
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
) -> list[MetricDelta]:
    deltas: list[MetricDelta] = []

    def add(
        label: str,
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
                label=label,
                reference=ref_text,
                candidate=cand_text,
                better=better,
            )
        )

    add(
        "Piezas colocadas",
        float(len(reference.placements)),
        float(len(candidate.placements)),
        higher_is_better=True,
        as_int=True,
    )
    add(
        "Piezas omitidas",
        float(len(reference.omitted_piece_ids)),
        float(len(candidate.omitted_piece_ids)),
        higher_is_better=False,
        as_int=True,
    )
    add(
        "Huecos internos",
        reference.waste_ratio,
        candidate.waste_ratio,
        higher_is_better=False,
        as_percent=True,
    )
    if board_waste_reference is not None and board_waste_candidate is not None:
        add(
            "Material libre",
            board_waste_reference,
            board_waste_candidate,
            higher_is_better=False,
            as_percent=True,
        )
    add(
        "Largo total (mm)",
        reference.total_length_mm,
        candidate.total_length_mm,
        higher_is_better=False,
        as_int=True,
    )
    add(
        "Ancho total (mm)",
        reference.total_width_mm,
        candidate.total_width_mm,
        higher_is_better=False,
        as_int=True,
    )
    add(
        "Paneles usados",
        float(len(reference.panel_references)),
        float(len(candidate.panel_references)),
        higher_is_better=False,
        as_int=True,
    )
    add(
        "Retales",
        float(len(reference.offcuts)),
        float(len(candidate.offcuts)),
        higher_is_better=True,
        as_int=True,
    )
    add(
        "Puntuación",
        reference.score.total,
        candidate.score.total,
        higher_is_better=True,
    )

    if reference.is_complete != candidate.is_complete:
        deltas.append(
            MetricDelta(
                label="Completitud",
                reference="completa" if reference.is_complete else "parcial",
                candidate="completa" if candidate.is_complete else "parcial",
                better="candidate" if candidate.is_complete else "reference",
            )
        )

    return deltas


def _placement_changes(
    reference: AssemblySolution,
    candidate: AssemblySolution,
) -> list[PlacementChange]:
    ref_map = _placements_by_id(reference)
    cand_map = _placements_by_id(candidate)
    changes: list[PlacementChange] = []

    for piece_id in sorted(set(ref_map) - set(cand_map)):
        changes.append(
            PlacementChange(
                piece_id=piece_id,
                kind="only_reference",
                detail=f"solo en referencia ({_format_placement(ref_map[piece_id])})",
            )
        )

    for piece_id in sorted(set(cand_map) - set(ref_map)):
        changes.append(
            PlacementChange(
                piece_id=piece_id,
                kind="only_candidate",
                detail=f"solo aquí ({_format_placement(cand_map[piece_id])})",
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
                    f"{_format_placement(ref_placement)} → "
                    f"{_format_placement(cand_placement)}"
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
) -> SolutionDiff:
    """Return the structured diff of `candidate` against `reference`."""
    if reference_index == candidate_index:
        return SolutionDiff(
            reference_index=reference_index,
            candidate_index=candidate_index,
            identical=True,
        )

    metrics = tuple(
        _metric_deltas(
            reference,
            candidate,
            board_waste_reference=board_waste_reference,
            board_waste_candidate=board_waste_candidate,
        )
    )
    placements = tuple(_placement_changes(reference, candidate))
    identical = not metrics and not placements

    return SolutionDiff(
        reference_index=reference_index,
        candidate_index=candidate_index,
        identical=identical,
        metrics=metrics,
        placements=placements,
    )


def format_diff_unavailable(reason: str) -> list[str]:
    """Friendly lines when a diff cannot be computed yet."""
    return ["Diferencias", "", reason]
