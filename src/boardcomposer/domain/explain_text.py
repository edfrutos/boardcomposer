"""Format deterministic solution explanations (IDE-0007 MVP, no LLM)."""

from __future__ import annotations

from boardcomposer.domain import AssemblySolution


def format_solution_explanation(
    solution: AssemblySolution,
    *,
    strengths_label: str = "Fortalezas",
    weaknesses_label: str = "Debilidades",
    notes_label: str = "Notas",
    empty_message: str = "Sin explicación disponible para esta candidata.",
) -> str:
    """Return a plain-text explanation block for UI / clipboard."""
    blocks: list[str] = []
    if solution.explanation.strengths:
        blocks.append(strengths_label)
        blocks.extend(f"+ {item}" for item in solution.explanation.strengths)
    if solution.explanation.weaknesses:
        if blocks:
            blocks.append("")
        blocks.append(weaknesses_label)
        blocks.extend(f"- {item}" for item in solution.explanation.weaknesses)
    if solution.explanation.notes:
        if blocks:
            blocks.append("")
        blocks.append(notes_label)
        blocks.extend(f"· {item}" for item in solution.explanation.notes)
    if not blocks:
        return empty_message
    return "\n".join(blocks)
