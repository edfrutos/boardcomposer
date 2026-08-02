"""Tests for deterministic explanation formatting (IDE-0007 MVP)."""

from boardcomposer.domain import AssemblySolution, SolutionExplanation
from boardcomposer.domain.explain_text import format_solution_explanation


def test_format_solution_explanation_sections():
    solution = AssemblySolution(
        placements=[],
        explanation=SolutionExplanation(
            strengths=["compacta"],
            weaknesses=["parcial"],
            notes=["maxrects"],
        ),
    )
    text = format_solution_explanation(solution)
    assert "Fortalezas" in text
    assert "+ compacta" in text
    assert "Debilidades" in text
    assert "- parcial" in text
    assert "Notas" in text
    assert "· maxrects" in text


def test_format_solution_explanation_empty():
    solution = AssemblySolution(placements=[])
    assert "Sin explicación" in format_solution_explanation(solution)
