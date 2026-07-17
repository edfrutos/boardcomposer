"""Tests for advanced export options and preview (SCR-007)."""

import json

from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    Offcut,
    PanelReference,
    SolutionExplanation,
    SolutionScore,
)
from studio.export_options import (
    ExportOptions,
    prepare_solution,
    preview_text,
    render_export,
)


def _solution() -> AssemblySolution:
    return AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50, panel_reference=PanelReference(0, 0))
        ],
        score=SolutionScore(waste_score=4.0),
        explanation=SolutionExplanation(notes=["test"], strengths=["compacta"]),
        offcuts=(Offcut(PanelReference(0, 0), 100, 0, 200, 50),),
    )


def test_prepare_solution_can_drop_offcuts():
    solution = _solution()

    without = prepare_solution(
        solution, ExportOptions(format="svg", include_offcuts=False)
    )

    assert solution.offcuts
    assert without.offcuts == ()


def test_render_export_json_respects_content_flags():
    solution = _solution()

    payload = json.loads(
        render_export(
            solution,
            None,
            ExportOptions(
                format="json",
                include_metrics=False,
                include_explanation=False,
                include_offcuts=False,
            ),
        )
    )

    assert "metrics" not in payload
    assert "notes" not in payload
    assert "offcuts" not in payload
    assert payload["placements"][0]["piece_id"] == "A"


def test_preview_text_includes_format_summary():
    text = preview_text(_solution(), None, ExportOptions(format="pdf"))

    assert "Formato: PDF" in text
    assert "Piezas colocadas: 1" in text
