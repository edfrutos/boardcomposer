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
from boardcomposer.export import prepare_solution_for_export
from studio.export_options import (
    ExportOptions,
    prepare_solution,
    preview_svg,
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


def test_prepare_solution_for_export_core_helper():
    solution = _solution()
    assert prepare_solution_for_export(solution).offcuts == solution.offcuts
    assert prepare_solution_for_export(solution, include_offcuts=False).offcuts == ()
    assert prepare_solution_for_export(solution, include_offcuts=True) is solution


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


def test_render_export_png_and_jpeg_return_svg_payload():
    svg_png = render_export(_solution(), None, ExportOptions(format="png"))
    svg_jpeg = render_export(_solution(), None, ExportOptions(format="jpeg"))
    assert isinstance(svg_png, str)
    assert isinstance(svg_jpeg, str)
    assert "<svg" in svg_png
    assert "<svg" in svg_jpeg


def test_preview_svg_respects_offcuts_option():
    from boardcomposer.export import DEFAULT_SVG_PALETTE

    solution = _solution()

    with_offcuts = preview_svg(solution, None, ExportOptions(include_offcuts=True))
    without_offcuts = preview_svg(solution, None, ExportOptions(include_offcuts=False))

    assert DEFAULT_SVG_PALETTE.offcut_stroke in with_offcuts
    assert DEFAULT_SVG_PALETTE.offcut_stroke not in without_offcuts
    assert "A" in with_offcuts


def test_export_dialog_embeds_graphic_preview(qapp):
    del qapp
    from studio.dialogs import ExportDialog

    dialog = ExportDialog(_solution(), None, ExportOptions(format="svg"))
    pixmap = dialog.graphic_preview.pixmap()

    assert pixmap is not None
    assert not pixmap.isNull()
    assert "Formato: SVG" in dialog.preview.toPlainText()

    dialog.include_offcuts.setChecked(False)
    dialog._refresh_preview()
    assert "Retales: 0" in dialog.preview.toPlainText()


def test_svg_to_raster_bytes_supports_png_and_jpeg(qapp):
    del qapp
    from studio.solution_thumbnail import svg_to_raster_bytes

    svg = preview_svg(_solution(), None, ExportOptions(format="svg"))
    png = svg_to_raster_bytes(svg, image_format="PNG")
    jpeg = svg_to_raster_bytes(svg, image_format="JPEG")
    assert png.startswith(b"\x89PNG")
    assert jpeg[:2] == b"\xff\xd8"
