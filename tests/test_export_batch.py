"""Ranked candidate batch export (IDE-0035 / SCR-007)."""

from __future__ import annotations

from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    PanelReference,
    SolutionExplanation,
    SolutionScore,
)
from studio.export_batch import (
    export_ranked_solutions,
    ranked_export_filename,
    write_export_payload,
)
from studio.export_options import ExportOptions, preview_svg, preview_text


def _solution(piece_id: str = "A") -> AssemblySolution:
    return AssemblySolution(
        placements=[
            BoardPlacement(
                piece_id, 0, 0, 100, 50, panel_reference=PanelReference(0, 0)
            )
        ],
        score=SolutionScore(waste_score=4.0),
        explanation=SolutionExplanation(notes=["test"]),
    )


def test_ranked_export_filename_is_1_based_and_padded():
    assert ranked_export_filename(0, "svg") == "boardcomposer-solution-01.svg"
    assert ranked_export_filename(9, "pdf") == "boardcomposer-solution-10.pdf"


def test_export_ranked_solutions_writes_numbered_svg(tmp_path):
    written = export_ranked_solutions(
        [_solution("A"), _solution("B")],
        None,
        ExportOptions(format="svg"),
        tmp_path,
    )

    assert [path.name for path in written] == [
        "boardcomposer-solution-01.svg",
        "boardcomposer-solution-02.svg",
    ]
    first = written[0].read_text(encoding="utf-8")
    second = written[1].read_text(encoding="utf-8")
    assert "<svg" in first
    assert "A 100x50" in first
    assert "B 100x50" in second


def test_write_export_payload_png_uses_dpi(qapp, tmp_path):
    del qapp
    path = tmp_path / "one.png"
    svg = preview_svg(_solution(), None, ExportOptions(format="png"))
    write_export_payload(path, svg, ExportOptions(format="png", raster_dpi=72))
    assert path.read_bytes().startswith(b"\x89PNG")
    path = tmp_path / "one.json"
    payload = '{"ok": true}'
    write_export_payload(path, payload, ExportOptions(format="json"))
    assert path.read_text(encoding="utf-8") == payload


def test_preview_text_mentions_batch_when_ranking_has_several():
    text = preview_text(
        _solution(),
        None,
        ExportOptions(format="svg", export_batch=True),
        ranked_count=3,
    )
    assert "Lote: 3 archivos boardcomposer-solution-01.svg" in text


def test_export_dialog_batch_enabled_only_with_several_candidates(qapp):
    del qapp
    from studio.dialogs import ExportDialog

    single = ExportDialog(_solution(), None, ExportOptions(format="svg"))
    assert not single.export_batch.isEnabled()
    assert not single.options().export_batch

    many = ExportDialog(
        _solution(),
        None,
        ExportOptions(format="svg", export_batch=True),
        ranked_count=4,
    )
    assert many.export_batch.isEnabled()
    assert many.export_batch.isChecked()
    assert many.options().export_batch is True
    assert "Exportar las 4 candidatas" in many.export_batch.text()
    assert "Lote: 4 archivos" in many.preview.toPlainText()
