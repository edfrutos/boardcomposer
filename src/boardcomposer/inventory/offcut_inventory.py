"""Promote solution offcuts to remnant StockPanel inventory (IDE-0025)."""

from __future__ import annotations

from collections import defaultdict

from boardcomposer.domain import AssemblySolution, Offcut, Project, StockPanel


def remnant_id_for(offcut: Offcut, source: StockPanel, index: int) -> str:
    """Stable id: ``{source}-{instance}-R{n}`` (1-based n per physical panel)."""
    base = source.id or f"P{offcut.panel_reference.stock_panel_index + 1}"
    instance = offcut.panel_reference.instance_index
    return f"{base}-{instance}-R{index}"


def remnant_stock_from_offcuts(
    project: Project,
    solution: AssemblySolution,
) -> list[StockPanel]:
    """Map usable offcuts to remnant stock (qty 1, same material/thickness).

    Ids are deterministic so a second promote of the same solution is a
    no-op when those boards already exist. Parent sheets are not consumed:
    the user lowers origin quantity after cutting (ADR-016 / IDE-0025).
    """
    counts: dict[tuple[int, int], int] = defaultdict(int)
    remnants: list[StockPanel] = []
    for offcut in solution.offcuts:
        source = project.stock_panel_for(offcut.panel_reference)
        if source is None:
            continue
        key = (
            offcut.panel_reference.stock_panel_index,
            offcut.panel_reference.instance_index,
        )
        counts[key] += 1
        remnants.append(
            StockPanel(
                length_mm=offcut.length_mm,
                width_mm=offcut.width_mm,
                thickness_mm=source.thickness_mm,
                id=remnant_id_for(offcut, source, counts[key]),
                quantity=1,
                material=source.material,
            )
        )
    return remnants
